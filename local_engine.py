"""
IMAGINA Local Engine — moteur Python local (GPU NVIDIA recommandé).
Démarrage : start_windows.bat ou python local_engine.py
Modèle par défaut : stabilityai/sdxl-turbo (téléchargement initial depuis Hugging Face).
"""
import base64, io, os, threading, time
from typing import Optional
import torch
from PIL import Image
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from diffusers import AutoPipelineForText2Image, AutoPipelineForImage2Image, AutoPipelineForInpainting, EulerAncestralDiscreteScheduler

MODEL_ID = os.getenv("IMAGINA_MODEL_ID", "stabilityai/sdxl-turbo")
INPAINT_MODEL_ID = os.getenv("IMAGINA_INPAINT_MODEL_ID", "diffusers/stable-diffusion-xl-1.0-inpainting-0.1")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32
PIPELINES = {}
LOCK = threading.Lock()
app = FastAPI(title="IMAGINA Local Engine", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["https://misquenimeoh-droid.github.io", "http://localhost:7860", "http://127.0.0.1:7860"], allow_methods=["GET", "POST"], allow_headers=["Content-Type"])

class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)
    negative_prompt: str = Field(default="", max_length=2000)
    width: int = Field(default=768, ge=256, le=1024)
    height: int = Field(default=768, ge=256, le=1024)
    steps: int = Field(default=4, ge=1, le=8)
    seed: Optional[int] = None
    source_image: Optional[str] = None
    source_mask: Optional[str] = None
    strength: float = Field(default=0.55, ge=0.05, le=0.95)

class EnhanceRequest(BaseModel):
    image: str
    operation: str

def decode_image(value: str) -> Image.Image:
    if "," in value and value.startswith("data:"):
        value = value.split(",", 1)[1]
    try:
        raw = base64.b64decode(value, validate=True)
        if len(raw) > 20 * 1024 * 1024:
            raise ValueError("Image trop volumineuse (20 Mo maximum).")
        return Image.open(io.BytesIO(raw)).convert("RGB")
    except Exception as exc:
        raise HTTPException(400, f"Image invalide : {exc}")

def encode_image(image: Image.Image) -> str:
    out = io.BytesIO()
    image.save(out, format="WEBP", quality=94, method=6)
    return base64.b64encode(out.getvalue()).decode("ascii")

def load_pipe(kind: str):
    if kind in PIPELINES:
        return PIPELINES[kind]
    model = INPAINT_MODEL_ID if kind == "inpaint" else MODEL_ID
    if kind == "text":
        pipe = AutoPipelineForText2Image.from_pretrained(model, torch_dtype=DTYPE, use_safetensors=True)
    elif kind == "image":
        pipe = AutoPipelineForImage2Image.from_pretrained(model, torch_dtype=DTYPE, use_safetensors=True)
    else:
        pipe = AutoPipelineForInpainting.from_pretrained(model, torch_dtype=DTYPE, use_safetensors=True)
    if hasattr(pipe, "scheduler") and kind != "inpaint":
        pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)
    pipe = pipe.to(DEVICE)
    try:
        pipe.enable_attention_slicing()
        pipe.enable_vae_slicing()
        pipe.enable_vae_tiling()
    except Exception:
        pass
    if DEVICE == "cuda":
        try:
            pipe.unet.to(memory_format=torch.channels_last)
        except Exception:
            pass
    PIPELINES[kind] = pipe
    return pipe

@app.get("/api/health")
def health():
    return {
        "ok": True, "device": DEVICE, "cuda": torch.cuda.is_available(),
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "model": MODEL_ID, "inpaint_model": INPAINT_MODEL_ID,
        "pipelines_loaded": list(PIPELINES.keys()),
        "torch": torch.__version__
    }

