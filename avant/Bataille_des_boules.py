#----------------------------- IMPORTS -------------------------#
import time
from random import randint
from upemtk import *
from math import *
import matplotlib
import os
#------------------------ FIN DES IMPORTS ---------------------#
#-------------------------- VARIABLES -------------------------#
rectanglePosAX = 200
rectanglePosAY = 200
rectanglePosBX = 800
rectanglePosBY = 800
# Ces 4 variables sont les coordonnées du rectangle qui servira de surface de jeu.

R = 50  # Initialisation du rayon de base d'un cercle

tourJoueur = 1
Emplacements = [] # Variable permettant d'initialiser la matrice qui permettra de vérifier si lorsqu'on place un cercle, il y a intersection avec un autre.
EmplacementsJoueur1 = []
EmplacementsJoueur2 = []
# Variables permettant d'initialiser les matrices qui seront utiliser afin de stocker les positions des cercles de chaque joueur.

Boules_bleu = []
Boules_rouge = []
# Variables permettant d'initialiser les matrices qui seront utiliser afin de stocker les cercles en tant "qu'objet" pour pouvoir les supprimer plus tard avec la fonction "remplace_boule()".

nbr_tout_s = 15  # nombre de secondes entre chaque tour pour la variable sablier

Budget1 = 450
Budget2 = 450
Budget = 0
# Variables pour la variante Taille des boules.

Liste_des_pixels = []
for i in range(200,801):
    for j in range(200,801):
        Liste_des_pixels.append((i,j,None))
#Initialise une matrice des pixels de la surface de jeu afin de savoir qui gagne.

compteur_terminaison = 0 #Permet de savoir si terminaison a déjà été utilisé, afin de pouvoir limiter son utilisation à 1 fois.
#------------------------ FIN DES VARIABLES -----------------------#
#-------------------------- FONCTIONS -----------------------------#
def menu():
    """Crée un menu pour jouer, quitter le jeu ou afficher le classement des joueurs.
    """
    ax = 250  # Permet de créer le premier bouton
    bx = 700
    ay = 350
    by = 450

    ax3 = 250  # Permet de créer le deuxième bouton
    bx3 = 700
    ay3 = 650
    by3 = 750
    
    ax2 = 250 # Permet de créer le troisième bouton
    bx2 = 700
    ay2 = 800
    by2 = 900
 
    ax4 = 250 # Permet de créer le quatrième bouton
    bx4 = 700
    ay4 = 500
    by4 = 600
    
    l1 = bx - ax  # On utlise cette formule pour centrer le texte dans les rectangles
    l2 = ay - by

    l1_1 = bx2 - ax2
    l2_2 = by2 - ay2
    
    l3 = bx3 - ax3
    l3_2 = by3 - ay3

    r1 = rectangle(0, 0, 1000, 1000, couleur='black', remplissage='black',tag='')  # Permet de mettre un fond de couleur
    image(500, 500, 'el.gif', ancrage='center') # Permet de mettre une image dans le menu
    r2 = rectangle(ax, ay, bx, by, couleur='white', remplissage='grey', epaisseur=5)  # Affichage premier bouton sous forme rectangulaire
    r3 = texte(ax + l1 / 2, by + l2 / 2, 'Jouer', couleur='black', ancrage='center', police="Purisa", taille=18, tag='')  # Permet d'écrire "Jouer" dans le premier rectangle
    r4 = rectangle(ax2, ay2, bx2, by2, couleur='white', remplissage='grey', epaisseur=5)  # Affichage deuxième bouton sous forme rectangulaire
    r5 = texte(ax2 + l1_1 / 2, ay2 + l2_2 / 2, 'Quitter', couleur='black', ancrage='center', police="Purisa", taille=18,tag='')  # Permet d'écrire "Quitter" dans le deuxième rectangle
    r6 = texte(ax2 + l1_1 / 2, 250, 'Bataille de boules', couleur='white', ancrage='center', police="Purisa", taille=50,tag='') 
    r7= rectangle(ax3, ay3, bx3, by3, couleur="white", remplissage='grey', epaisseur=5) # Affichage troisième bouton sous forme rectangulaire
    r8 = texte(ax3 + l3 / 2, ay3 + l3_2 / 2, 'Classement', couleur='black', ancrage='center', police="Purisa", taille=18,tag='') # Permet d'écrire "Classement" dans le deuxième rectangle
    r9 = rectangle(ax4, ay4, bx4, by4, couleur='white', remplissage='grey',epaisseur=5)  # Affichage quatrième bouton sous forme rectangulaire
    r10 = texte(ax + l1 / 2, by + 150 + l2 / 2, 'Charger', couleur='black', ancrage='center', police="Purisa", taille=18,tag='')  # Permet d'écrire "Charger" dans le premier rectangle
    jeu=0 # condition pour le attente clic
    while jeu == 0:
        x, y, t = attente_clic()
        if ax < x < bx and ay < y < by: #si le clic est dans le bouton jouer.
            jeu = 1
            efface(r1)
            efface(r2)
            efface(r3)
            efface(r4)
            efface(r5)
            efface(r6)
            efface(r7)
            efface(r8)
            efface(r9)
            efface(r10)
            return 1
        if ax2 < x < bx2 and ay2 < y < by2: #si le clic est dans le bouton quitter.
            return False
        if ax3 < x < bx3 and ay3 < y < by3: #si le clic est dans le bouton classement.
            efface(r1)
            efface(r2)
            efface(r3)
            efface(r4)
            efface(r5)
            efface(r6)
            efface(r7)
            efface(r8)
            efface(r9)
            efface(r10)
            return 2
        if ax4 < x < bx4 and ay4 < y < by4:
            efface(r1)
            efface(r2)
            efface(r3)
            efface(r4)
            efface(r5)
            efface(r6)
            efface(r7)
            efface(r8)
            efface(r9)
            efface(r10)
            return 3


def verifier_clic_boule(emplacementClic):
    """Permet de vérifier si l'utilisateur clique à l'intérieur d'une boule adverse.
    
    Arguments :
        emplacementClic : variable contenant l'abscisse, l'ordonnée et le type du clic de l'utilisateur.
    """
    x = emplacementClic[0]
    y = emplacementClic[1]
    lst = []
    EmplacementsJoueurAdversaire = []

    if tourJoueur == 1:
        EmplacementsJoueurAdversaire = EmplacementsJoueur2
    else:
        EmplacementsJoueurAdversaire = EmplacementsJoueur1

    f = True

    for Emplacement in EmplacementsJoueurAdversaire:
        if sqrt((Emplacement[0] - x) ** 2 + (Emplacement[1] - y) ** 2) <= Emplacement[2]:
            lst = [False, Emplacement[0], Emplacement[1]]
            return lst
        else:
            lst = [True, Emplacement[0], Emplacement[1]]
    return lst

def verifier_clic_boule2(emplacementClic, rayon, x, y):
    if sqrt((emplacementClic[0] - x) ** 2 + (emplacementClic[1] - y) ** 2) <= rayon:
        return True
    else:
        return False


def verifierIntersection(x, y, r, EmplacementJoueurAdv):
    """Permet de vérifier si, lors du placement d'une boule, il y a intersection avec une boule d'une autre couleur.
    
    Arguments :
        x : abscisse du clic de l'utilisateur.
        y : ordonnée du clic de l'utilisateur.
        r : rayon de la boule que l'utilisateur va placer.
        EmplacementJoueurAdv : Liste contenant l'emplacement (x,y,r) de toutes les boules adverses.
    """
    for i in range(len(EmplacementJoueurAdv)):
        xA = EmplacementJoueurAdv[i][0]
        yA = EmplacementJoueurAdv[i][1]
        rA = EmplacementJoueurAdv[i][2]

        if r + rA >= sqrt((x - xA)**2 + (y - yA)**2):
            return False
    return True


def verifierEmplacementClic(emplacementClic, rayon, ax, ay, bx, by):
    """Permet de resteindre le placement des boules uniquement au sein de la surface de jeu (Le rectangle).
    
    Arguments :
        emplacementClic : variable contenant l'abscisse, l'ordonnée et le type du clic de l'utilisateur.
        rayon : rayon de la boule que l'utilisateur va placer.
        ax : abscisse du premier point du rectangle.
        ay : ordonné du premier point du rectangle.
        bx : abscisse du second point du rectangle.
        by : ordonné du second point du rectangle.
    """
    x = emplacementClic[0]
    y = emplacementClic[1]
    positionX = ax + rayon < x < bx - rayon
    positionY = ay + rayon < y < by - rayon
    if positionY == True and positionX == True:
        return True
    else:
        return False


def dessiner_superficie():
    """Permet de créer la surface de jeu.
    """
    rectangle(rectanglePosAX, rectanglePosAY, rectanglePosBX, rectanglePosBY, couleur='black', remplissage='grey',epaisseur=10)
    mise_a_jour()



