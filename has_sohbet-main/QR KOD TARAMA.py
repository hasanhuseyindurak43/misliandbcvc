import cv2
from pyzbar.pyzbar import decode
import customtkinter as ctk
from PIL import Image
import numpy as np

# Kamera için video yakalama nesnesini oluşturun
cap = cv2.VideoCapture(2)

# CustomTkinter için ana pencereyi oluşturun
root = ctk.CTk()
root.title("QR Kod Okuyucu")
root.geometry("800x600")


def qr_kod_oku():
    # Kameradan bir kare al
    ret, frame = cap.read()
    if not ret:
        return

    # QR kodlarını oku
    decoded_objects = decode(frame)
    for obj in decoded_objects:
        # QR kodunun sınır kutusunu çizin
        points = obj.polygon
        if len(points) == 4:
            pts = [(point.x, point.y) for point in points]
            cv2.polylines(frame, [np.array(pts, np.int32)], True, (0, 255, 0), 2)

        # QR kodunun metnini çıkar
        qr_kod_data = obj.data.decode("utf-8")
        cv2.putText(frame, qr_kod_data, (obj.rect.left, obj.rect.top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),
                    2)

        # Tarama sonuçlarını ekrana yazdır
        label.configure(text=f"Taranan QR Kod: {qr_kod_data}")

    # Görüntüyü Tkinter formatına dönüştür ve göster
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb)

    # CTkImage nesnesi oluşturun
    ctk_img = ctk.CTkImage(img, size=(800, 600))

    video_label.configure(text="", image=ctk_img)
    video_label.image = ctk_img  # Referansı kaybetmemek için image'i saklayın

    # Tekrar fonksiyonu çağırarak sürekli tarama yap
    root.after(10, qr_kod_oku)


# Etiket ve video görüntüsü için bir alan oluşturun
label = ctk.CTkLabel(root, text="QR Kod Tarama Başlatıldı...")
label.pack(pady=10)

video_label = ctk.CTkLabel(root)
video_label.pack()

# QR kod okuma fonksiyonunu başlat
qr_kod_oku()

# Pencereyi çalıştır
root.mainloop()

# Program kapandığında kamera kaynağını serbest bırak
cap.release()
