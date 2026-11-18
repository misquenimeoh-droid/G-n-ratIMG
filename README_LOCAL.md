# IMAGINA — moteur Python local

Ce moteur ajoute une génération locale sur ton propre ordinateur. Il est indépendant de GitHub Pages : le site web reste hébergé sur GitHub, mais le calcul se fait sur ton PC.

## Configuration

- Python 3.10 ou 3.11.
- GPU NVIDIA conseillé (8 Go de VRAM minimum pour tenter SDXL Turbo, 12 Go ou plus recommandés). Le CPU fonctionne parfois mais sera très lent.
- Plusieurs Go de stockage pour les modèles. Le premier lancement télécharge automatiquement les poids depuis Hugging Face.
- Connexion Internet nécessaire au premier téléchargement ; ensuite les modèles déjà téléchargés peuvent être réutilisés hors ligne.

## Démarrage Windows

1. Installe Python 3.11.
2. Double-clique sur `start_windows.bat` : il crée l’environnement et installe les bibliothèques du moteur.
3. Si PyTorch manque, ouvre une deuxième fenêtre CMD, exécute les deux commandes affichées par le script, puis installe PyTorch depuis https://pytorch.org/get-started/locally/ (CUDA pour NVIDIA, CPU sinon).
4. Relance `start_windows.bat` et attends le téléchargement initial du modèle SDXL Turbo.
5. Ouvre IMAGINA sur GitHub Pages, choisis **Moteur local Python**, puis clique sur **Tester le moteur**.

Le serveur écoute uniquement sur `http://127.0.0.1:7860` : il n'est pas exposé sur Internet.

## Modèles et performances

- Génération par défaut : `stabilityai/sdxl-turbo`, optimisé pour quelques étapes (1 à 4).
- Image-vers-image : même modèle, force de transformation réglable.
- Inpainting : `diffusers/stable-diffusion-xl-1.0-inpainting-0.1`, téléchargé seulement lors de la première retouche masquée.
- GPU NVIDIA avec FP16, attention/ VAE slicing et tuilage activés quand disponibles.
- Les temps réels dépendent du GPU, de la VRAM, de la résolution et du modèle. Aucun temps de génération n'est garanti.

Variables facultatives :
- `IMAGINA_MODEL_ID` : autre modèle Diffusers compatible.
- `IMAGINA_INPAINT_MODEL_ID` : autre modèle d'inpainting compatible.
- `IMAGINA_REALESRGAN_WEIGHTS` : chemin vers `RealESRGAN_x4plus.pth`.
- `IMAGINA_GFPGAN_WEIGHTS` : chemin vers `GFPGANv1.4.pth`.

## Amélioration locale optionnelle

Les endpoints GFPGAN et RealESRGAN sont prévus dans le moteur. Pour les activer, installe les dépendances de `requirements-optional.txt` et place les poids pré-entraînés correspondants dans le dossier `weights/`. Leurs dépendances peuvent être sensibles aux versions de PyTorch/Torchvision ; ce module est donc optionnel et ne bloque pas la génération.

## Confidentialité et sécurité

Le moteur écoute sur localhost. Il n'accepte pas de connexion distante. Les images envoyées par l'interface à ce moteur restent sur ton ordinateur. N'expose pas le port 7860 publiquement sans authentification et configuration de sécurité adaptées.

## Dépannage

- **CUDA indisponible** : réinstalle PyTorch avec la bonne version CUDA ou utilise CPU (lent).
- **Out of memory** : baisse largeur/hauteur, ferme les logiciels GPU et utilise un modèle plus léger.
- **Erreur CORS** : ouvre le site en HTTPS et vérifie que le moteur est démarré sur le port 7860.
- **Téléchargement bloqué** : vérifie l'accès à Hugging Face ; accepte la licence du modèle si le dépôt l'exige.