def remplacer_boule(emplacement, boule, lst, Clic, couleurBoule, Liste_des_pixels):
    """Permet d'effacer une boule si l'utilisateur adverse clique dessus, pour laisser de la place afin de la remplacer par 2 boules plus petites.
    
    Arguments :
        emplacement : Liste contenant l'emplacement (x,y,r) de toutes les boules adverses.
        boule : Liste des boules dessinées de l'adversaire.
        lst : Liste de tuples contenant True ou False, l'abscisse et l'ordonnée des boules adverses.
        Clic : variable contenant l'abscisse, l'ordonnée et le type du clic de l'utilisateur.
        couleurBoule : Couleur de la boule de l'adversaire
        Liste_des_pixels : Liste de couples où tous les pixels du jeu sont enregistrés.
    """
    # Etape1 supprimer l'ancienne boule :
    for i in range(len(emplacement)):
        # Sert à savoir quelle boule supprimer
        if emplacement[i][0] == lst[1] and emplacement[i][1] == lst[2]:
            compteur = i
            x = emplacement[i][0]
            y = emplacement[i][1]
            r = emplacement[i][2]
            a = Clic[0]
            b = Clic[1]
            if (sqrt(((a - x) ** 2) + ((b - y) ** 2))) == 0:
                break
            else:
                efface(boule[compteur])
                # Etape2 Placer les 2 boules :
                # rayon du plus petit cercle (1er cercle)
                r1 = r - (sqrt((((x - a) ** 2) + ((y - b) ** 2))))
                r2 = r - r1  # rayon du deuxième cercle
                s = r - (2 * r1)
                t = s - r2
                va = (a - x) / (sqrt(((a - x) ** 2) + ((b - y) ** 2)))
                vb = (b - y) / (sqrt(((a - x) ** 2) + ((b - y) ** 2)))
                c = x + (t * va)
                d = y + (t * vb)

                boule1 = cercle(a, b, r1, couleur=couleurBoule, remplissage=couleurBoule, epaisseur=1)
                boule2 = cercle(c, d, r2, couleur=couleurBoule, remplissage=couleurBoule, epaisseur=1)
                # Etape 3 supprimer dans la liste d'emplacement l'ancien cercle, et y ajouter les 2 nouveaux cercles.
                emplacement.pop(i)
                emplacement.append([a, b, r1])
                emplacement.append([c, d, r2])
                # Etape 4 supprimer dans la liste des boules, l'ancienne boule et y ajouter les 2 nouvelles boules.
                boule.pop(i)
                boule.append(boule1)
                boule.append(boule2)
                #Etape 5 supprimer les pixels qui ne sont plus présent et affecter les nouveaux pixels.
                Liste_des_pixels=supprimer_pixel(Liste_des_pixels, x, y, r)
                Liste_des_pixels=affecter_pixel(Liste_des_pixels, a, b, r1, couleurBoule)
                Liste_des_pixels=affecter_pixel(Liste_des_pixels, c, d, r2, couleurBoule)


def calculer_resultat(Liste_des_pixels,couleurJoueur1,couleurJoueur2):
    """Permet de calculer le score (le nombre de pixels) des joueurs.
    
    Arguments : 
        Liste_des_pixels : Liste de couples où tous les pixels du jeu sont enregistrés.
        couleurJoueur1 : couleur du joueur1
        couleurJoueur2 : couleur du joueur2
    """
    compteur_joueur1=0
    compteur_joueur2=0
    for elements in Liste_des_pixels:
        if elements[2]==couleurJoueur1:
            compteur_joueur1+=1
        elif elements[2]==couleurJoueur2:
            compteur_joueur2+=1
    return (compteur_joueur1, compteur_joueur2)


def affecter_pixel(Liste_des_pixels,x,y,r,couleurJoueur):
    """Fonction permettant d'affecter un/des pixel à un joueur.

    Arguments:
        Liste_des_pixels : Liste de couples où tous les pixels du jeu sont enregistrés.
        x : abscisse de la boule posée.
        y : ordonnée de la boule posée.
        r : rayon de la boule posée.
        couleurJoueur : couleur du joueur qui se voit affecter un pixel.
    """
    for i in range(len(Liste_des_pixels)):
        x2=Liste_des_pixels[i][0]
        y2=Liste_des_pixels[i][1]
        if ((x2-x)<=r and (x2-x)>=0) and ((y2-y)<=r and (y2-y)>=0):
            Liste_des_pixels[i]=(x2,y2,couleurJoueur)
            
    return Liste_des_pixels


def supprimer_pixel(Liste_des_pixels, x, y, r):
    """Fonction permettant de supprimer un/des pixel à un joueur.

    Arguments:
        Liste_des_pixels : Liste de couples où tous les pixels du jeu sont enregistrés.
        x : abscisse de la boule posée.
        y : ordonnée de la boule posée.
        r : rayon de la boule posée.
    """
    for i in range(len(Liste_des_pixels)):
        x2=Liste_des_pixels[i][0]
        y2=Liste_des_pixels[i][1]
        if ((x2-x)<=r and (x2-x)>=0) and ((y2-y)<=r and (y2-y)>=0):
            if Liste_des_pixels[i][2]:
                Liste_des_pixels[i]=(x2,y2,None)
            
    return Liste_des_pixels
    

def timer(compteur=nbr_tout_s, nbTour=0):
    """Fonction permettant de mettre en place un sablier pour que chaque utilisateurs ait un temps précis pour jouer. (Variante sablier)

    Args:
        compteur : variable contenant le nombre de secondes entre chaque tour.
        nbTour : variable contenant 0.
    """
    global nbr_tout_s, customCanvas, texte_compteur, nbTourReel

    if nbTourReel == nbTour:
        if texte_compteur != '':
            efface(texte_compteur)
        compteur -= 1
        if compteur == 0:
            nextTour()
            return

        customCanvas.canvas.after(1000, timer, compteur, nbTour)
        txt = "Temps restant : " + str(compteur) + "sec"
        texte_compteur = texte(0, 0, txt, couleur="white")
    return False


def nextTour():
    """Fonction permettant de fixer la variable pasDeClic à True. (en lien avec la fonction timer())
    """
    global customCanvas, pasDeClic
    pasDeClic = True
    customCanvas.canvas.event_generate('<Button-1>')


def Obstacles(nb_obstacle):
    """Fonction permettant de créer des obstacles.

    Arguments:
        nb_obstacle : variable contenant le nombre d'obstacles à placer.
    """
    obst_a = []
    obst_b = []

    for i in range(nb_obstacle):
        a = randint(200 + 50, 800 - 50)
        b = randint(200 + 50, 800 - 50)
        cercle(a, b, 30, 'black', 'black', 1, "obstacles")
        obst_a.append(a)
        obst_b.append(b)

    return obst_a, obst_b


def inter_obstacle(x, y, r, obst_a, obst_b):
    """Fonction permettant de vérifier si lorsque l'on place une boule elle n'est pas en intersection avec des obstacles.
    
    Arguments : 
        x : abscisse de la boule posée.
        y : ordonnée de la boule posée.
        r : rayon de la boule posée.
        obst_a : Liste contenant les abscisses des obstacles.
        obst_b : Liste contenant les ordonnées des obstacles.
    """
    for i in range(len(obst_a)):
        if sqrt((x - obst_a[i]) ** 2 + (y - obst_b[i]) ** 2) < (r + 30):
            return False

    return True


def Scores(couleur_joueur1, couleur_joueur2, Liste_des_pixels):
    """Fonction permettant de calculer le score actuel des 2 joueurs, puis de l'afficher pendant 2 secondes. (Variante)
    
    Arguments :
        couleur_joueur1 : couleur du joueur1.
        couleur_joueur2 : couleur du joueur2.
        Liste_des_pixels : Liste de couples où tous les pixels du jeu sont enregistrés.
    """
    compteur = 0
    resultat=calculer_resultat(Liste_des_pixels,couleur_joueur1, couleur_joueur2)
    score_bleu=resultat[0]
    score_rouge=resultat[1]
    sb = texte(50, 50, "score joueur 1 : " +
               str(score_bleu), couleur=couleur_joueur1)
    sr = texte(50, 100, "score joueur 2 : " +
               str(score_rouge), couleur=couleur_joueur2)

    mise_a_jour()

    while compteur != 2:
        time.sleep(1)
        mise_a_jour()
        compteur += 1

    efface(sb)
    efface(sr)


def bouton_jeu(couleur_joueur1, couleur_joueur2):
    """Fonction permettant de créer les boutons pour pouvoir choisir les variantes que l'on veut (en lien avec la fonction variante()).

    Args:
        couleur_joueur1 : couleur du joueur 1.
        couleur_joueur2 : couleur du joueur 2.
    """
    cercle_1 = cercle(200, 200, 70, couleur=couleur_joueur1,
                      remplissage=couleur_joueur1, epaisseur=10, tag='')
    txt_1 = texte(200, 200, "Sablier", couleur='black',
                  ancrage='center', police="Purisa", taille=20, tag='')

    cercle_2 = cercle(500, 200, 70, couleur=couleur_joueur2,
                      remplissage=couleur_joueur2, epaisseur=10, tag='')
    txt_2 = texte(500, 200, "Obstacle", couleur='black',
                  ancrage='center', police="Purisa", taille=20, tag='')

    cercle_3 = cercle(800, 200, 70, couleur=couleur_joueur1,
                      remplissage=couleur_joueur1, epaisseur=10, tag='')
    txt_3 = texte(800, 200, "Score", couleur='black',
                  ancrage='center', police="Purisa", taille=20, tag='')

    cercle_4 = cercle(200, 500, 70, couleur=couleur_joueur2,
                      remplissage=couleur_joueur2, epaisseur=10, tag='')
    txt_4 = texte(200, 500, "Taille_boules", couleur='black',
                  ancrage='center', police="Purisa", taille=17, tag='')

    cercle_5 = cercle(500, 500, 70, couleur=couleur_joueur1,
                      remplissage=couleur_joueur1, epaisseur=10, tag='')
    txt_5 = texte(500, 500, "Dynamique", couleur='black',
                  ancrage='center', police="Purisa", taille=19, tag='')

    cercle_6 = cercle(800, 500, 70, couleur=couleur_joueur2,
                      remplissage=couleur_joueur2, epaisseur=10, tag='')
    txt_6 = texte(800, 500, "Terminaison", couleur='black',
                  ancrage='center', police="Purisa", taille=17, tag='')

    lst = [200, 500, 800, 200, 500, 800]
    lst2 = [200, 200, 200, 500, 500, 500]
    lst_cercle = [cercle_1, cercle_2, cercle_3, cercle_4, cercle_5, cercle_6]
    lst_txt = [txt_1, txt_2, txt_3, txt_4, txt_5, txt_6]
    lst_3 = ['Sablier', 'Obstacle', 'Score','Taille_boules', 'Dynamique', 'Terminaison']
    lst_4 = [['blue', couleur_joueur1], [couleur_joueur2, 'white']]
    return lst, lst2, lst_cercle, lst_txt, lst_3, lst_4


