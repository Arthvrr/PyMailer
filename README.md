# Gestionnaire d'emails pour les parents d'animés

Ce projet permet de gérer une base de données d'emails des parents d'animés via un site web simple. Il inclut les fonctionnalités suivantes :

- Ajouter un email via le site
- Supprimer un email de la liste
- Envoyer des emails à toute la base de données en quelques clics

## Technologies utilisées

- **Front-end** : GitHub Pages pour héberger le site et rendre le formulaire interactif via `index.html`
- **Back-end** : Flask pour gérer les requêtes, la base de données et l'envoi d'emails, et

## Fonctionnalités

### 1. Ajouter un email via le site
Les utilisateurs peuvent entrer leur email via un formulaire sur le site GitHub Pages. L'email sera ajouté à une base de données SQLite.

### 2. Supprimer un email de la liste
Il est possible de supprimer un email de la liste via une simple interface de suppression.

### 3. Envoyer des emails à toute la base de données
Un script Python permet d'envoyer un email à **tous** les utilisateurs enregistrés dans la base de données en une seule commande.

## Mode Opératoire

### Étape 1 : Écrire le contenu du mail
Écrivez le contenu de votre email dans un fichier texte nommé `message.txt`. Ce fichier contiendra le sujet et le corps de votre message.

### Étape 2 : Envoyer l'email à toute la base de données
Une fois le fichier `message.txt` prêt, vous pouvez envoyer l'email à tous les utilisateurs inscrits. Pour cela, ouvrez un terminal et exécutez la commande suivante :

```bash
python script.py "Objet de l'email"
```