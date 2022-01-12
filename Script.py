# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""
from zipfile import ZipFile,BadZipFile,LargeZipFile
import os
from datetime import datetime
from datetime import timedelta
import filecmp
import pysftp
from pysftp import AuthenticationException,SSHException
import urllib.request
from urllib.request import urlopen, URLError, HTTPError
from configparser import ConfigParser,ParsingError
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import sys

# =============================================================================
# Etape 1: Définissions des variables globales permettant le remplissage du tableau 
#    pour la notification Mattermost
# =============================================================================
## variable permettant de savoir ce qu'il s'est bien passé ou non
NON=":no_entry_sign:"
OUI=":white_check_mark:"

a=NON
b=NON
c=NON
d=NON
e=NON
f=NON
g=NON
h=NON
i=NON
j=NON
k=NON

# =============================================================================
# Etape 2: Creation d'un fichier log
# =============================================================================

def creation_fichier_LOG():

    try :
        mon_fichier_LOG="./Dossier_LOG/LOG "+str(datetime.today().strftime('%Y-%d-%m'))+".txt"
        fichier_log = open(mon_fichier_LOG, "w")
        fichier_log.write("Etape 1: Le script s'est bien lancé.\n")
        fichier_log.write ("Etape 2: Définissions des variables globales permettant le remplissage du tableau pour la notification Mattermost.\n")
        a=OUI ## variable permettant de savoir ce qu'il s'est bien passé ou non
    except ParsingError:
                  fichier_log.write ("DEBUG : Une erreur est survenur dans la lecture du fichier configuration, mal remplie le fichier configuration.ini.\n")
                  a=NON ## variable permettant de savoir ce qu'il s'est bien passé ou non
    return fichier_log,mon_fichier_LOG,a

fichier_log,mon_fichier_LOG,a= creation_fichier_LOG()

# =============================================================================
# Etape 3: Definition de la fonction pour envoyer un email
# =============================================================================