def bouton_desactive(x, y, c, txt, noms, couleur):
    """Fonction permettant de désactiver un bouton (en lien avec la fonction variante()).

    Args:
        x : abscisse du bouton que l'on veut désactiver.
        y : ordonnée du bouton que l'on veut désactiver.
        c : cercle visée.
        txt : texte du cercle visée.
        noms : nom de la variante.
        couleur : couleur du bouton.
    """
    efface(c)
    c2 = cercle(x, y, 70, couleur[0], remplissage=couleur[1], epaisseur=10, tag='')
    efface(txt)
    txt2 = texte(x, y, noms, couleur='black', ancrage='center', police='Purisa', taille=17, tag='')
    mise_a_jour()

    return c2, txt2


def bouton_active(x, y, c, txt, noms):
    """Fonction permettant de désactiver un bouton (en lien avec la fonction variante()).

    Args:
        x : abscisse du bouton que l'on veut activer.
        y : ordonnée du bouton que l'on veut activer.
        c : cercle visée.
        txt : texte du cercle visée.
        noms : nom de la variante.
    """
    efface(c)
    c3 = cercle(x, y, 70, couleur='grey', remplissage='white', epaisseur=10, tag='')
    efface(txt)
    txt3 = texte(x, y, noms, couleur='black', ancrage='center', police='Purisa', taille=17, tag='')
    mise_a_jour()

    return c3, txt3


def variante():
    """Fonction permettant de créer un menu pour pouvoir sélectionner les variantes que l'on veut.
    """
    efface_tout()
    mise_a_jour()
    sablier = False
    obstacles = False
    score = False
    taille_boules = False
    dynamique = False
    terminaison = False

    rectangle(0, 0, 1000, 1000, remplissage="lightgrey")
    image(530, 350, 'ok.png', ancrage='center')
    x_play, y_play, r_play = bouton_play()
    lst, lst2, lst_cercle, lst_txt, lst_3, lst_4 = bouton_jeu(couleur_joueur1, couleur_joueur2)
    while True:
        mise_a_jour()
        x, y, t = attente_clic()
        if sqrt((x - x_play) ** 2 + (y - y_play) ** 2) <= r_play:
            return sablier, obstacles, score, taille_boules, dynamique, terminaison
        for c in range(len(lst_cercle)):
            if c % 2 == 0:
                couleur = lst_4[0]
            else:
                couleur = lst_4[1]
            hy = sqrt((x - lst[c]) ** 2 + (y - lst2[c]) ** 2)
            if hy <= 70:
                if c == 0:
                    if t == "ClicGauche":
                        c5, txt5 = bouton_active(lst[c], lst2[c], lst_cercle[c], lst_txt[c], lst_3[c])
                        lst_cercle.pop(c)
                        lst_txt.pop(c)
                        lst_cercle.insert(c, c5)
                        lst_txt.insert(c, txt5)
                        sablier = True
                    if t == "ClicDroit":
                        c5, txt5 = bouton_desactive(lst[c], lst2[c], lst_cercle[c], lst_txt[c], lst_3[c], couleur)
                        lst_cercle.pop(c)
                        lst_txt.pop(c)
                        lst_cercle.insert(c, c5)
                        lst_txt.insert(c, txt5)
                        sablier = False
                if c == 1:
                    if t == "ClicGauche":
                        c5, txt5 = bouton_active(
                            lst[c], lst2[c], lst_cercle[c], lst_txt[c], lst_3[c])
                        lst_cercle.pop(c)
                        lst_txt.pop(c)
                        lst_cercle.insert(c, c5)
                        lst_txt.insert(c, txt5)
                        obstacles = True
                    if t == "ClicDroit":
                        c5, txt5 = bouton_desactive(
                            lst[c], lst2[c], lst_cercle[c], lst_txt[c], lst_3[c], couleur)
                        lst_cercle.pop(c)
                        lst_txt.pop(c)
                        lst_cercle.insert(c, c5)
                        lst_txt.insert(c, txt5)
                        obstacles = False
                if c == 2:
                    if t == "ClicGauche":
                        c5, txt5 = bouton_active(
                            lst[c], lst2[c], lst_cercle[c], lst_txt[c], lst_3[c])
                        lst_cercle.pop(c)
                        lst_txt.pop(c)
                        lst_cercle.insert(c, c5)
                        lst_txt.insert(c, txt5)
                        score = True
                    if t == "ClicDroit":
                        c5, txt5 = bouton_desactive(
                            lst[c], lst2[c], lst_cercle[c], lst_txt[c], lst_3[c], couleur)
                        lst_cercle.pop(c)
                        lst_txt.pop(c)
                        lst_cercle.insert(c, c5)
                        lst_txt.insert(c, txt5)
                        score = False
                if c == 3:
                    if t == "ClicGauche":
                        c5, txt5 = bouton_active(
                            lst[c], lst2[c], lst_cercle[c], lst_txt[c], lst_3[c])
                        lst_cercle.pop(c)
                        lst_txt.pop(c)
                        lst_cercle.insert(c, c5)
                        lst_txt.insert(c, txt5)
                        taille_boules = True
                    if t == "ClicDroit":
                        c5, txt5 = bouton_desactive(
                            lst[c], lst2[c], lst_cercle[c], lst_txt[c], lst_3[c], couleur)
                        lst_cercle.pop(c)
                        lst_txt.pop(c)
                        lst_cercle.insert(c, c5)
                        lst_txt.insert(c, txt5)
                        taille_boules = False
                if c == 4:
                    if t == "ClicGauche":
                        c5, txt5 = bouton_active(
                            lst[c], lst2[c], lst_cercle[c], lst_txt[c], lst_3[c])
                        lst_cercle.pop(c)
                        lst_txt.pop(c)
                        lst_cercle.insert(c, c5)
                        lst_txt.insert(c, txt5)
                        dynamique = True
                    if t == "ClicDroit":
                        c5, txt5 = bouton_desactive(
                            lst[c], lst2[c], lst_cercle[c], lst_txt[c], lst_3[c], couleur)
                        lst_cercle.pop(c)
                        lst_txt.pop(c)
                        lst_cercle.insert(c, c5)
                        lst_txt.insert(c, txt5)
                        dynamique = False
                if c == 5:
                    if t == "ClicGauche":
                        c5, txt5 = bouton_active(
                            lst[c], lst2[c], lst_cercle[c], lst_txt[c], lst_3[c])
                        lst_cercle.pop(c)
                        lst_txt.pop(c)
                        lst_cercle.insert(c, c5)
                        lst_txt.insert(c, txt5)
                        terminaison = True
                    if t == "ClicDroit":
                        c5, txt5 = bouton_desactive(
                            lst[c], lst2[c], lst_cercle[c], lst_txt[c], lst_3[c], couleur)
                        lst_cercle.pop(c)
                        lst_txt.pop(c)
                        lst_cercle.insert(c, c5)
                        lst_txt.insert(c, txt5)
                        terminaison = False


def bouton_play():
    """Fonction permettant de créer un bouton "jouer".
    """
    x = 800
    y = 700
    r = 70

    cercle(x, y, r, couleur='#32CD99', remplissage='#70DB93', epaisseur=10, tag='')
    texte(x, y, "Jouer", couleur='black', ancrage='center', police="Purisa", taille=18, tag='')
    mise_a_jour()

    return x, y, r


def Terminaisons():
    """Fonction permettant de fixer le nombre de tour restant à 5. (Variante)
    """
    txt_terminaison = texte(100, 100, "Terminaison dans : 5 tours", couleur="white")
    compteur = 0
    mise_a_jour()
    while compteur != 1:
        time.sleep(1)
        mise_a_jour()
        compteur += 1
    efface(txt_terminaison)
    return 5


