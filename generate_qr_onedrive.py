# generate_qr_cv.py
import os
import qrcode

# Lien de téléchargement direct OneDrive
CV_URL = "https://onedrive.live.com/download?resid=865866267B5325A1!ET8bIAmPTNRGtzYf7Sh5_6wBNE4iTqRLl2aBVRW00tyEBw&authkey=!gA9I6k"

# Dossier de sortie
out_dir = os.path.join("static", "img")
os.makedirs(out_dir, exist_ok=True)

# Génération du QR code
out_path = os.path.join(out_dir, "qr_cv.png")
qrcode.make(CV_URL).save(out_path)

print(f"✅ QR Code généré : {out_path}")
print(f"🔗 Lien vers le CV : {CV_URL}")