def Email():
    if a==OUI:  ## variable permettant de savoir ce qu'il s'est bien passé ou non
        ligne1= " Etape 2: Le fichier  fichier log s'est bien crée \n"
    else: 
        ligne1= " Etape 2: Le fichier  fichier log n'a pas pu être crée \n"
    
    if b==OUI: ## variable permettant de savoir ce qu'il s'est bien passé ou non
        ligne2= " Etape 5: Le fichier  configuration.ini a pu être ouvert \n"
    else: 
        ligne2= " Etape 5: Le fichier  configuration.ini n'a pas pu être ouvert \n"
    
    if c==OUI: ## variable permettant de savoir ce qu'il s'est bien passé ou non
        ligne3= " Etape 6: Vous avez bien remplie le fichier configuration \n"
    else: 
        ligne3= " Etape 6: Vous avez mal remplie le fichier configuration.ini \n"
    
    if d==OUI: ## variable permettant de savoir ce qu'il s'est bien passé ou non
        ligne4= " Etape 7: Le fichier zip a bien été téléchargé depuis l'URL \n"
    else: 
        ligne4= " Etape 7: Le fichier zip n'a pas pu être télécharger depuis l'URL \n"
    
    if e==OUI: ## variable permettant de savoir ce qu'il s'est bien passé ou non
        ligne5= " Etape 8: Le fichier ZIP a correctement été dézippé. \n"
    else: 
        ligne5= " Etape 8: Le fichier ZIP n'a pas pu être dézippé. \n"
        
    if f==OUI: ## variable permettant de savoir ce qu'il s'est bien passé ou non
        ligne6= " Etape 9: Le fichier a bien été renommé à la date du jour \n"
    else: 
        ligne6= " Etape 9: Le fichier n'a pas été renommé à la date du jour. \n"
        
    if g==OUI: ## variable permettant de savoir ce qu'il s'est bien passé ou non
        ligne7= " Etape 10: Le fichier a été zippé au format .tgz \n"
    else: 
        ligne7= " Etape 10: Le fichier n'a pas pu être correctement zippé au format .tgz \n"
        
    if h==OUI: ## variable permettant de savoir ce qu'il s'est bien passé ou non
        ligne8= " Etape 11: La connexion SFTP à bien été établie avec le serveur. \n"
    else: 
        ligne8= " Etape 11: La connexion SFTP n'a pas pu être établie avec le serveur. \n"
        
    if i==OUI: ## variable permettant de savoir ce qu'il s'est bien passé ou non
        ligne9= " Etape 14: La fichier du jour à bien été déposé sur le serveur. \n"
    else: 
        ligne9= " Etape 14: La fichier du jour n'a pas pu être déposé sur le serveur. \n"
        
    if j==OUI: ## variable permettant de savoir ce qu'il s'est bien passé ou non
        ligne10= " Etape 15: Certain fichier ont bien été supprimer selon la durée de conservation que vous avez rentré dans le fichier configuration. \n"
    else: 
        ligne10= " Etape 15: Impossible de supprimer certain fichier du serveur selon la durée de conservation que vous avez remplie. \n"   
    
    ligne=ligne1+ligne2+ligne3+ligne4+ligne5+ligne6+ligne7+ligne8+ligne9+ligne10
    
    try: 
        Fromadd = 'roleciq@gmail.com'
        Toadd = adresse_mail_destinataire    #  Spécification des destinataires
        message = MIMEMultipart()    # Création de l'objet "message"
        message['From'] = Fromadd    #Spécification de l'expéditeur
        message['To'] = Toadd    #Attache du destinataire à l'objet "message"
        message['Subject'] = objet_du_mail  #Spécification de l'objet de votre mail
        msg = 'Bonjour,\n Voici votre tableau récapitutaif résumant les étapes qui se sont bien passées.\n\n'+ligne+'\n Cordialement\n\n'   #Message à envoyer
        message.attach(MIMEText(msg.encode('utf-8'), 'plain', 'utf-8'))  #Attache du message à l'objet "message", et encodage en UTF-8
          
        nom_fichier = str(datetime.today().strftime('%Y-%d-%m'))+".txt"    ## Spécification du nom de la pièce jointe
        piece = open("./Dossier_LOG/LOG "+str(datetime.today().strftime('%Y-%d-%m'))+".txt", "rb")    ## Ouverture du fichier pour verifier qu'il existe
        part = MIMEBase('application', 'octet-stream')    ## Encodage de la pièce jointe en Base64
        part.set_payload((piece).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "piece; filename= %s" % nom_fichier)
        message.attach(part)    ## Attache de la pièce jointe à l'objet "message" 
        
        serveur = smtplib.SMTP('smtp.gmail.com', 587)    ## Connexion au serveur sortant (en précisant son nom et son port)
        serveur.starttls()    ## Spécification de la sécurisation
        serveur.login(Fromadd, 'iscaiznvownmcpex')    ## Authentification
        texte= message.as_string().encode('utf-8')    ## Conversion de l'objet "message" en chaine de caractère et encodage en UTF-8
        serveur.sendmail(Fromadd, Toadd, texte)    ## Envoi du mail
        serveur.quit()    ## Déconnexion du serveur
        
        k=OUI ## variable permettant de savoir ce qu'il s'est bien passé ou non
        fichier_log = open(mon_fichier_LOG, "a")
        fichier_log.write ("INFO : L'email à bien été envoyé.\n")

    except FileNotFoundError:
        fichier_log.write ("DEBUG : Impossible d'envoyer l'email car la pièce jointe est introuvable.\n")
        k=NON ## variable permettant de savoir ce qu'il s'est bien passé ou non
        Mattermost(a,b,c,d,e,f,g,h,i,j,k)
        
        
    return k

# =============================================================================
# Etape 4: Definition de la fonction pour envoyer une notification Mattermost 
# =============================================================================

