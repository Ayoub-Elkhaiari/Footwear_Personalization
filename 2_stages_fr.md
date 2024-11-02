# Système de Suivi du Pied en Deux Étapes pour l’Essayage Virtuel de Chaussures

Ce document explique le flux de processus d'un système de suivi du pied en deux étapes pour aligner précisément les modèles de chaussures virtuels 3D avec le pied d'un utilisateur dans un environnement de réalité mixte. Le système utilise des données de profondeur et de couleur capturées par une caméra RGB-D et est divisé en deux étapes principales : **Étape 1 - Détection Initiale** et **Étape 2 - Suivi Précis**.

## Vue d'Ensemble des Entrées
- **Capture d'Image** : Une caméra RGB-D capture des données de couleur et de profondeur du pied de l'utilisateur.
  - **Données de Profondeur** : Fournit des informations 3D sur la forme et la position du pied.
  - **Données de Couleur** : Capture des informations de couleur, utiles pour la détection initiale des marqueurs.

## Étape 1 : Détection Initiale et Positionnement Approximatif
Dans la première étape, le système effectue une détection initiale et un alignement approximatif du modèle de chaussure virtuel avec le pied de l'utilisateur.

1. **Détection de Marqueurs** :
   - Utilise les données de couleur pour détecter des marqueurs spécifiques sur le pied. Ces marqueurs aident à localiser et identifier les points clés du pied.
   - Fournit une position et une orientation générales du pied pour un alignement approximatif.

2. **Positionnement Approximatif** :
   - Positionne le modèle de chaussure virtuel en ligne approximative avec le pied de l’utilisateur.
   - Affiche l'alignement approximatif en surimpression, fournissant un retour visuel immédiat.

## Étape 2 : Suivi Précis et Enregistrement 3D
La deuxième étape affine l'alignement à l'aide des données de profondeur pour un ajustement plus précis.

1. **Segmentation du Pied** :
   - Segmente le pied de l'utilisateur à l'aide des données de profondeur, l'isolant de l'arrière-plan pour un suivi précis.

2. **Enregistrement 3D avec ICP** :
   - Utilise l'algorithme ICP (Iterative Closest Point) pour aligner les données de profondeur du pied avec un modèle de pied de référence.
   - Affine l'alignement de la chaussure virtuelle en minimisant la distance entre les points réels du pied et le modèle virtuel.

3. **Algorithme de Découpage** :
   - Coupe le modèle de référence en fonction de l'angle de vue, réduisant la charge de calcul et améliorant l'efficacité.

4. **Résultat de Suivi Précédent** :
   - Utilise les données de suivi de la trame précédente pour assurer un suivi fluide, surtout en cas de mouvements rapides du pied.

## Résultat Final : Localisation du Pied
La localisation précise du pied est ensuite affichée avec un modèle de chaussure virtuel aligné avec précision, créant une expérience d'essayage virtuel réaliste et réactive.

---
