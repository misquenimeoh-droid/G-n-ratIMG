# IMAGINA — AI Image Studio

Studio web de génération d'images IA, en français, conçu pour être publié avec GitHub Pages.

## Fonctionnalités

- Génération d'images depuis une description avec l'API Pollinations.
- Sélection de modèles d'image (FLUX, GPT Image, Gemini, Seedream, Ideogram).
- Styles rapides : anime, semi-réaliste, photoréaliste, manga, 3D, fantasy, etc.
- Prompt négatif, formats portrait/paysage/carré/cinéma, taille et variations.
- Seed personnalisable pour reproduire une génération.
- Galerie de session, aperçu agrandi, copie du prompt et téléchargement.
- Interface responsive pour ordinateur, tablette et mobile.

## Démarrage

1. Ouvrir le site publié ou télécharger `index.html`.
2. Créer une clé secrète Pollinations sur https://enter.pollinations.ai/keys.
3. Coller la clé dans le champ « Clé API Pollinations ».
4. Décrire l'image, choisir le modèle et cliquer sur « Générer mes images ».

La génération peut consommer le solde ou le budget associé à la clé. Les modèles disponibles, leurs prix et leurs permissions dépendent du compte Pollinations. Consultez la documentation officielle : https://gen.pollinations.ai/docs.

## Publication GitHub Pages

1. Ouvrir **Settings → Pages**.
2. Choisir **Deploy from a branch**.
3. Sélectionner la branche `main` et le dossier `/ (root)`.
4. Enregistrer et attendre la fin du déploiement.

## Sécurité

- La clé API est saisie à la demande et conservée uniquement dans la mémoire de la page.
- Elle n'est pas enregistrée dans le dépôt, le stockage local ou le code source.
- Ne jamais publier une clé secrète `sk_...` dans GitHub, dans une capture d'écran ou dans un lien.
- Pour une application publique avec plusieurs utilisateurs, intégrer un flux OAuth Pollinations Connect / Pollinations Pay (PKCE) ou un backend sécurisé. Ne pas partager une clé personnelle entre visiteurs.

## Limites connues

- Le générateur dépend de la disponibilité et des règles de l'API Pollinations.
- Une clé API valide et un budget suffisant sont nécessaires.
- La galerie est conservée uniquement pendant la session ouverte ; elle n'est pas synchronisée entre appareils.
- Les modèles affichés sont des choix proposés par l'interface ; l'accès effectif dépend des autorisations du compte et du catalogue fournisseur.
- Le paramètre de taille est une indication envoyée au fournisseur : la résolution finale peut varier selon le modèle.

## Licence

Aucune licence open-source n'est déclarée pour ce dépôt. Ajouter une licence si vous souhaitez autoriser explicitement la réutilisation du code.