def Mattermost(a,b,c,d,e,f,g,h,i,j,k):   
    fichier_log = open(mon_fichier_LOG, "a")
    fichier_log.write ("Etape 15:  Envoie d'une notification Mattermost décrivant brièvement les étapes qui se sont bien passé ou non dans le script.\n")

    try: 
        ligne1= "|                  Etapes                 |             Etats             |\n"
        ligne2= "|:----------------------------------------|:------------------------------|\n"
        ligne3= "| Creation du fichier log                 | " ''+a+'' "                   |\n"
        ligne4= "| Lecture du fichier conf                 | " ''+b+'' "                   |\n"
        ligne5= "| Bon remplissage du fichier configuration| " ''+c+'' "                   |\n"
        ligne6= "| Telechargement du fichier ZIP           | " ''+d+'' "                   |\n"
        ligne7= "| Dezippage                               | " ''+e+'' "                   |\n"
        ligne8= "| Fichier renomme                         | " ''+f+'' "                   |\n"
        ligne9= "| Zipper au format .tgz                   | " ''+g+'' "                   |\n"
        ligne10="| Connexion SFTP                          | " ''+h+'' "                   |\n"
        ligne11="| Depot sur le serveur                    | " ''+i+'' "                   |\n"
        ligne12="| Gestion de la duree de conservation     | " ''+j+'' "                   |\n"
        ligne13="| Envoie d'un Email                       | " ''+k+'' "                   |\n"
        
        
        ligne=ligne1+ligne2+ligne3+ligne4+ligne5+ligne6+ligne7+ligne8+ligne9+ligne10+ligne11+ligne12+ligne13 ## variable conteant le tableau récapitulatif des étapes
        
        
        headers = {'Content-Type':'application/json',} 
        payload = '{ "text": " '+ligne+' "}'
        
        
        requests.post('https://chat.telecomste.fr/hooks/otnp6d3trpf3peo1gdinzq77gh', headers=headers, data=payload) ## envoie sur le chat de la notification mattermost
        
    except FileNotFoundError: ## gestion d'une exception 
            fichier_log.write ("DEBUG : Impossible de déposer le fichier du jour sur le serveur car celui-ci est introuvable.\n")
            fichier_log.close()
            sys.exit()

# =============================================================================
# Etape 5: Lecture du fichier de configuration
# =============================================================================

fichier_log.write ("Etape 3: Lecture du fichier de configuration.\n")

def lecture_fichier_conf():
    try:  
        parser = ConfigParser() 
        mon_fichier='configuration.ini'
        parser.read(mon_fichier)
        open(mon_fichier) #permet d'essayer d'ouvrir le fichier pour savoir si il existe 
        b=OUI ## variable permettant de savoir ce qu'il s'est bien passé ou non
    
    except ParsingError: ## gestion d'une exception 
              fichier_log.write ("DEBUG : Une erreur est survenur dans la lecture du fichier configuration, mal remplie le fichier configuration.ini.\n")
              fichier_log.close()
              b=NON ## variable permettant de savoir ce qu'il s'est bien passé ou non
              k=Email()
              Mattermost(a,b,c,d,e,f,g,h,i,j,k)
              sys.exit()
                
    except FileNotFoundError: ## gestion d'une exception 
              fichier_log.write ("DEBUG :Fichier configuration.ini est introuvable.Peut-être que le nom du fichier à été modifié.\n")  
              fichier_log.close()
              b=NON ## variable permettant de savoir ce qu'il s'est bien passé ou non
              k=Email()
              Mattermost(a,b,c,d,e,f,g,h,i,j,k)
              sys.exit()
    return parser,b

parser,b=lecture_fichier_conf()

# =============================================================================
# Etape 6: Association des variables globales aux valeurs remplies par l'utilisateur
# =============================================================================