def Dynamique_obstacle(EmplacementsJoueur1, EmplacementsJoueur2, obst_a, obst_b, couleur_joueur1, couleur_joueur2):
    """Fonction permettant d'augmenter le rayon de tous les cercles à la fin du tour même si la variante Obstacles est active. (Variante)

    Arguments:
        EmplacementsJoueur1 : Emplacemments des boules du joueur 1.
        EmplacementsJoueur2 : Emplacemments des boules du joueur 2.
        obst_a : Liste contenant les abscisses des obstacles.
        obst_b : Liste contenant les ordonnées des obstacles
        couleur_joueur1 : couleur du joueur 1.
        couleur_joueur2 : couleur du joueur 2.
    """
    if len(EmplacementsJoueur1) != 0:
        for i in range(len(EmplacementsJoueur1)):
            EmplacementsJoueurAdversaire = EmplacementsJoueur2
            couleurBoule = couleur_joueur1
            x_bd = EmplacementsJoueur1[i][0]
            y_bd = EmplacementsJoueur1[i][1]
            rayon_bd = (EmplacementsJoueur1[i][2]+5)
            if verifierEmplacementClic([x_bd, y_bd], rayon_bd, rectanglePosAX, rectanglePosAY, rectanglePosBX, rectanglePosBY):
                if verifierIntersection(x_bd, y_bd, rayon_bd, EmplacementsJoueurAdversaire) and inter_obstacle(x_bd, y_bd, rayon_bd, obst_a, obst_b):
                    efface(Boules_bleu[i])
                    Boules_bleu.pop(i)
                    boule_bd = cercle(
                        x_bd, y_bd, rayon_bd, couleur=couleurBoule, remplissage=couleurBoule, epaisseur=1)
                    Boules_bleu.append(boule_bd)
                    EmplacementsJoueur1.pop(i)
                    EmplacementsJoueur1.append([x_bd, y_bd, rayon_bd])
    if len(EmplacementsJoueur2) != 0:
        for i in range(len(EmplacementsJoueur2)):
            EmplacementsJoueurAdversaire = EmplacementsJoueur1
            couleurBoule = couleur_joueur2
            x_bd2 = EmplacementsJoueur2[i][0]
            y_bd2 = EmplacementsJoueur2[i][1]
            rayon_bd2 = (EmplacementsJoueur2[i][2]+5)
            if verifierEmplacementClic([x_bd2, y_bd2], rayon_bd2, rectanglePosAX, rectanglePosAY, rectanglePosBX, rectanglePosBY):
                if verifierIntersection(x_bd2, y_bd2, rayon_bd2, EmplacementsJoueurAdversaire) and inter_obstacle(x_bd2, y_bd2, rayon_bd2, obst_a, obst_b):
                    efface(Boules_rouge[i])
                    Boules_rouge.pop(i)
                    boule_bd2 = cercle(
                        x_bd2, y_bd2, rayon_bd2, couleur=couleurBoule, remplissage=couleurBoule, epaisseur=1)
                    Boules_rouge.append(boule_bd2)
                    EmplacementsJoueur2.pop(i)
                    EmplacementsJoueur2.append([x_bd2, y_bd2, rayon_bd2])


def Dynamique(EmplacementsJoueur1, EmplacementsJoueur2, couleur_joueur1, couleur_joueur2):
    """Fonction permettant d'augmenter le rayon de tous les cercles à la fin du tour. (Variante)

    Arguments:
        EmplacementsJoueur1 : Emplacemments des boules du joueur 1.
        EmplacementsJoueur2 : Emplacemments des boules du joueur 2.
        couleur_joueur1 : couleur du joueur 1.
        couleur_joueur2 : couleur du joueur 2.
    """
    if len(EmplacementsJoueur1) != 0:
        for i in range(len(EmplacementsJoueur1)):
            EmplacementsJoueurAdversaire = EmplacementsJoueur2
            couleurBoule = couleur_joueur1
            x_bd = EmplacementsJoueur1[i][0]
            y_bd = EmplacementsJoueur1[i][1]
            rayon_bd = (EmplacementsJoueur1[i][2]+5)
            if verifierEmplacementClic([x_bd, y_bd], rayon_bd, rectanglePosAX, rectanglePosAY, rectanglePosBX, rectanglePosBY):
                if verifierIntersection(x_bd, y_bd, rayon_bd, EmplacementsJoueurAdversaire):
                    efface(Boules_bleu[i])
                    Boules_bleu.pop(i)
                    boule_bd = cercle(
                        x_bd, y_bd, rayon_bd, couleur=couleurBoule, remplissage=couleurBoule, epaisseur=1)
                    Boules_bleu.append(boule_bd)
                    EmplacementsJoueur1.pop(i)
                    EmplacementsJoueur1.append([x_bd, y_bd, rayon_bd])
    if len(EmplacementsJoueur2) != 0:
        for i in range(len(EmplacementsJoueur2)):
            EmplacementsJoueurAdversaire = EmplacementsJoueur1
            couleurBoule = couleur_joueur2
            x_bd2 = EmplacementsJoueur2[i][0]
            y_bd2 = EmplacementsJoueur2[i][1]
            rayon_bd2 = (EmplacementsJoueur2[i][2]+5)
            if verifierEmplacementClic([x_bd2, y_bd2], rayon_bd2, rectanglePosAX, rectanglePosAY, rectanglePosBX, rectanglePosBY):
                if verifierIntersection(x_bd2, y_bd2, rayon_bd2, EmplacementsJoueurAdversaire):
                    efface(Boules_rouge[i])
                    Boules_rouge.pop(i)
                    boule_bd2 = cercle(
                        x_bd2, y_bd2, rayon_bd2, couleur=couleurBoule, remplissage=couleurBoule, epaisseur=1)
                    Boules_rouge.append(boule_bd2)
                    EmplacementsJoueur2.pop(i)
                    EmplacementsJoueur2.append([x_bd2, y_bd2, rayon_bd2])


def Accueil(LargeurFenetre):
    """
    Permet de creer l'écran d'accueil du jeu.
    
    Arguments :
        LargeurFenetre : Largeur de la fenêtre de jeu
    """
    polygone([(400, 480), (400, 520), (425, 500)], remplissage='White')
    polygone([(110, 480), (110, 520), (85, 500)], remplissage='White')

    polygone([(590, 480), (590, 520), (565, 500)], remplissage='White')
    polygone([(895, 480), (895, 520), (920, 500)], remplissage='White')

    lst_col = [cname for cname, hex in matplotlib.colors.cnames.items() if cname != "rebeccapurple"]

    i = 9
    j = 119

    texte(LargeurFenetre / 2 - 50, 100, "Bataille d             ",taille=50, ancrage="center", couleur=lst_col[i])
    texte(LargeurFenetre / 2 - 50, 100, "               e Boules",taille=50, ancrage="center", couleur=lst_col[j])
    cercle(250, 500, 70, remplissage=str(lst_col[i]))
    cercle(750, 500, 70, remplissage=str(lst_col[j]))
    cercle(500, 350, 70, remplissage='#27cc75')
    texte(500, 350, 'Continuer', ancrage='center', police="Purisa", taille=18,tag='')
    while True:
        x1, y1, type_clique = attente_clic()
        if verifierEmplacementClic((x1, y1), 0, 400, 480, 425, 520):
            if i == len(lst_col) - 1:
                i = 0
            else:
                i += 1

        if verifierEmplacementClic((x1, y1), 0, 85, 480, 110, 520):
            if i == 0:
                i = len(lst_col) - 1
            else:
                i -= 1

        if verifierEmplacementClic((x1, y1), 0, 565, 480, 590, 520):
            if j == len(lst_col) - 1:
                j = 0
            else:
                j += 1

        if verifierEmplacementClic((x1, y1), 0, 895, 480, 920, 520):
            if j == 0:
                j = len(lst_col) - 1
            else:
                j -= 1
        if verifier_clic_boule2((x1,y1), 70, 500, 350):
            efface_tout()
            texte(LargeurFenetre / 2 - 50, 100, "Bataille d             ",
                  taille=50, ancrage="center", couleur=lst_col[i])
            texte(LargeurFenetre / 2 - 50, 100, "               e Boules",
                  taille=50, ancrage="center", couleur=lst_col[j])
            return lst_col[i], lst_col[j]
            break

        if i == j:
            if i == 0:
                j = len(lst_col) - 1
            elif i == len(lst_col) - 1:
                j = len(lst_col) - 2
            else:
                i += 1
        cercle(250, 500, 70, remplissage=str(lst_col[i]))
        texte(LargeurFenetre / 2 - 50, 100, "Bataille d             ",
              taille=50, ancrage="center", couleur=lst_col[i])
        cercle(750, 500, 70, remplissage=str(lst_col[j]))
        texte(LargeurFenetre / 2 - 50, 100, "               e Boules",
              taille=50, ancrage="center", couleur=lst_col[j])


