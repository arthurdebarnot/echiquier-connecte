# Echiquier connecté

## Installation des packages

`conda env create -f environment-windows.yml`

## Fonctionnement du programme

### Cas de simulation sans le raspberry

Etant donné que nous n'avons pas eu accès aux capteurs nous avons beaucoup développé l'aspect simulation des inputs pour tester notre programme d'échecs.

Le fichier à exécuter est celui qui s'appelle [main.py](./main.py). Il est possible de modifier le FEN de départ. Une interface graphique s'ouvre et permet de visualiser la position des capteurs allumés, ainsi que la position des pièces enregistrée par l'ordinateur.

En cliquant sur les cases, on peut simuler l'allumage ou l'extinction d'un reed switch. Lorsque le programme détecte qu'un coup a été effectué (par exemple, soulèvement du pion en e2, puis posage sur pion en e4), il met à jour son échiquier interne et déplace la lettre du pion.

Le programme prend en charge le roque, la prise en passant, la promotion ainsi que les différentes façon de terminer la partie : échec et mat, pat, insuffisance de matériel, nulle par répétition, nulle par suite consécutive de 50 coups sans prise ni déplacement de pion.

#### Promotion

Lorsqu'un pion arrive sur la case de promotion, il faut le changer en une autre pièce. Pour indiquer quelle pièce on a choisi à l'ordinateur, nous avons décidé de demander au joueur de modifier l'état d'une case tampon.

![image des cases tampons](./images/promotion.png)

Si une pièce est posée sur la case tampon, la pièce doit être soulevée puis reposée. Si aucune pièce n'est sur la case tampon, une pièce doit être posée puis reprise.

---

**ATTENTION**
Il faut bien penser que quand le pion est promu, il doit être remplacé par une autre pièce, et donc pour que l'ordinateur valide la promotion, la case du pion doit être désactivée puis réactivée pour simuler ce changement de pièce.

---

#### Choix du FEN de départ

Il est possible de changer la position de départ en le précisant à l'aide d'un FEN. Il est possible de trouver le FEN d'une position à l'aide de ce [lien](https://www.chess.com/analysis)

#### Evaluation par stockfish des coups


L'intérêt de cet échiquier connecté est de pouvoir évaluer chaque coup et donner du "feedback" en temps réel aux jouers. Ceci se fait à travers un algorithme d'échecs, Stockfish. À chaque coup, l'état du jeu (représenté par le FEN) est envoyé à Stockfish, qui évalue la situation et renvoie une valeur (qu'on passe ensuite dans la fonction $\mathrm{argsinh}$ pour donner plus de valeur à des modification d'évaluation proche de 0). En le comparant avec la situation d'avant, on peut ainsi juger la pertinence du coup.


## Partie physique

### LED strip

Pour mieux communiquer des information importantes (coup illégal, "blunder", etc.) aux joueurs, une LED strip est mise sous l'échiquier et peut allumer chaque case de différentes couleurs (rouge, vert, orange, etc.). 

### Reed switch

Pour détecter la présence ou non d'une pièce, des reed switches sont mis sous chaque case et des aimants sont mis sous chaque pièce. Ainsi, lorsqu'une pièce est mise sur une case, le reed switch s'active et un courant circule. Il aurait fallut faire usage d'un multiplexeur pour permettre de sonder toutes les cases malgré le nombre d'inputs limité du Raspberry Pi. En l'absence de celui-ci, nous n'avons accès qu'à 48 cases (8 colonnes et seulement 6 lignes). Malheureusement, on n'a pas recu la commande de ces capteurs, et on a dû utiliser ceux du projet de l'année dernière, ce qui posait pas mal de problèmes (capteurs cassés, nécessité de resouder plusieurs connexions, etc.).

La lecture se fait grâce à [reedswitches-leds.py](./reedswitches-leds.py)

### Impression 3D
On a imprimé en 3D une échiquier fin (épaisseur 0.5mm) pour le mettre au-dessus du LED strip et des reed-switches, ainsi que des pièces avec un trou pour les aimants. Il fallait faire la conception des pièces nous-mêmes pour pouvoir bien mettre des aimants en-dessous. Malheureusement, nous n'avons jamais reçu les aimants, et nous avons dû faire recours aux pièces utilisées par le groupe de l'année précedente. 