fichier_log.write ("Etape 4: Association des variables globales aux valeurs remplies par l’utilisateur.\n")
def variables():
    try :
        # URL de télechargement 
        url=parser.items(parser.sections()[0])[0][1]
        
        # spécifiant le nom du fichier zip
        file =parser.items(parser.sections()[1])[0][1]
        
        #paramètre de connexion SFTP
        myHostname = str(parser.items(parser.sections()[2])[0][1])
        myUsername = str(parser.items(parser.sections()[2])[1][1])
        myPassword = str(parser.items(parser.sections()[2])[2][1])
        port = int(parser.items(parser.sections()[2])[3][1])
        
        cnopts  =  pysftp . CnOpts () 
        cnopts . hostkeys  =  None
        
        #Chemin du répertoir dans lequel on souhaite stocker le fichier à archiver 
        chemin_serveur=str(parser.items(parser.sections()[3])[0][1])
        
        #Durée que l'utilisateur souhaite garder ses fichiers
        duree_de_conservation_des_fichiers=int(parser.items(parser.sections()[4])[0][1])
        
        #Envoie d'un email
        adresse_mail_destinataire = str(parser.items(parser.sections()[5])[0][1])
        objet_du_mail = str(parser.items(parser.sections()[5])[1][1])
        
        #je recupère la  date du jour 
        date=datetime.today().strftime('%Y-%d-%m')
        
        c=OUI  ## variable permettant de savoir ce qu'il s'est bien passé ou non
        
    except FileNotFoundError: ## gestion d'une exception 
                  fichier_log.write ("DEBUG :Fichier configuration.ini est introuvable.Peut-être que le nom du fichier à été modifié.\n")  
                  fichier_log.close()
                  c=NON ## variable permettant de savoir ce qu'il s'est bien passé ou non
                  k=Email()
                  Mattermost(a,b,c,d,e,f,g,h,i,j,k)
                  sys.exit()
                  # à modifier aucune erreur n'a té gérée
    return url,file,myHostname,myUsername,myPassword,port,cnopts,chemin_serveur,duree_de_conservation_des_fichiers,adresse_mail_destinataire,objet_du_mail,date,c

url,file,myHostname,myUsername,myPassword,port,cnopts,chemin_serveur,duree_de_conservation_des_fichiers,adresse_mail_destinataire,objet_du_mail,date,c=variables()

# =============================================================================
# Etape 7: Téléchargement d'un fichier à partir d'un url
# =============================================================================

fichier_log.write ("Etape 5: Téléchargement d'un fichier à partir d'un url.\n")


def telechargemment_URL():
    
    try:
        urlopen(url)    
        # Open the url
        urllib.request.urlretrieve(url,file)
        fichier_log.write ("INFO : Le Téléchargement du fichier depuis url :"+url+" s'est bien déroulé.\n")
        d=OUI ## variable permettant de savoir ce qu'il s'est bien passé ou non
        
    except HTTPError : ## gestion d'une exception 
        fichier_log.write ("DEBUG : L'adresse que vous avez spécifiée est momentanément indisponible ou n'existe plus.\n")
        fichier_log.close()
        d=NON ## variable permettant de savoir ce qu'il s'est bien passé ou non
        k=Email()
        Mattermost(a,b,c,d,e,f,g,h,i,j,k)
        sys.exit()
    
    except URLError : ## gestion d'une exception 
        fichier_log.write ("DEBUG : L'URL que vous avez spécifiée n'existe pas (il est invalide) ou vous n'êtes pas connecté à internet.\n")
        fichier_log.close()
        k=Email()
        Mattermost(a,b,c,d,e,f,g,h,i,j,k)
        d=NON ## variable permettant de savoir ce qu'il s'est bien passé ou non
        sys.exit()
        
    return d

d=telechargemment_URL()

# =============================================================================
# Etape 8: Dézippage du fichier téléchargé
# =============================================================================

fichier_log.write ("Etape 6: Dézippage du fichier téléchargé..\n")

