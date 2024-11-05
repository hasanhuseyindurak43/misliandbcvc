import customtkinter as ctk
import qrcode
from PIL import Image
import os
import subprocess

# Pencere oluşturma
app = ctk.CTk()
app.title("QR Kod Oluşturucu")
app.geometry("400x600")

def qr_olustur():
    veri = entry.get()
    if veri.strip() != "":
        try:
            # Metni UTF-8 olarak encode et
            qr = qrcode.make(veri.encode('utf-8'))
            qr.save(f"{veri}.png")  # QR kodunu PNG olarak kaydetme
            qr_img = Image.open(f"{veri}.png")
            qr_img_resized = qr_img.resize((200, 200))  # Görüntü boyutunu ayarlama
            qr_ctk_image = ctk.CTkImage(light_image=qr_img_resized, size=(200, 200))
            qr_label.configure(text="", image=qr_ctk_image)
            qr_label.image = qr_ctk_image
        except Exception as e:
            print("Hata oluştu:", e)

def yazdir():
    dosya_yolu = os.path.abspath("qrcode.png")
    if os.name == 'nt':  # Windows için
        os.startfile(dosya_yolu, "print")
    else:  # MacOS ve Linux için
        try:
            subprocess.run(["lp", dosya_yolu], check=True)
        except subprocess.CalledProcessError:
            print("Yazdırma işlemi başarısız oldu. Lütfen varsayılan yazıcıyı kontrol edin.")

# Girdi kutusu
entry = ctk.CTkEntry(app, placeholder_text="QR kodu için metin girin")
entry.pack(pady=20)

# QR kod oluşturma butonu
olustur_button = ctk.CTkButton(app, text="QR Kod Oluştur", command=qr_olustur)
olustur_button.pack(pady=10)

# QR kod görüntü etiketi
qr_label = ctk.CTkLabel(app)
qr_label.pack(pady=20)

# Yazdırma butonu
yazdir_button = ctk.CTkButton(app, text="Yazdır", command=yazdir)
yazdir_button.pack(pady=10)

app.mainloop()
