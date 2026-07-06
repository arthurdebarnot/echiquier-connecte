## Echiquier Physique

### Pièces

Bien que de nombreux modèles de pièces d'échecs existent sur internet, nous avons préféré créer nos modèles nous même afin d'avoir un jeu adapter à la taille de nos cases et à celles des aimants que nous esperions recevoir. Du fait de l'absence des aimants, nous avons dû utiliser celle du projet IDS de cette année.


### Structure du plateau

Afin d'éviter que la LED d'une case n'en éclaire une autre, nous avons décidé de réaliser une grille coupant chaque cases de ses voisines. Seul un cercle bas dans le plateau permet aux cases de communiquer pour faire passer le ruban LED. 

La Grille a été réalisé grâce à la découpeuse laser, dont la précision permet un emboitement sans trop de jeu. Il y a un carré pour le bas. Chacune des 18 barres qui composent la grille sont tenus par 4 points à la plaque.

Le haut du plateau est une impression bicolore blanc-noir de 0.5mm, permettant de faire passer la lumière des LEDS. L'utilisation de PETG translucide pour mieux faire passer la lumière a été écarté sous les conseils de Némo.


### Capteurs

En l'absence de capteurs reçus, nous avons récupéré le montage du trimestre IDS de cette année. Nous n'avons donc pas pu réellement modifier cette structure et avons donc plutôt adapter le reste du plateau à celle-ci. 

ll aurait fallut faire usage d'un multiplexeur pour permettre de sonder toutes les cases malgré le nombre d'inputs limité du Raspberry Pi. En l'absence de celui-ci, nous n'avons accès qu'à 48 cases (8 colonnes et seulement 6 lignes). La strucutre récupéré a posé pas mal de problèmes (capteurs cassés, nécessité de resouder plusieurs connexions, etc.).

## Partie informatique

### Mission principale

Nous avons choisi d'utiliser le package python `chess.py` pour gérer ce qui révèle de la logique du jeu d'échecs en lui-même : légalité des coups, possibilité de réaliser une roque, etc. Notre défi était de donner, à partir des données des capteurs, les bonnes informations à `chess.py`. 

En effet, les capteurs nous indiquent seulement si il y a ou non une pièce sur une certaine case, mais n'en disent rien sur la nature de la pièce (que ce soit son rang ou son couleur). Il fallait ainsi construire une logique qui permet de passer de la "magnet-board" (grille de 1 et des 0 indiquant la présence ou non d'une pièce) à des coups compréhensibles par `chess.py`.

### Organisation du code

On a d'abord fait un prototype de code pour commencer réflechir à la structure du code. Cependant, il est vite devenu incompréhensible, et il fallait qu'on refasse tout de scratch pour avoir une architecture cohérente et robuste.

### Difficultés recontrées

Avoir une architecture de code cohérente et lisible était plus dur que prévu, il fallait réflechir en avance de comment on voulait structurer la logique et les interactions entre les différentes parties du code. 

Par ailleurs, la gestion des coups illégaux était un peu délicat : en effet, si `chess.py` détecte un mauvais coup, il réfuse de l'enregistrer. Mais physiquement parlant, la pièce a quand-même été déplacée, et il faut qu'on "dise au code" qu'il est "légal" de rebouger la pièce pour la remettre dans son position initial.

Une grande défi à surmonter était la gestion de la roque : de la point de vue du "magnet-board", c'est une situation très bizarre, puisqu'il voit 2 pièces de la même couleur soulevées, ce qui est normalement illégal. Il faut alors réussir à bien détecter ce qui se passe et basculer sur une autre système de gestion pour bien comprendre et enregistrer ce qui se passe sur l'échiquier.


## Lien physique - informatique

Malheureusement, en raison des difficultés du côté physique avec les capteurs, on n'a pas pu connecter les deux parties de notre projet. Avec un peu plus de temps, et surtout le matériel nécessaire, on aurait aimé faire le lien et compléter le projet.