def Dizappage(file):
    try :   
        # ouvrir le fichier zip en mode lecture
        with ZipFile(file, 'r') as zip: 
            
            # extraire tous les fichiers
            zip.extractall() 
            fichier_log.write ("INFO : L'extraction du fichier ZIP s'est bien déroulée.\n")
            e=OUI ## variable permettant de savoir ce qu'il s'est bien passé ou non
            
    except BadZipFile: ## gestion d'une exception 
            fichier_log.write ("DEBUG : Le fichier ZIP est non valide.\n")
            fichier_log.close()
            e=NON ## variable permettant de savoir ce qu'il s'est bien passé ou non
            k=Email()
            Mattermost(a,b,c,d,e,f,g,h,i,j,k)
            sys.exit()
            
    except LargeZipFile: ## gestion d'une exception 
            fichier_log.write ("DEBUG : Le fichier ZIp nécessite la fonctionnalité ZIP64 mais elle n'as pas été activée.\n")
            fichier_log.close()
            e=NON ## variable permettant de savoir ce qu'il s'est bien passé ou non
            k=Email()
            Mattermost(a,b,c,d,e,f,g,h,i,j,k)
            sys.exit()
    return zip,e

zip,e=Dizappage(file)

# =============================================================================
# Etape 9: Changement du nom du fichier au format Y-d-m
# =============================================================================

fichier_log.write ("Etape 7: Changement du nom du fichier au format Y-d-m..\n")

def renommer():
    # Liste vide afin de stocker plus tard le nom du fichier
    L=[];
    
    try:
        
        for zinfo in zip.infolist():
            L.append(zinfo.filename)
        
        zip.close()
        
        #je recherche l'extension du fichier contenue dans le zip
        extension=L[0].split('.')[-1]
        
        #je renomme le fichier
        ancien_nom=str(L[0]);
        nouveau_nom=str(date)+'.'+extension
        os.rename(ancien_nom, nouveau_nom)
        
        fichier_log.write ("INFO : Le fichier à bien été renommé à la date du jour.\n")
        f=OUI ## variable permettant de savoir ce qu'il s'est bien passé ou non
        
    except BadZipFile: ## gestion d'une exception 
        fichier_log.write ("DEBUG : Le fichier ZIP est non valide.\n")
        fichier_log.close()
        f=NON ## variable permettant de savoir ce qu'il s'est bien passé ou non
        k=Email()
        Mattermost(a,b,c,d,e,f,g,h,i,j,k)
        sys.exit()
        
    except LargeZipFile: ## gestion d'une exception 
        fichier_log.write ("DEBUG : Le fichier ZIP nécessite la fonctionnalité ZIP64 mais elle n'as pas été activée.\n")
        fichier_log.close()
        f=NON ## variable permettant de savoir ce qu'il s'est bien passé ou non
        k=Email()
        Mattermost(a,b,c,d,e,f,g,h,i,j,k)
        sys.exit()
    
    except AttributeError: ## gestion d'une exception 
        fichier_log.write ("DEBUG : Le fichier ZIP téléchargé est vide.\n")
        fichier_log.close()
        f=NON ## variable permettant de savoir ce qu'il s'est bien passé ou non
        k=Email()
        Mattermost(a,b,c,d,e,f,g,h,i,j,k)
        sys.exit()
        
    except OSError: ## gestion d'une exception 
        fichier_log.write ("DEBUG : Impossible de renomer localement ce fichier avec date du jour car un fichier existe déjà à cet emplacement avec ce nom.\n")
        fichier_log.close()
        f=NON ## variable permettant de savoir ce qu'il s'est bien passé ou non
        k=Email()
        Mattermost(a,b,c,d,e,f,g,h,i,j,k)
        sys.exit()
        
    return nouveau_nom,f

nouveau_nom,f=renommer()

# =============================================================================
# Etape 10: Zippage du fichier téléchargé au format .tgz
# =============================================================================

fichier_log.write ("Etape 8: Zippage du fichier téléchargé au format .tgz.\n")

