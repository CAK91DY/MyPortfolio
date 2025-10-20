# generate_qr_local_cv.py
import os, qrcode

# ⚠️ En dev, mets l'IP locale de ta machine (PAS 127.0.0.1) pour que ton téléphone y accède.
# Exemple: "http://192.168.1.25:5000/cv"
CV_URL = "http://192.168.1.25:5000/cv"

# En prod, tu mettras ton domaine :
# CV_URL = "https://datacraftstudio.fr/cv"

out_dir = os.path.join("static", "img")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "qr_cv.png")

qrcode.make(CV_URL).save(out_path)
print("✅ QR généré ->", out_path)
print("🔗 URL ->", CV_URL)