def pseudo():
    """Fonction permettant aux utilisateurs de rentrer leur pseudo pour jouer.
    """
    rectangle_pseudo=rectangle(100,400,900,600,couleur='black', remplissage='white',epaisseur=10)
    texte_pseudo=texte(110,410,"Joueur1, veuillez entrer un pseudo (max 25 lettres):", couleur="black", taille=18)
    mise_a_jour()
    compteur_touche_pseudo=1
    pseudo1=''
    pseudo2=''
    touche_pseudo=attente_touche()
    while touche_pseudo != 'Return':  #Pseudo1
        if touche_pseudo == 'BackSpace' and compteur_touche_pseudo > 1:
                pseudo1=pseudo1[:-1]
                compteur_touche_pseudo-=1
                efface(txt_pseudo)
                txt_pseudo=texte(500,510,str(pseudo1),couleur='black', ancrage='center')
                
        if touche_pseudo in ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'] and compteur_touche_pseudo < 26:
            if compteur_touche_pseudo==1:
                pseudo1+=str(touche_pseudo)
                txt_pseudo=texte(500,510,str(pseudo1),couleur='black', ancrage='center')
                compteur_touche_pseudo+=1
            else:
                pseudo1+=str(touche_pseudo)
                efface(txt_pseudo)
                txt_pseudo=texte(500,510,str(pseudo1),couleur='black', ancrage='center')
                compteur_touche_pseudo+=1
                
        mise_a_jour()
        touche_pseudo = attente_touche()
    
    efface(texte_pseudo)
    efface(txt_pseudo)
    compteur_touche_pseudo=1
    texte_pseudo=texte(110,410,"Joueur2, veuillez entrer un pseudo (max 25 lettres):", couleur="black",taille=18)
    mise_a_jour()
    touche_pseudo = attente_touche()
    while touche_pseudo != 'Return': #Pseudo2
        if touche_pseudo == 'BackSpace' and compteur_touche_pseudo > 1:
                pseudo2=pseudo2[:-1]
                compteur_touche_pseudo-=1
                efface(txt_pseudo)
                txt_pseudo=texte(500,510,str(pseudo2),couleur='black', ancrage='center')
                
        if touche_pseudo in ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'] and compteur_touche_pseudo < 26:
            if compteur_touche_pseudo==1:
                pseudo2+=str(touche_pseudo)
                txt_pseudo=texte(500,510,str(pseudo2),couleur='black', ancrage='center')
                compteur_touche_pseudo+=1
            else:
                pseudo2+=str(touche_pseudo)
                efface(txt_pseudo)
                txt_pseudo=texte(500,510,str(pseudo2),couleur='black', ancrage='center')
                compteur_touche_pseudo+=1
                
        mise_a_jour()
        touche_pseudo = attente_touche()
    
    return (pseudo1, pseudo2)
    

def Classement():
    """Fonction permettant d'afficher le classement des 3 meilleurs joueurs ayant joué au jeu. (BONUS)
    """
    ax2 = 250
    bx2 = 700
    l1_1 = bx2 - ax2
    image(500, 500, 'el.gif', ancrage='center')
    classement_txt=texte(ax2 + l1_1 / 2, 250, 'Bataille de boules', couleur='white', ancrage='center', police="Purisa", taille=50,tag='')
    classement_txt2=texte(ax2 + l1_1 / 2, 320, 'Classement', couleur='white', ancrage='center', police="Purisa", taille=50,tag='')
    f1=open('Classement.txt')
    lst_vainqueur=f1.readlines()
    f1.close()
    
    if lst_vainqueur==[]:
        txt_0=texte(ax2 + l1_1 / 2, 520, 'Pas de joueurs enregistré !', couleur='white', ancrage='center', police="Purisa", taille=18,tag='')
        ax = 250  # Permet de créer le premier bouton dont les valeurs
        bx = 700
        ay = 850
        by = 950
        z1= bx - ax
        z2= by - ay
        bouton_quitter = rectangle(ax, ay, bx, by, couleur='white', remplissage='grey', epaisseur=5)
        txt_quitter = texte(ax + z1 / 2, ay + z2 / 2, 'Retour', couleur='black', ancrage='center', police="Purisa", taille=18,tag='')
        mise_a_jour()
        retour=0
        while retour == 0:
            x, y, t = attente_clic()
            if ax < x < bx and ay < y < by:
                retour=1
    elif len(lst_vainqueur) == 1:
        Liste_classement=[]
        for lignes in lst_vainqueur:
            chaine_auxilaire=''
            points=''
            for caracteres in lignes:
                if caracteres != ';' and caracteres not in ['0','1','2','3','4','5','6','7','8','9']:
                    chaine_auxilaire+=caracteres
                elif caracteres != ';' and caracteres in ['0','1','2','3','4','5','6','7','8','9']:
                    points+=caracteres
            Liste_classement.append((chaine_auxilaire,points))
            
            top1=''
            point1=0

            for i in range(len(Liste_classement)):
                if int(Liste_classement[i][1])>point1:
                    point1=int(Liste_classement[i][1])
                    top1=Liste_classement[i][0]
                    indice=i
            Liste_classement.pop(indice)
            
            ax = 350
            bx = 650
            ay = 485
            by = 550
            z1 = bx - ax
            z2 = by - ay
            bouton_top1=rectangle(ax, ay, bx, by, couleur='white', remplissage='goldenrod', epaisseur=5)
            txt_top1=texte(ax + z1 / 2, ay + z2 / 2, '1er : '+str(top1)+' avec '+str(point1)+' points', couleur='black', ancrage='center', police="Purisa", taille=16,tag='')
            ax = 250  # Permet de créer le premier bouton dont les valeurs
            bx = 700
            ay = 850
            by = 950
            z1= bx - ax
            z2= by - ay
            bouton_quitter = rectangle(ax, ay, bx, by, couleur='white', remplissage='grey', epaisseur=5)
            txt_quitter = texte(ax + z1 / 2, ay + z2 / 2, 'Retour', couleur='black', ancrage='center', police="Purisa", taille=18,tag='')
            mise_a_jour()
            retour=0
            while retour == 0:
                x, y, t = attente_clic()
                if ax < x < bx and ay < y < by:
                    retour=1
            
    elif len(lst_vainqueur) == 2:
        Liste_classement=[]
        for lignes in lst_vainqueur:
            chaine_auxilaire=''
            points=''
            for caracteres in lignes:
                if caracteres != ';' and caracteres not in ['0','1','2','3','4','5','6','7','8','9']:
                    chaine_auxilaire+=caracteres
                elif caracteres != ';' and caracteres in ['0','1','2','3','4','5','6','7','8','9']:
                    points+=caracteres
            Liste_classement.append((chaine_auxilaire,points))

        top1=''
        point1=0
        top2=''
        point2=0
        
        for i in range(len(Liste_classement)):
            if int(Liste_classement[i][1])>point1:
                point1=int(Liste_classement[i][1])
                top1=Liste_classement[i][0]
                indice=i
        Liste_classement.pop(indice)
        
        for i in range(len(Liste_classement)):
            if int(Liste_classement[i][1])>point2:
                point2=int(Liste_classement[i][1])
                top2=Liste_classement[i][0]
                indice=i
        Liste_classement.pop(indice)
            
        ax = 350
        bx = 650
        ay = 485
        by = 550
        z1 = bx - ax
        z2 = by - ay
        bouton_top1=rectangle(ax, ay, bx, by, couleur='white', remplissage='goldenrod', epaisseur=5)
        txt_top1=texte(ax + z1 / 2, ay + z2 / 2, '1er : '+str(top1)+' avec '+str(point1)+' points', couleur='black', ancrage='center', police="Purisa", taille=16,tag='')
        ax = 350
        bx = 650
        ay = 550
        by = 615
        z1 = bx - ax
        z2 = by - ay
        bouton_top2=rectangle(ax, ay, bx, by, couleur='white', remplissage='silver', epaisseur=5)
        txt_top2=texte(ax + z1 / 2, ay + z2 / 2, '2eme : '+str(top2)+' avec '+str(point2)+' points', couleur='black', ancrage='center', police="Purisa", taille=16,tag='')       
        ax = 250  # Permet de créer le premier bouton dont les valeurs
        bx = 700
        ay = 850
        by = 950
        z1= bx - ax
        z2= by - ay
        bouton_quitter = rectangle(ax, ay, bx, by, couleur='white', remplissage='grey', epaisseur=5)
        txt_quitter = texte(ax + z1 / 2, ay + z2 / 2, 'Retour', couleur='black', ancrage='center', police="Purisa", taille=18,tag='')
        mise_a_jour()
        retour=0
        while retour == 0:
            x, y, t = attente_clic()
            if ax < x < bx and ay < y < by:
                retour=1
            
    else:      
        Liste_classement=[]
        for lignes in lst_vainqueur:
            chaine_auxilaire=''
            points=''
            for caracteres in lignes:
                if caracteres != ';' and caracteres not in ['0','1','2','3','4','5','6','7','8','9']:
                    chaine_auxilaire+=caracteres
                elif caracteres != ';' and caracteres in ['0','1','2','3','4','5','6','7','8','9']:
                    points+=caracteres
            Liste_classement.append((chaine_auxilaire,points))

        top1=''
        point1=0
        top2=''
        point2=0
        top3=''
        point3=0
        
        for i in range(len(Liste_classement)):
            if int(Liste_classement[i][1])>point1:
                point1=int(Liste_classement[i][1])
                top1=Liste_classement[i][0]
                indice=i
        Liste_classement.pop(indice)
        
        for i in range(len(Liste_classement)):
            if int(Liste_classement[i][1])>point2:
                point2=int(Liste_classement[i][1])
                top2=Liste_classement[i][0]
                indice=i
        Liste_classement.pop(indice)
            
        for i in range(len(Liste_classement)):
            if int(Liste_classement[i][1])>point3:
                point3=int(Liste_classement[i][1])
                top3=Liste_classement[i][0]
                indice=i
        Liste_classement.pop(indice)
            
        ax = 350
        bx = 650
        ay = 485
        by = 550
        z1 = bx - ax
        z2 = by - ay
        bouton_top1=rectangle(ax, ay, bx, by, couleur='white', remplissage='goldenrod', epaisseur=5)
        txt_top1=texte(ax + z1 / 2, ay + z2 / 2, '1er : '+str(top1)+' avec '+str(point1)+' points', couleur='black', ancrage='center', police="Purisa", taille=16,tag='')
        ax = 200
        bx = 500
        ay = 550
        by = 615
        z1 = bx - ax
        z2 = by - ay
        bouton_top2=rectangle(ax, ay, bx, by, couleur='white', remplissage='silver', epaisseur=5)
        txt_top2=texte(ax + z1 / 2, ay + z2 / 2, '2eme : '+str(top2)+' avec '+str(point2)+' points', couleur='black', ancrage='center', police="Purisa", taille=16,tag='')
        ax = 500
        bx = 800
        ay = 550
        by = 615
        z1 = bx - ax
        z2 = by - ay
        bouton_top3=rectangle(ax, ay, bx, by, couleur='white', remplissage='brown', epaisseur=5)
        txt_top3=texte(ax + z1 / 2, ay + z2 / 2, '3eme : '+str(top3)+' avec '+str(point3)+' points', couleur='black', ancrage='center', police="Purisa", taille=16,tag='')       
                
        ax = 250  # Permet de créer le premier bouton dont les valeurs
        bx = 700
        ay = 850
        by = 950
        z1= bx - ax
        z2= by - ay
        bouton_quitter = rectangle(ax, ay, bx, by, couleur='white', remplissage='grey', epaisseur=5)
        txt_quitter = texte(ax + z1 / 2, ay + z2 / 2, 'Retour', couleur='black', ancrage='center', police="Purisa", taille=18,tag='')
        mise_a_jour()
        retour=0
        while retour == 0:
            x, y, t = attente_clic()
            if ax < x < bx and ay < y < by:
                retour=1

 