def zippage(nouveau_nom):
    
    try :
        
        #Compression du fichier en au format .tgz 
        with ZipFile(str(date+'.tgz'), 'w') as zip:
              zip.write(nouveau_nom)
             
        # Supprimer l'ancien fichier compressé et l'achive téléchargée depuis l'url
        os.remove(nouveau_nom)
        os.remove(file)
        
        fichier_log.write ("INFO : Le fichier à bien été compressé au format .tgz à la date du jour.\n")
        g=OUI ## variable permettant de savoir ce qu'il s'est bien passé ou non
         
    except BadZipFile: ## gestion d'une exception 
            fichier_log.write ("DEBUG : Le fichier ZIP est non valide.\n")
            g=NON ## variable permettant de savoir ce qu'il s'est bien passé ou non
            fichier_log.close()
            k=Email()
            Mattermost(a,b,c,d,e,f,g,h,i,j,k)
            sys.exit()
            
    except LargeZipFile: ## gestion d'une exception 
            fichier_log.write ("DEBUG : Le fichier ZIP nécessite la fonctionnalité ZIP64 mais elle n'as pas été activée.\n")
            g=NON ## variable permettant de savoir ce qu'il s'est bien passé ou non
            fichier_log.close()
            k=Email()
            Mattermost(a,b,c,d,e,f,g,h,i,j,k)
            sys.exit()
            
    except FileNotFoundError: ## gestion d'une exception 
            fichier_log.write ("DEBUG : Impossible de supprimer le fichier qui vient d'être compressé au format .tgz car il n'existe plus.\n")
            g=NON ## variable permettant de savoir ce qu'il s'est bien passé ou non
            fichier_log.close()
            k=Email()
            Mattermost(a,b,c,d,e,f,g,h,i,j,k)
            sys.exit()
            
    return g

g=zippage(nouveau_nom)

# =============================================================================
# Etape 11: Début de la connexion SFTP
# =============================================================================

fichier_log.write ("Etape 9: Début de la connexion SFTP.\n")

def connexion_SFTP():
    
    try:
        ## debut de la connnexion SFTP
        sftp=pysftp.Connection(host=myHostname, username=myUsername, password=myPassword, port=port,cnopts = cnopts)
        fichier_log.write ("INFO : La connexion a bien été établie.\n")
        h=OUI ## variable permettant de savoir ce qu'il s'est bien passé ou non
    
    except AuthenticationException: ## gestion d'une exception 
            fichier_log.write ("DEBUG : Le nom d'utilisateur ou le mot de passe est incorrect.Impossible par conséquent de se connecter au serveur.\n")
            fichier_log.close()
            h=NON ## variable permettant de savoir ce qu'il s'est bien passé ou non
            k=Email()
            Mattermost(a,b,c,d,e,f,g,h,i,j,k)
            sys.exit()
       
    except SSHException: ## gestion d'une exception 
            fichier_log.write ("DEBUG : Le connexion à été refusée car le port ou l'adresse IP  est incorrect.\n")
            fichier_log.close()
            h=NON ## variable permettant de savoir ce qu'il s'est bien passé ou non
            k=Email()
            Mattermost(a,b,c,d,e,f,g,h,i,j,k)
            sys.exit()
            
    return sftp,h

sftp,h=connexion_SFTP()
 
# =============================================================================
# Etape 12: Récupération du fichier de la semaine dernière
# =============================================================================

fichier_log.write ("Etape 10: Récupération du fichier de la semaine dernière.\n")

