# IMAGINA — AI Image Studio

Petit studio web autonome en français pour préparer des prompts et demander des images à un fournisseur tiers.

## Lancer en local
1. Téléchargez `index.html`.
2. Ouvrez-le dans un navigateur récent.
3. Saisissez une description, choisissez un style et cliquez sur **Générer mes images**.

## Publier avec GitHub Pages
1. Ajoutez `index.html` à la racine de votre dépôt GitHub.
2. Dans **Settings → Pages**, choisissez **Deploy from a branch**.
3. Sélectionnez la branche `main` et le dossier `/ (root)`, puis enregistrez.
4. Attendez la fin du déploiement GitHub Pages.

## À propos du service d'images
Cette version utilise une URL de démonstration basée sur `image.pollinations.ai`. La disponibilité de ce service, ses paramètres, ses modèles et ses conditions d'accès peuvent évoluer. Selon le fournisseur, une clé API, un compte ou des crédits peuvent être nécessaires. Le code ne garantit pas un accès gratuit ou illimité.

Pour une utilisation publique ou professionnelle, branchez un fournisseur officiellement documenté et utilisez un backend (proxy serveur) pour protéger la clé API. Ne placez jamais une clé secrète dans le code public du navigateur.

## Limites de cette première version
- La galerie est conservée uniquement dans la page ouverte (pas de compte ni de base de données).
- La génération dépend du service externe et de ses règles.
- Les options de modèles sont indicatives et doivent être adaptées au fournisseur réellement utilisé.