def pause():
    """Permet de crée une interface qui va permettre de mettre pause, de reprendre ou de quitter le jeu.
    """
    ax = 1000/2 - 100  # Permet de créer le premier bouton dont les valeurs
    bx = 1000/2 + 100
    ay = 1000/2 - 150
    by = 1000/2 - 100

    ax2 = 1000/2 - 100   # Permet de créer le deuxième bouton dont les valeurs
    bx2 = 1000/2 + 100
    ay2 = 1000/2 - 50
    by2 = 1000/2

    ax3 = 1000/2 - 100   # Permet de créer le troisième bouton dont les valeurs
    bx3 = 1000/2 + 100
    ay3 = 1000/2 + 50
    by3 = 1000/2 + 100

    l1 = bx - ax  # On utlise cette formule pour centrer le texte dans les rectangles
    l2 = ay - by

    l1_1 = bx2 - ax2
    l2_2 = by2 - ay2

    r1 = rectangle(1000/2 - 200, 1000/2 - 200, 1000/2 + 200, 1000/2 + 200, couleur='black', remplissage='grey',
              tag='rect')

    r2 = rectangle(ax, ay, bx, by, couleur='white', remplissage='grey',
                   epaisseur=5, tag='rect')  # Affichage premier bouton sous forme rectangulaire
    r3 = texte(ax + l1 / 2, by + l2 / 2, 'Reprendre', couleur='black', ancrage='center', police="Purisa", taille=18,
               tag='rect')  # Permet d'écrire "Jouer" dans le premier rectangle
    r4 = rectangle(ax2, ay2, bx2, by2, couleur='white', remplissage='grey',
                   epaisseur=5, tag='rect')  # Affichage deuxième bouton sous forme rectangulaire
    r5 = texte(ax2 + l1_1 / 2, ay2 + l2_2 / 2, 'Sauvegarder', couleur='black', ancrage='center', police="Purisa", taille=18,
               tag='rect')

    r6 = rectangle(ax3, ay3, bx3, by3, couleur='white', remplissage='grey',
                   epaisseur=5, tag='rect')
    r5 = texte(ax3 + l1_1 / 2, ay3 + l2_2 / 2, 'Quitter', couleur='black', ancrage='center', police="Purisa",
               taille=18,
               tag='rect')

    p = True
    while p:
        x, y, t = attente_clic()
        if ax < x < bx and ay < y < by:
            efface('rect')
            p = False
        if ax2 < x < bx2 and ay2 < y < by2:
            efface('rect')
            return 'sauvegarde'
        if ax3 < x < bx3 and ay3 < y < by3:
            return False
        

def Sauvegarder(sablier, obst, score, taille_boules, dynamique, terminaisons,nbTours, couleur_joueur1, couleur_joueur2, obst_a, obst_b, score_bleu, score_rouge, Budget1, Budget2, pseudo1, pseudo2, Liste_des_pixels):
    """Fonction permettant de sauvegarder des variables et des structures de données.
    
    Arguments :
        sablier : variable contenant False ou True.
        obst : variable contenant False ou True.
        score : variable contenant False ou True.
        taille_boules : variable contenant False ou True.
        dynamique : variable contenant False ou True.
        terminaisons : variable contenant False ou True.
        nbTours : variable contenant le nombre de tours.
        couleur_joueur1 : chaine de caractère contenant la couleur du joueur 1.
        couleur_joueur2 : chaine de caractère contenant la couleur du joueur 2.
        obst_a : Liste contenant les abscisses des obstacles.
        obst_b : Liste contenant les ordonnées des obstacles
        score_bleu : variable contenant le score du joueur 1
        score_rouge : variable contenant le score du joueur 2
        Budget1 : chaine de caractère contenant le Budget du joueur 1
        Budget2 : chaine de caractère contenant le Budget du joueur 2
        pseudo1 : chaine de caractère contenant le pseudo du joueur 1
        pseudo2 : chaine de caractère contenant le pseudo du joueur 2
        Liste_des_pixels : Liste contenant tous les pixels du jeu.
    """
    with open("save.txt",'w') as fich_s:
        fich_s.write("EmplacementsJoueur1:"+str(EmplacementsJoueur1)+"\n")
        fich_s.write("EmplacementsJoueur2:"+str(EmplacementsJoueur2)+"\n")
        fich_s.write("tourJoueur:" + str(tourJoueur) + "\n")
        fich_s.write("texte_compteur:" + str(texte_compteur) + "\n")
        fich_s.write("nbTourReel:" + str(nbTourReel) + "\n")
        fich_s.write("nbTours:" + str(nbTours) + "\n")
        fich_s.write("couleur_joueur1:" + str(couleur_joueur1) + "\n")
        fich_s.write("couleur_joueur2:" + str(couleur_joueur2) + "\n")
        fich_s.write("sablier:" + str(sablier) + "\n")
        fich_s.write("dynamique:" + str(dynamique) + "\n")
        fich_s.write("terminaisons:" + str(terminaisons) + "\n")
        fich_s.write("obst:" + str(obst) + "\n")
        fich_s.write("score:" + str(score) + "\n")
        fich_s.write("taille_boules:" + str(taille_boules) + "\n")
        fich_s.write("pseudo1:" + str(pseudo1) + "\n")
        fich_s.write("pseudo2:" + str(pseudo2) + "\n")
        fich_s.write("Liste_des_pixels:" + str(Liste_des_pixels)+ "\n")
        if obst:
            fich_s.write("obst_a:" + str(obst_a) + "\n")
            fich_s.write("obst_b:" + str(obst_b) + "\n")
        if score:
            fich_s.write("score_bleu:" + str(score_bleu) + "\n")
            fich_s.write("score_rouge:" + str(score_rouge) + "\n")
        if taille_boules:
            fich_s.write("Budget1:" + str(Budget1) + "\n")
            fich_s.write("Budget2:" + str(Budget2) + "\n")