@app.post("/api/generate")
def generate(req: GenerateRequest):
    if not req.prompt.strip():
        raise HTTPException(400, "Décris l’image avant de lancer la génération.")
    if req.width % 8 or req.height % 8:
        raise HTTPException(400, "Largeur et hauteur doivent être des multiples de 8.")
    with LOCK:
        try:
            actual_seed = req.seed if req.seed is not None else int(time.time_ns() % 2**31)
            generator = torch.Generator(device=DEVICE).manual_seed(actual_seed)
            common = dict(prompt=req.prompt, negative_prompt=req.negative_prompt or None,
                          width=req.width, height=req.height, num_inference_steps=req.steps,
                          generator=generator)
            if req.source_image:
                source = decode_image(req.source_image).resize((req.width, req.height), Image.Resampling.LANCZOS)
                if req.source_mask:
                    mask = decode_image(req.source_mask).convert("L").resize((req.width, req.height), Image.Resampling.NEAREST)
                    pipe = load_pipe("inpaint")
                    result = pipe(**common, image=source, mask_image=mask,
                                  strength=req.strength, guidance_scale=0.0).images[0]
                else:
                    pipe = load_pipe("image")
                    result = pipe(**common, image=source, strength=req.strength,
                                  guidance_scale=0.0).images[0]
            else:
                pipe = load_pipe("text")
                result = pipe(**common, guidance_scale=0.0).images[0]
            return {"ok": True, "image": encode_image(result), "device": DEVICE,
                    "model": INPAINT_MODEL_ID if req.source_mask else MODEL_ID,
                    "seed": actual_seed}
        except HTTPException:
            raise
        except torch.cuda.OutOfMemoryError:
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            raise HTTPException(507, "Mémoire GPU insuffisante. Réduis la résolution ou ferme les autres applications GPU.")
        except Exception as exc:
            raise HTTPException(500, f"Génération locale impossible : {type(exc).__name__}: {exc}")

@app.post("/api/enhance")
def enhance(req: EnhanceRequest):
    image = decode_image(req.image)
    try:
        import numpy as np
        if req.operation == "upscale":
            from realesrgan import RealESRGANer
            from basicsr.archs.rrdbnet_arch import RRDBNet
            weights = os.getenv("IMAGINA_REALESRGAN_WEIGHTS", "weights/RealESRGAN_x4plus.pth")
            if not os.path.isfile(weights):
                raise HTTPException(424, "Poids RealESRGAN absents. Consulte README_LOCAL.md pour les installer.")
            model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
            upsampler = RealESRGANer(scale=4, model_path=weights, model=model,
                                     tile=256 if DEVICE == "cuda" else 128,
                                     tile_pad=10, pre_pad=0, half=(DEVICE == "cuda"))
            output, _ = upsampler.enhance(np.array(image)[:, :, ::-1], outscale=4)
            result = Image.fromarray(output[:, :, ::-1])
        elif req.operation == "face":
            from gfpgan import GFPGANer
            weights = os.getenv("IMAGINA_GFPGAN_WEIGHTS", "weights/GFPGANv1.4.pth")
            if not os.path.isfile(weights):
                raise HTTPException(424, "Poids GFPGAN absents. Consulte README_LOCAL.md pour les installer.")
            restorer = GFPGANer(model_path=weights, upscale=2, arch="clean",
                                channel_multiplier=2, bg_upsampler=None, device=DEVICE)
            _, _, restored = restorer.enhance(np.array(image)[:, :, ::-1],
                                               has_aligned=False, only_center_face=False,
                                               paste_back=True)
            result = Image.fromarray(restored[:, :, ::-1])
        else:
            raise HTTPException(400, "Opération inconnue. Choisis face ou upscale.")
        return {"ok": True, "image": encode_image(result), "device": DEVICE}
    except HTTPException:
        raise
    except ImportError as exc:
        raise HTTPException(424, f"Module optionnel absent : {exc}. Consulte README_LOCAL.md.")
    except Exception as exc:
        raise HTTPException(500, f"Amélioration impossible : {type(exc).__name__}: {exc}")

if __name__ == "__main__":
    import uvicorn
    print(f"IMAGINA Local Engine · {DEVICE.upper()} · {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU (lent)'}")
    uvicorn.run(app, host="127.0.0.1", port=7860, log_level="info")