def recuperer_zip_hier():
    
    date_de_la_veille=datetime.today() - timedelta(1)
    date_de_la_veille=date_de_la_veille.strftime('%Y-%d-%m')
    nom_du_fichier_veille=str(date_de_la_veille)+'.tgz'
    
    # Je definit le chemin du fichier de la veille 
    remoteFilePath = chemin_serveur+nom_du_fichier_veille
    
    #Je définit le chemin absolue du fichier de la veille où celui-ci va être téléchargé 
    localFilePath = './'+nom_du_fichier_veille
    
    # Je verifie que le fichier de la veille existe avant de le télécharger pour le comparere avec celui de la veille 
    if sftp.exists(remoteFilePath):    
        sftp.get(remoteFilePath, localFilePath)
        fichier_log.write ("INFO : Le Fichier d'hier à bien été téléchargé.\n")

    else:
        fichier_log.write ("INFO : Pas de fichier déposer la veille. Inutile de vérifier qu'il est différent de celui de la veille.\n")
    
    
    return remoteFilePath,nom_du_fichier_veille,date_de_la_veille

remoteFilePath,nom_du_fichier_veille,date_de_la_veille=recuperer_zip_hier()


# =============================================================================
# Etape 13: Comparaison du fichier de la semaine dernière et de celui du jour
# =============================================================================

fichier_log.write ("Etape 11: Comparaison du fichier de la semaine dernière et de celui du jour.\n")

def comparaison(remoteFilePath,nom_du_fichier_veille,date_de_la_veille):
    
    nom_du_jour= str(date)+'.tgz'
    comparaison= False
    
    try:
        
        #Je verifie que le fichier de la veille exist avant de faire une comparaison avec clui du jour
        if sftp.exists(remoteFilePath):
            f1=nom_du_fichier_veille
            f2=nom_du_jour
            
            Dizappage(f1)
            Dizappage(f2)
            
            comparaison=filecmp.cmp(date_de_la_veille+".sql", date+".sql", shallow=True)
            fichier_log.write (comparaison)
            
            os.remove(f1)
            os.remove(date_de_la_veille+".sql")
            os.remove(date+".sql")
            
            if comparaison:
                fichier_log.write ("INFO : Le fichier est identique à celui de la veille, inutile de le télécharger sur le serveur car il y est déjà présent.\n")
            
            else:
              fichier_log.write ("INFO : Le fichier est bien différent de celui de la veille. On va donc pouvoir le télécharger sur le serveur.\n")
            
    
    except FileNotFoundError: ## gestion d'une exception 
            fichier_log.write ("DEBUG : Impossible de comparer les deux fchiers car l'un d'entre eux ou les deux n'existent plus.\n")
            fichier_log.close()
            k=Email()
            Mattermost(a,b,c,d,e,f,g,h,i,j,k)
            sys.exit()
            
    return nom_du_jour,comparaison

nom_du_jour,comparaison=comparaison(remoteFilePath,nom_du_fichier_veille,date_de_la_veille)

# =============================================================================
# Etape 14: Dépôt du fichier du jour sur le serveur à condition qu'il soit different de celui de la veille
# =============================================================================

fichier_log.write ("Etape 12: Dépôt du fichier du jour sur le serveur à condition qu'il soit different de celui de la veille.\n")

def deposer(nom_du_jour,comparaison):
    try:  
        
        if comparaison == False:    
            
            # Define the file that you want to upload from your local directorty
            # or absolute "C:\Users\sdkca\Desktop\TUTORIAL2.txt"
            localFilePath = './'+nom_du_jour
    
            # Define the remote path where the file will be uploaded
            remoteFilePath = chemin_serveur+nom_du_jour
        
            sftp.put(localFilePath, remoteFilePath)
            fichier_log.write ("INFO : Fichier du jour bien été déposé sur le serveur.\n")
            
        else:
            fichier_log.write ("INFO : Inutile de  transférer le fichier du jour car il s'agit du même que celui de la veille.\n")    
        
        os.remove(nom_du_jour) ## je supprime le fichier .tgz stocké et local une fois bien déposé sur le serveur
        i=OUI ## variable permettant de savoir ce qu'il s'est bien passé ou non
        
    
    except FileNotFoundError: ## gestion d'une exception 
            fichier_log.write ("DEBUG : Impossible de déposer le fichier du jour sur le serveur car celui-ci est introuvable.\n")
            i=NON ## variable permettant de savoir ce qu'il s'est bien passé ou non
            fichier_log.close()
            k=Email()
            Mattermost(a,b,c,d,e,f,g,h,i,j,k)
            sys.exit()
    
    except PermissionError: ## gestion d'une exception 
            fichier_log.write ("DEBUG : Vous ne pouvez pas déposer le fichier du jour sur le serveur car vous n'avez pas les droits d'écriture.\n")
            i=NON ## variable permettant de savoir ce qu'il s'est bien passé ou non
            fichier_log.close()
            k=Email()
            Mattermost(a,b,c,d,e,f,g,h,i,j,k)
            sys.exit()
            
    return i

