#!/bin/bash
set -e

CURRENT_USER=$(logname 2>/dev/null || whoami)
CURRENT_UID=$(id -u "$CURRENT_USER")
INSTALL_DIR="/home/$CURRENT_USER/PhotoBooth"
SERVICE_NAME="photobooth"

echo "=== Installation du PhotoBooth  ==="

# ── Dépendances système ───────────────────────────────────────
echo "[1/4] Installation des dépendances..."
sudo apt update

sudo apt install -y \
    python3-opencv \
    python3-pygame \
    python3-pil \
    python3-numpy

sudo apt install -y \
    python3-gpiozero \
    python3-lgpio \
    python3-picamera2

# ── Copie des fichiers ────────────────────────────────────────
echo "[2/4] Copie des fichiers vers $INSTALL_DIR..."
sudo mkdir -p "$INSTALL_DIR"
if [ "$(realpath .)" != "$(realpath "$INSTALL_DIR")" ]; then
    sudo cp -r ./* "$INSTALL_DIR/"
else
    echo "    Déjà dans $INSTALL_DIR, copie ignorée."
fi
sudo chown -R "$CURRENT_USER:$CURRENT_USER" "$INSTALL_DIR"

# ── Permissions ───────────────────────────────────────────────
echo "[3/4] Permissions et dossier photos..."
sudo usermod -aG video,render,gpio "$CURRENT_USER"
mkdir -p "/home/$CURRENT_USER/photos"

# ── Service systemd ───────────────────────────────────────────
echo "[4/4] Installation du service systemd..."
sed \
    -e "s/YOUR_USER/$CURRENT_USER/g" \
    -e "s/YOUR_UID/$CURRENT_UID/g" \
    photobooth.service | sudo tee "/etc/systemd/system/${SERVICE_NAME}.service" > /dev/null
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl start  "$SERVICE_NAME"

echo ""
echo "=== Installation terminée (plateforme : $PLATFORM) ==="
echo ""
echo "Commandes utiles :"
echo "  sudo systemctl status $SERVICE_NAME"
echo "  journalctl -u $SERVICE_NAME -f"
