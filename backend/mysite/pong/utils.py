import pyotp
from datetime import datetime, timedelta

def send_otp(request):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)   #totp = time based one time password
    otp = totp.now() # this what the user need to put , if the user put an inpout close to this, it will be close to success
    request.session["otp_secret_key"] = totp.secret #store the secret key in the user session
    valid_date = datetime.now() + timedelta(minutes=1) #set the expiration time for the otp
    request.session["otp_valid_date"] = str(valid_date) #store the expiration time to the user session

    print(f"your one time password is {otp}") #we can send taht otp by email or sms but instead we are going to print it

    # a quel moment le token est paratgé au client de manière sécurisé ?
        # ok en fait c quand le utiolisateur il enabled pour la premiere fois la 2fa que un qr code va etre généré, 
        #il va scanner le qr code avec son authetificator
        # ça va synchroniser son authentificator avec le serveur, en gros les 2 auront le token de sauvegarder de leur coté
        # la prochaine fois qu'il va se connecter il lui sera demandé le otp etcomme il kl'aura sync avec sa machien ça ofnctionnera
        # genre il se connetcera il lancera en parralèle l'uathentifccator qui sortira le bon mdp
        # et du coup le token doit etre propre a chaque user sinon bah c une faille de securité