i=deposer(nom_du_jour,comparaison)


# =============================================================================
# Etape 15: Gestion de la durée de conservation des fichiers stockés sur le serveur
# =============================================================================

fichier_log.write ("Etape 13: Gestion de la durée de conservation des fichiers stockés sur le serveur.\n")

def gestion_duree():
    
    try:
        Date_limit=datetime.today() - timedelta(duree_de_conservation_des_fichiers)
        Date_limit=Date_limit.strftime('%Y-%d-%m')
        
        Listdir=sftp.listdir(chemin_serveur)
        Nom=[]
        for k in Listdir:
            if k.split('.')[-1]=='tgz':
                Nom.append(os.path.splitext(k)[0]) 
        
        
        for name in Nom:
            if datetime.strptime(name, '%Y-%d-%m')<datetime.strptime(Date_limit,'%Y-%d-%m'):
                #Define the file that you want to remove from your local directorty
                sftp.remove(chemin_serveur+name+'.tgz')
        
        
        Listdir=sftp.listdir(chemin_serveur)
        Nom1=[]
        for k in Listdir:
            if k.split('.')[-1]=='tgz':
                Nom1.append(os.path.splitext(k)[0]) 
          
            
        if Nom==Nom1:
            fichier_log.write ("INFO : Aucun fichier n'a été supprimé.\n")
            
        else: 
            fichier_log.write ("INFO : Des fichiers ont été supprimer du serveur selon la durée de conservation que vous avez rentré.\n")
       
        j=OUI ## variable permettant de savoir ce qu'il s'est bien passé ou non
        
    except FileNotFoundError: ## gestion d'une exception 
            fichier_log.write ("DEBUG : Impossible de supprimer un fichier sur le serveur car celui-ci est introuvable.\n")
            j=NON ## variable permettant de savoir ce qu'il s'est bien passé ou non
            k=Email()
            Mattermost(a,b,c,d,e,f,g,h,i,j,k)
            
    except PermissionError: ## gestion d'une exception 
            fichier_log.write ("DEBUG : Vous ne pouvez pas déposer supprimer les fichiers trop ancien sur le serveur car vous n'avez pas les droits d'écriture.\n")
            j=NON ## variable permettant de savoir ce qu'il s'est bien passé ou non
            k=Email()
            Mattermost(a,b,c,d,e,f,g,h,i,j,k)    
            
    return j
     
j=gestion_duree()

# =============================================================================
# Etape 16: Envoie d'un email contenant un objet, le fichier log en pièce jointe  
# ainsi qu'un message décrivant décrivant brièvement les étapes qui 
# se sont bien passé ou non dans le script
# =============================================================================

fichier_log.write ("Etape 13:Envoie d'un email à "+adresse_mail_destinataire+" contenant en pièce jointe ce fichier.\n")
fichier_log.close()

k=Email()

# =============================================================================
# Etape 17: Envoie d'une notification Mattermost décrivant brièvement les étapes
# qui se sont bien passé ou non tout au longde ce script
# =============================================================================

Mattermost(a,b,c,d,e,f,g,h,i,j,k)

# =============================================================================
# Etape 18: Fermeture de la connexion SFTP  et fermeture du fichier LOG  
# =============================================================================

sftp.close()
fichier_log.close()
