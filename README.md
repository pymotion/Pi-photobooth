# PhotoBooth

PhotoBooth est un photobooth Python pour Raspberry Pi. Il affiche l'aperçu de la caméra en plein écran, déclenche une photo après un compte à rebours et affiche le résultat avant de revenir à l'aperçu.

Les photos sont enregistrées au format JPEG. Le bouton et le flash sont pilotés par les broches GPIO.

## Matériel requis

- Un Raspberry Pi avec Raspberry Pi OS et un environnement graphique.
- Une caméra prise en charge par Picamera2.
- Un écran connecté au Raspberry Pi.
- Un bouton relié à la broche BCM 17 et à GND.
- Un flash ou une commande de flash reliée à la broche BCM 27.


## Installation

Exécutez ces commandes depuis le Raspberry Pi, dans une session utilisateur disposant de `sudo` :

```sh
git clone https://github.com/pymotion/Pi-photobooth.git
cd Pi-photobooth
chmod +x install.sh
./install.sh
```

Le script installe les dépendances Python fournies par Raspberry Pi OS, copie le programme dans `/home/<utilisateur>/PhotoBooth`, configure les groupes nécessaires et installe le service `systemd`. Le service est activé et démarré à la fin de l'installation.

## Configuration

Les principaux réglages se trouvent dans `config.py` :

- `BUTTON_PIN` et `FLASH_PIN` : broches GPIO utilisées, numérotées selon le schéma BCM.
- `CAMERA_WIDTH`, `CAMERA_HEIGHT` et `CAMERA_FPS` : résolution et cadence de la caméra.
- `CAMERA_AUTOFOCUS` : activation de l'autofocus continu.
- `COUNTDOWN` et `REVIEW_DURATION` : durée du compte à rebours et de l'affichage de la photo.
- `SAVE_DIR` : dossier de sauvegarde des photos.

Par défaut, `SAVE_DIR` vaut `/home/pi/photos`. Le script d'installation crée plutôt `/home/<utilisateur>/photos` : si le compte du Raspberry Pi n'est pas `pi`, modifiez `SAVE_DIR` dans `config.py` pour qu'il corresponde au dossier souhaité.

## Service systemd

Le service `photobooth` démarre automatiquement au démarrage du Raspberry Pi. Pour consulter son état et ses journaux :

```sh
sudo systemctl status photobooth
journalctl -u photobooth -f
```

Pour redémarrer ou arrêter le service :

```sh
sudo systemctl restart photobooth
sudo systemctl stop photobooth
```

Le fichier du service utilisé par l'installation est `photobooth.service`.

## Pour aller plus loin

Retrouvez la présentation du projet et du matériel utilisé dans [cet article sur pymotion.com](https://pymotion.com/photobooth-etape1/).