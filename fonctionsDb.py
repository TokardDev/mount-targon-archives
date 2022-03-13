# Créé par tissiel, le 18/02/2022 en Python 3.7

import sqlite3
import time
bdd = sqlite3.connect("leagueOfLegends.db")
curseur = bdd.cursor()
import json

def AfficherListeJoueurs(c):
    '''
    fonction qui permet d'afficher un la liste de tous les joueurs:
    elle affiche le pseudo, le niveau, ainsi que la photo de profil
    '''

    requete = f"""
    SELECT nomjoueur, level, iconurl
    FROM JOUEURS
    """
    c.execute(requete)
    liste=c.fetchall()
    dicos=[]

    for element in liste:
        dicos.append({"pseudo":element[0],"niveau":element[1],"icone":element[2]})
    return dicos


def AfficherLigneJoueurs(c):
    '''
    fonction qui permet de renvoyer une ligne de la liste des joueurs
    elle affiche le pseudo, le niveau, ainsi que la photo de profil
    '''
    requete = f"""
    SELECT nomjoueur, level, iconurl
    FROM JOUEURS
    """
    c.execute(requete)
    liste = c.fetchone()

    if len(liste) == None:
        return None
    else:
        return liste

def IdGames(c):
    '''
    fonction qui permet de renvoyer tous les identifiants des games
    '''

    requete = f"""
    SELECT gameid
    FROM PARTIES
    """
    c.execute(requete)
    liste = c.fetchall()
    if len(liste) == None:
        return None
    else:
        return liste





def IdGame(c):
    '''
    fonction qui permet de renvoyer un identifiant de game (le premier)
    '''
    requete = f"""
    SELECT gameid
    FROM PARTIES
    """
    c.execute(requete)
    liste = c.fetchone()

    if len(liste) == None:
        return None
    else:
        return liste



def AfficherPartiesJoueurs(c, pseudo):
    '''
    cette fonction retourne l'historique des parties d'un joueur donné
    la variable pseudo correspond au nom du joueur donné
    elle retourne donc les joueurs dans les équipes et les personnages joués
    summonners correspond aux pseudos et champions aux personnages
    '''
    requete = f"""
    SELECT summoners, champions, gameid, duree, dateCreation, morts, golds, ratioKda, kills, levels, totalDamages, farm, vision, win
    FROM PARTIES
    WHERE joueur =  ?
    ORDER BY dateCreation DESC
    """
    c.execute(requete, [pseudo])
    listeTexte = c.fetchall()
    liste=[]
    for element in listeTexte:
        liste.append({"joueurs":json.loads(element[0]),"champions":json.loads(element[1]),"gameid":element[2],"duree":element[3],"dateCreation":element[4],"morts":json.loads(element[5]),
                    "golds":json.loads(element[6]),"kda":json.loads(element[7]),"kills":json.loads(element[8]),"levels":json.loads(element[9]),"totalDamages":json.loads(element[10]),"farm":json.loads(element[11]),
                    "vision":json.loads(element[12]),"win":json.loads(element[13])})

    if len(liste) == None:
        return None
    else:
        return liste


def Summoners(c, gameid):
    '''
    fonction qui renvoie les noms des joueurs présents dans une partie donnée
    la variable gameid correspond à l'identifiant de la game
    '''
    requete = f"""
    SELECT summoners
    FROM PARTIES
    WHERE gameid = ?
    """
    c.execute(requete, [gameid[0]])
    liste = c.fetchall()

    if len(liste) == None:
        return None
    else:
        return liste


def Champions(c, gameid):
    '''
    fonction qui renvoie les noms des champions présents dans une partie donnée
    la variable gameid correspond à l'identifiant de la game
    '''
    requete = f"""
    SELECT champions
    FROM PARTIES
    WHERE gameid = ?
    """
    c.execute(requete, [gameid[0]])
    liste = c.fetchall()

    if len(liste) == None:
        return None
    else:
        return liste


def profil_joueur(c, pseudo):
    '''
    affiche certaines infos et stats comme la photo de profil, le niveau,
    le nom et des moyennes (comme le KDA moyen, temps moyen de jeu, etc)
    '''
    requete = f"""
    SELECT iconurl, level, region
    FROM Joueurs
    WHERE nomjoueur =  ?
    """
    c.execute(requete, [pseudo])
    profil=c.fetchone()

    if profil==None:
        return None
    else:
        requete = f"""
        SELECT duree
        FROM Parties
        WHERE joueur =  ?
        """
        tempsSecondes=[]
        c.execute(requete, [pseudo])
        durees=c.fetchall()
        for temps in durees:
            tempsPartie = temps[0].split(':')
            tempsSecondes.append(int(tempsPartie[0])*3600+int(tempsPartie[1])*60+int(tempsPartie[2]))
        if len(tempsSecondes)!=0:
            moyenneSecondes=sum(tempsSecondes)/len(tempsSecondes)
            tempsMoyen=time.strftime('%H:%M:%S', time.gmtime(moyenneSecondes))
        else:
            tempsMoyen=0
        profil={"icone":profil[0],"niveau":profil[1],"region":profil[2],"tempsMoyen":tempsMoyen}
        return profil







#tests:

##print(AfficherListeJoueurs(curseur))
##print(AfficherLigneJoueurs(curseur))
##print(IdGames(curseur))
##print(IdGame(curseur))
##print(AfficherPartiesJoueurs(curseur, "kyashiw"))