def main(sablier, obst, score, taille_boules, dynamique, terminaisons, couleur_joueur1, couleur_joueur2, pseudo1, pseudo2, CompteurG):
    """Fonction principale qui permet d'éxecuter le code principal.
    
    Arguments :
        sablier : variable contenant True ou False.
        obst : variante contenant True ou False.
        score : variante contenant True ou False.
        taille_boules : variante contenant True ou False.
        dynamique : variante contenant True ou False.
        terminaisons : variante contenant True ou False.
        couleur_joueur1 : Couleur du joueur 1.
        couleur_joueur2 : Couleur du joueur 2.
        pseudo1 : Pseudo du joueur 1.
        pseudo 2 : Pseudo du joueur 2.
        CompteurG : Variable contenant 0 ou 1.
    """
    obst_a, obst_b= [],[]
    score_bleu, score_rouge= 0,0
    if CompteurG==0: #Vérifie si on lance le jeu normalement
        global tourJoueur, Emplacements, EmplacementsJoueur2, EmplacementsJoueur1, Boules_rouge, Boules_bleu, customCanvas, texte_compteur, nbTourReel, pasDeClic, Budget1, Budget2, Budget, compteur_terminaison, Liste_des_pixels
        efface_tout()
        image(500, 500, 'el.gif', ancrage='center') #image de fond.
        if tourJoueur==1:
            texte_joueur = texte(380, 150, "Tour de : "+str(pseudo1), couleur=couleur_joueur1)
        else:
            texte_joueur = texte(380, 150, "Tour de : "+str(pseudo2), couleur=couleur_joueur2)
        nbTours = 20
        if taille_boules: #si la variable taille_boules est active
            Budget1 = 200 
            Budget2 = 200
            budget_txt = texte(380, 800, "Budget : " +str(Budget1), couleur=couleur_joueur1)
        nbTourReel = 0 #initialise le nombre de tour actuel
        dessiner_superficie() #dessine la surface du jeu
        texte_compteur = texte(0, 0, '', couleur=couleur_joueur1)
        if obst: #si la variante obstacles est active
            nbr_obst = randint(4, 7)
            obst_a, obst_b = Obstacles(nbr_obst)
    else: #Vérifie qu'on charge une sauvegarde
        dessiner_superficie()
        if os.path.isfile('save.txt'):
            dico = dict()
            with open("save.txt") as parametre:
                for line in parametre:
                    line = line
                    (key, val) = line.split(":")
                    dico[key] = val[:-1]
                EmplacementsJoueur1 = eval(dico['EmplacementsJoueur1'])
                EmplacementsJoueur2 = eval(dico['EmplacementsJoueur2'])
                tourJoueur = eval(dico['tourJoueur'])
                #customCanvas = eval(dico['customCanvas'])
                texte_compteur = eval(dico['texte_compteur'])
                nbTourReel = eval(dico['nbTourReel'])
                nbTours = eval(dico['nbTours'])
            if obst:
                obst_a = eval(dico["obst_a"])
                obst_b = eval(dico["obst_b"])
            if score:
                score_bleu = eval(dico["score_bleu"])
                score_rouge = eval(dico["score_rouge"])
            if taille_boules:
                Budget1 = eval(dico["Budget1"])
                Budget2 = eval(dico["Budget2"])
            boule = []
            if len(EmplacementsJoueur1) > 0:
                for i in EmplacementsJoueur1:
                    boule1 = cercle(i[0], i[1], i[2], couleur=couleur_joueur1, remplissage=couleur_joueur1)
                    boule.append(boule1)
                    Boules_bleu.append(boule1)   
            if len(EmplacementsJoueur2) > 0:
                for i in EmplacementsJoueur2:
                    boule2 = cercle(i[0], i[1], i[2], couleur=couleur_joueur2, remplissage=couleur_joueur2)
                    boule.append(boule2)
                    Boules_rouge.append(boule2)       
            if obst:
                if len(obst_a) > 0:
                    for i in range(len(obst_a)):
                        boule = cercle(obst_a[i], obst_b[i], 30, remplissage='black')
            if tourJoueur == 2:
                texte_joueur=texte(380, 150, "Tour de : "+str(pseudo1), couleur=couleur_joueur1)
                if taille_boules:
                    budget_txt = texte(380, 800, "Budget : " + str(Budget1), couleur=couleur_joueur1)
            else:
                texte_joueur=texte(380, 150, "Tour de : "+str(pseudo2), couleur=couleur_joueur2)
                if taille_boules:
                    budget_txt = texte(380, 800, "Budget : " + str(Budget2), couleur=couleur_joueur2)
                        
    
    while nbTourReel != nbTours: #tant que le nombre de tour actuel n'est pas égal au nombre de tour total.
        texte_nbtour = texte(820, 0, "Tour :" + str(nbTourReel + 1) + "/" + str(nbTours), couleur="white")
        pasDeClic = False
        if sablier: #si la variante sablier est active.
            timer(nbr_tout_s, nbTourReel)
            
        emplacementClic = attente_clic_ou_touche() #Attend un clic ou une touche de la part de l'utilisateur.

        while emplacementClic[2] == "Touche":
            if emplacementClic[1] == 'p':
                vari = pause()
                if vari == False:
                    ferme_fenetre()
                    exit()
                if vari == 'sauvegarde':
                    score_bleu, score_rouge= 0,0
                    Sauvegarder(sablier, obst, score, taille_boules, dynamique, terminaisons,nbTours, couleur_joueur1, couleur_joueur2, obst_a, obst_b, score_bleu, score_rouge, Budget1, Budget2, pseudo1, pseudo2, Liste_des_pixels)
                    
            if emplacementClic[1] == "s" and score: #si la touche pressée est 's' et que la variante score est active.
                Scores(couleur_joueur1, couleur_joueur2, Liste_des_pixels)
            if emplacementClic[1] == "t" and terminaisons: #si la touche pressée est 't' et que la variante terminaison est active.
                if compteur_terminaison == 0: #si la variante terminaison n'a toujours pas été utilisée.
                    nbTours = Terminaisons()
                    nbTourReel = 0
                    efface(texte_nbtour)
                    texte_nbtour = texte(820, 0, "Tour :" + str(nbTourReel + 1) + "/" + str(nbTours), couleur="white")
                    mise_a_jour()
                    compteur_terminaison = 1
            emplacementClic = attente_clic_ou_touche()
            
        if taille_boules: #si la variante taille_boules est active. On crée alors un espace pour pouvoir écrire le rayon.
            rectangle_input=rectangle(100,400,900,600,couleur='black', remplissage='white',epaisseur=10)
            texte_rectangle=texte(330,410,"Veuillez entrer un rayon :", couleur="black")
            texte_rectangl2=texte(220,435,"Si vous cliquez dans un cercle, mettez 0.", couleur="black")
            rayon=''
            compteur_touche=1
            touche = attente_touche() #attend une touche
            
            while touche != 'Return': #si la touche n'est pas "entrée"
                if touche == 'BackSpace' and compteur_touche > 1: #si la touche n'est pas "effacer" et que il y'a au moins 1 chiffre écrit.
                    rayon = rayon[:-1]
                    if compteur_touche == 2:
                        efface(valeur1)
                        compteur_touche -= 1
                    elif compteur_touche == 3:
                        efface(valeur2)
                        compteur_touche -= 1
                    elif compteur_touche == 4:
                        efface(valeur3)
                        compteur_touche -= 1
                if compteur_touche != 4: #Le budget max étant un nombre à 3 chiffres. On limite alors le nombre écrit à 3 chiffres.
                    if touche in ['0','1','2','3','4','5','6','7','8','9']:
                        rayon+=str(touche)
                        if compteur_touche==1:
                            valeur1=texte(500,510,str(touche),couleur='black')
                            compteur_touche+=1
                        elif compteur_touche==2:
                            valeur2=texte(520,510,str(touche),couleur='black')
                            compteur_touche+=1
                        else:
                            valeur3=texte(540,510,str(touche),couleur='black')
                            compteur_touche+=1
                        mise_a_jour()
                touche = attente_touche() #on attend une touche
            

            while rayon == '': #si l'utilisateur n'a pas rentré de valeur et à appuyé sur entrée.
                txt_erreur=texte(280,460,"Veuillez entrer un rayon valide !",couleur='black')
                mise_a_jour()
                compteur_erreur=0

                while compteur_erreur != 1:
                    time.sleep(1)
                    mise_a_jour()
                    compteur_erreur +=1
                
                efface(txt_erreur)

                compteur_touche=1
                touche = attente_touche()
                while touche != 'Return' and compteur_touche != 4:
                    if touche in ['0','1','2','3','4','5','6','7','8','9']:
                        rayon+=str(touche)
                        if compteur_touche==1:
                            valeur1=texte(500,510,str(touche),couleur='black')
                            compteur_touche+=1
                        elif compteur_touche==2:
                            valeur2=texte(520,510,str(touche),couleur='black')
                            compteur_touche+=1
                        else:
                            valeur3=texte(540,510,str(touche),couleur='black')
                            compteur_touche+=1
                    touche = attente_touche()
                
            rayon = int(rayon)
            efface(budget_txt)
            efface(texte_joueur)
            efface(rectangle_input)
            efface(texte_rectangle)
            efface(texte_rectangl2)
            if compteur_touche==2:
                efface(valeur1)
            if compteur_touche==3:
                efface(valeur1)
                efface(valeur2)
            if compteur_touche==4:
                efface(valeur1)
                efface(valeur2)
                efface(valeur3)
            mise_a_jour()
        else:
            rayon = R #rayon initial si la variante taille boule n'est pas active.

        if nbTourReel % 2 == 0:
            tourJoueur = 1
            efface(texte_joueur)
            texte_joueur = texte(380, 150, "Tour de : "+str(pseudo2), couleur=couleur_joueur2)
            if taille_boules:
                Budget = Budget2
                efface(budget_txt)
                budget_txt = texte(380, 800, "Budget : " + str(Budget2), couleur=couleur_joueur2)
        else:
            tourJoueur = 2
            efface(texte_joueur)
            texte_joueur = texte(
                380, 150, "Tour de : "+str(pseudo1), couleur=couleur_joueur1)
            if taille_boules:
                efface(budget_txt)
                budget_txt = texte(380, 800, "Budget : " + str(Budget1), couleur=couleur_joueur1)
                Budget = Budget1
        # si pas de clic passage au tour suivant
        if pasDeClic == True:
            nbTourReel += 1
            if tourJoueur == 1:
                tourJoueur = 2
            else:
                tourJoueur = 1
            efface(texte_nbtour)
            
            continue

        if verifierEmplacementClic(emplacementClic, rayon, rectanglePosAX, rectanglePosAY, rectanglePosBX, rectanglePosBY) == True:
            pose_boule = True
            if tourJoueur == 1 and taille_boules: #permet de déduire le budget utilisée au budget initial
                Budget = Budget1
            elif tourJoueur == 2 and taille_boules: #permet de déduire le budget utilisée au budget initial
                Budget = Budget2
            if taille_boules:
                if Budget >= rayon: #si le rayon est plus grand que le budget restant.
                    pose_boule = True
                else:
                    pose_boule = False
            if pose_boule:
                if tourJoueur == 1: 
                    EmplacementsJoueur = EmplacementsJoueur1
                    EmplacementsJoueurAdversaire = EmplacementsJoueur2
                    couleurBoule = couleur_joueur1
                    Boules = Boules_rouge
                else:
                    EmplacementsJoueur = EmplacementsJoueur2
                    EmplacementsJoueurAdversaire = EmplacementsJoueur1
                    couleurBoule = couleur_joueur2
                    Boules = Boules_bleu

                lst_verif_clic_boule = verifier_clic_boule(emplacementClic)
                condition = True
                # obliger d'insérer une boucle pour obtenir le 1er element car lst_verif_clic_boule[0] provoque un index out of range.
                for element in lst_verif_clic_boule:
                    condition = element
                    break

                if condition == True:
                    inter_obst = True
                    x, y, t = emplacementClic
                    if verifierIntersection(x, y, rayon, EmplacementsJoueurAdversaire):
                        if obst:
                            inter_obst = inter_obstacle(
                                x, y, rayon, obst_a, obst_b)
                        if inter_obst:
                            Emplacements.append(emplacementClic)
                            boule = cercle(emplacementClic[0], emplacementClic[1], rayon, couleur=couleurBoule, remplissage=couleurBoule, epaisseur=1)
                            Liste_des_pixels=affecter_pixel(Liste_des_pixels, emplacementClic[0], emplacementClic[1], rayon, couleurBoule)
                            if tourJoueur == 1:
                                EmplacementsJoueur1.append(
                                    [emplacementClic[0], emplacementClic[1], rayon])
                                Boules_bleu.append(boule)
                                if taille_boules:
                                    Budget1 = Budget1 - rayon
                            else:
                                EmplacementsJoueur2.append(
                                    [emplacementClic[0], emplacementClic[1], rayon])
                                Boules_rouge.append(boule)
                                if taille_boules:
                                    Budget2 = Budget2 - rayon
                    else:
                        rectangle_erreur=rectangle(100,400,900,600,couleur='black', remplissage='white',epaisseur=10)
                        msg_erreur_rectangle=texte(250,475,"Intersection ! Vous perdez votre tour !", couleur="black")
                        
                        mise_a_jour()
                        compteur_erreur_msg=0
                        while compteur_erreur_msg!=1:
                            time.sleep(1)
                            compteur_erreur_msg+=1
                        
                        efface(rectangle_erreur)
                        efface(msg_erreur_rectangle)
                else:
                    if tourJoueur == 1:
                        couleurBoule = couleur_joueur2
                        Boules=Boules_rouge
                    else:
                        couleurBoule = couleur_joueur1
                        Boules=Boules_bleu
                    remplacer_boule(EmplacementsJoueurAdversaire, Boules, lst_verif_clic_boule, emplacementClic, couleurBoule, Liste_des_pixels)
                nbTourReel += 1
                efface(texte_nbtour)
                efface(texte_nbtour)
            else: #si l'utilisateur rentre un rayon qui dépasse le budget restant.
                rectangle_erreur=rectangle(100,400,900,600,couleur='black', remplissage='white',epaisseur=10)
                msg_erreur_rectangle=texte(300,475,"Erreur ! Pas assez de budget !", couleur="black")
                
                mise_a_jour()
                compteur_erreur_msg=0
                while compteur_erreur_msg!=1:
                    time.sleep(1)
                    compteur_erreur_msg+=1
                
                efface(rectangle_erreur)
                efface(msg_erreur_rectangle)
                nbTourReel += 1
                efface(texte_nbtour)
        else: #si l'utilisateur clique en dehors de la surface jouable.
            rectangle_erreur=rectangle(100,400,900,600,couleur='black', remplissage='white',epaisseur=10)
            msg_erreur_rectangle=texte(350,475,"Vous perdez votre tour !", couleur="black")
            
            mise_a_jour()
            compteur_erreur_msg=0
            while compteur_erreur_msg!=1:
                time.sleep(1)
                compteur_erreur_msg+=1
            
            efface(rectangle_erreur)
            efface(msg_erreur_rectangle)
            
            efface(texte_nbtour)
            nbTourReel += 1
            efface(texte_compteur)
        if dynamique and obst: #si la variante dynamique et la variante obstacle sont actives.
            Dynamique_obstacle(EmplacementsJoueur1, EmplacementsJoueur2, obst_a, obst_b, couleur_joueur1, couleur_joueur2)
        if dynamique and obst == False: #si la variante dynamique est active mais pas la variante obstacle.
            Dynamique(EmplacementsJoueur1, EmplacementsJoueur2, couleur_joueur1, couleur_joueur2)

    
    #Fin de la Partie
    efface(texte_joueur)
    efface(texte_compteur)
    if taille_boules:
        efface(budget_txt)
    scores_joueurs = calculer_resultat(Liste_des_pixels, couleur_joueur1, couleur_joueur2) #calcul des scores
    if scores_joueurs[0] > scores_joueurs[1]: #si le joueur1 à un plus grand score que le joueur 2
        texte(600, 100, str(pseudo1)+" gagne !", couleur=couleur_joueur1, ancrage='center')
    elif scores_joueurs[1] > scores_joueurs[0]: #si le joueur 2 à un plus grand score que le joueur 1
        texte(600, 100, str(pseudo2)+" gagne !", couleur=couleur_joueur2, ancrage='center')
    else: #si le joueur 1 à le même score que le joueur 2
        texte(600, 100, "Egalité, personne ne gagne !", couleur="white", ancrage='center')
    
    
    #Affection les nouveaux scores/nouveaux joueurs au classement.
    Fichier_classement=open('Classement.txt')
    Lst_classement=Fichier_classement.readlines()
    Fichier_classement.close()
    
    dico_classement={}
    
    for lignes in Lst_classement:
        chaine_aux=''
        point=''
        for caracteres in lignes:
            if caracteres != ';' and caracteres not in ['0','1','2','3','4','5','6','7','8','9']:
                chaine_aux+=caracteres
            elif caracteres != ';' and caracteres in ['0','1','2','3','4','5','6','7','8','9']:
                point+=caracteres
        dico_classement[chaine_aux[:-1]]=point
    
    couple1 = (pseudo1, scores_joueurs[0])
    couple2 = (pseudo2, scores_joueurs[1])
    
    if couple1[0] in dico_classement.keys():
        if couple1[1] > int(dico_classement[couple1[0]]):
            dico_classement[couple1[0]]=couple1[1]
    else:
        dico_classement[couple1[0]] = couple1[1]
                
    if couple2[0] in dico_classement.keys():
        if couple2[1] > int(dico_classement[couple2[0]]):
            dico_classement[couple2[0]]=couple2[1]
    else:
        dico_classement[couple2[0]] = couple2[1]
        
    Fichier_classement=open('Classement.txt', 'w')
    for element in dico_classement:
        if element[-1]=='\n':
            element2 = element[:-1]
            Fichier_classement.write(str(element2)+';'+str(dico_classement[element])+'\n')
        else:
            Fichier_classement.write(str(element)+';'+str(dico_classement[element])+'\n')
    Fichier_classement.close()
        
    
    attente_clic()
    mise_a_jour()
