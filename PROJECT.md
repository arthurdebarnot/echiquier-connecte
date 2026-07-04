## Echiquier Physique.

### Pièces.

Bien que de nombreux modèles de pièces d'échecs existent sur internet, nous avons préféré créer nos modèles nous même afin d'avoir un jeu adapter à la taille de nos cases et à celles des aimants que nous esperions recevoir. Du fait de l'absence des aimants, nous avons dû utiliser celle du projet IDS de cette année.


### Structure du plateau.

Afin d'éviter que la LED d'une case n'en éclaire une autre, nous avons décidé de réaliser une grille coupant chaque cases de ses voisines. Seul un cercle bas dans le plateau permet aux cases de communiquer pour faire passer le ruban LED. 

La Grille a été réalisé grâce à la découpeuse laser, dont la précision permet un emboitement sans trop de jeu. Il y a un carré pour le bas. Chacune des 18 barres qui composent la grille sont tenus par 4 points à la plaque.

Le haut du plateau est une impression bicolore blanc-noir de 0.5mm, permettant de faire passer la lumière des LEDS. L'utilisation de PETG translucide pour mieux faire passer la lumière a été écarté sous les conseils de Némo.


### Capteurs.

En l'absence de capteurs reçus, nous avons récupéré le montage du trimestre IDS de cette année. Nous n'avons donc pas pu réellement modifier cette structure et avons donc plutôt adapter le reste du plateau à celle-ci. 

ll aurait fallut faire usage d'un multiplexeur pour permettre de sonder toutes les cases malgré le nombre d'inputs limité du Raspberry Pi. En l'absence de celui-ci, nous n'avons accès qu'à 48 cases (8 colonnes et seulement 6 lignes). La strucutre récupéré a posé pas mal de problèmes (capteurs cassés, nécessité de resouder plusieurs connexions, etc.).