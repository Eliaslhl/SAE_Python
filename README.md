SAE Initiation au développement :

AMOUCHE Chamsedine TP Alpha et LAHLOUH Elias TP Beta.

Rendu final :

Le fichier UPEMTK,les images ainsi que le/les fichier txt 
pour les bonus sont dans le dossier.

Bonus implémentées :
	- Classement (Chamsedine)
	- Pause et Sauvegarde (Elias)

Organisation du programme :

	- 1re étape : moi et mon camarade avons lu en entier et analyser chaque étape du sujet.
	- 2ème étape : mettre en place un espace de travail convenable. On est aller sur le site github afin de partager notre avancée.
	- 3ème étape : Utiliser des noms de variables et des noms de fonctions explicite. (Avec les docstrings on a décrit ce que chaque fonction faisait).
	- 4ème étape : Coder le jeu de base
	- 5ème étape : Ajouter les variantes (Sablier : Elias ; Scores : Chamsedine ; Taille des boules : Chamsedine ; Version dynamique : Chamsedine ; Terminaison : Chamsedine ; Obstacles : Elias)
	- 6ème étape : Crée un menu pour choisir les variantes (Elias)
	- 7ème étape : Implémentation des bonus

Les choix techniques :
	
	- Jeu codé grâce au logiciel Visual Studio Code et Pycharm.
	- Mise en commun du code via github.
	- Liste, Matrice, Liste de tuples, Ensemble, Dictionnaires comme structure de données.
	- 2 Fichiers textes pour les bonus.
	- Mise en place d'une surface de jeu pour délimiter la zone jouable.
	- Mettre les input et les sorties directement dans la fenêtre pour un confort de jeu.

Problèmes rencontrées :
	- Trouver les formules pour pouvoir savoir si il y'a une intersection, ou pour savoir le centre du deuxième cercle à placer si il ya un clic dans une boule adverse ont été très compliqué à trouver et à comprendre.
	Merci à notre professeur, mr.Hubard qui nous a expliquer et grâce à ses explications nous avons réussi, bien tant que mal.
	- L'organisations des matrices pour les réutiliser fut subtil et pas explicite au début, après de longues heures de réflexion nous avons pu trouver la meilleure méthode selon nous qui est de enregistrer, pour chaque cercle, la position du centre ainsi que son rayon.
	- Problème si adversaire clique dans une intersection de 2 boules (si le joueur bleu a 2 boules qui s'intersectionnent et que le joueur rouge clique
	sur l'intersection, alors les 2 boules ne sont pas sub-diviser). En effet, malgré un temps non négligeable consacré à ce problème, nous n'avons pas encore trouver la solution.
	- Lors de l'implémentation de variantes et des bonus nous avons dû réorganiser notre code avec des changements considérables.

Informations pratiques :
  - Pour la variante score, appuyer sur la touche 's'.
  - Pour la variante terminaison, appuyer sur la touche 't'. Faisable qu'une fois par partie !
  - Pour le bonus Pause et Sauvegarde, appuyer sur la touche 'p'.

Autres :
	Malgré les soucis rencontrées, le jeu fonctionne très bien.