# ---------------------- FIN DES FONCTIONS ----------------------#
if __name__ == '__main__':
    customCanvas=cree_fenetre(1000, 1000)  # Création fenetre
    u = 0
    while u == 0:
        affichage=menu()
        if affichage == 1:  # condition pour si menu = 1 cela affiche le jeu ("Jouer")
            u=1
            couleur_joueur1, couleur_joueur2 = Accueil(1000)
            pseudos=pseudo()
            pseudo1=pseudos[0]
            pseudo2=pseudos[1]
            sablier, obstacles, score, taille_boules, dynamique, terminaison = variante()
            main(sablier, obstacles, score, taille_boules, dynamique, terminaison, couleur_joueur1, couleur_joueur2, pseudo1, pseudo2, 0)  # Le jeu
        elif affichage == 2:
            Classement()
        elif affichage == 3:
            if os.path.isfile('save.txt'):
                dico = dict()
                with open("save.txt") as parametre:
                    for line in parametre:
                        line = line
                        (key, val) = line.split(":")
                        dico[key] = val[:-1]
                    Liste_des_pixels = eval(dico['Liste_des_pixels'])
                    couleur_joueur1 = dico['couleur_joueur1']
                    couleur_joueur2 = dico['couleur_joueur2']
                    sablier = eval(dico['sablier'])
                    dynamique = eval(dico['dynamique'])
                    terminaisons = eval(dico['terminaisons'])
                    obst = eval(dico['obst'])
                    score = eval(dico['score'])
                    taille_boules = eval(dico['taille_boules'])
                    pseudo1= dico['pseudo1']
                    pseudo2= dico['pseudo2']
                main(sablier, obst, score, taille_boules, dynamique, terminaisons, couleur_joueur1, couleur_joueur2, pseudo1, pseudo2, 1)
                u=1
            else:
                texte(500,500, 'Il n y a pas de fichier sauvegarde.')
        else:
            u=1