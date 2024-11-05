import customtkinter as ctk
import tkinter as tk

# Dark mod ayarları
ctk.set_appearance_mode("dark")  # Dark mod etkinleştirme
ctk.set_default_color_theme("blue")  # Varsayılan renk temasını mavi yapma

# İlk pencere
root = ctk.CTk()
root.geometry("600x400")
root.title("UI Tasarlama")

# İkinci pencere
root2 = ctk.CTk()
root2.geometry("300x600")
root2.title("UI Widgetler")

# Menü oluşturma
menubar = tk.Menu(root2, bg="black", fg="white")

# 'File' menüsü
file_menu = tk.Menu(menubar, tearoff=0, bg="black", fg="white")
file_menu.add_command(label="Open")
file_menu.add_command(label="Save")
file_menu.add_command(label="Save As")
file_menu.add_command(label="Export.py")
menubar.add_cascade(label="File", menu=file_menu)

# 'Theme' menüsü
theme_menu = tk.Menu(menubar, tearoff=0, bg="black", fg="white")
theme_menu.add_command(label="Theme Maker")
menubar.add_cascade(label="Theme", menu=theme_menu)

# Menüyü root2 penceresine ekleyin
root2.config(menu=menubar)

# Menü çubuğunun altına 10px boşluk bırak
root2.grid_rowconfigure(0, minsize=10)

# Frame 1 oluşturma
frame1 = ctk.CTkFrame(root2, height=100)  # Yükseklik 100px olarak ayarlandı
frame1.grid(row=1, column=0, padx=5, pady=0, sticky="ew")  # Yalnızca sağ ve sol boşluklar

# Frame 1 genişletmek için sütun ve satır konfigürasyonu
frame1.grid_columnconfigure(0, weight=1)
frame1.grid_columnconfigure(1, weight=0)
frame1.grid_columnconfigure(2, weight=1)
frame1.grid_rowconfigure(1, weight=1)

# Frame 1 içeriği
label1 = ctk.CTkLabel(frame1, text="Ekran genişliği", font=("Arial", 14))
label1.grid(row=0, column=0, columnspan=3, pady=(0, 5), sticky="ew")

entry1 = ctk.CTkEntry(frame1)
entry1.grid(row=1, column=0, padx=(5, 0), pady=5, sticky="ew")

label_x1 = ctk.CTkLabel(frame1, text="x", font=("Arial", 14))
label_x1.grid(row=1, column=1, padx=10, pady=5)

entry2 = ctk.CTkEntry(frame1)
entry2.grid(row=1, column=2, padx=(0, 5), pady=5, sticky="ew")

# Frame 2 oluşturma
frame2 = ctk.CTkFrame(root2, height=500)  # Yükseklik 500px olarak ayarlandı
frame2.grid(row=2, column=0, padx=5, pady=0, sticky="ew")  # Yalnızca sağ ve sol boşluklar

# Frame 2 genişletmek için sütun ve satır konfigürasyonu
frame2.grid_columnconfigure(0, weight=1)
frame2.grid_columnconfigure(1, weight=0)
frame2.grid_columnconfigure(2, weight=1)
frame2.grid_rowconfigure(0, weight=1)

# Root2 pencere ayarları
root2.grid_rowconfigure(1, weight=0)  # Frame 1
root2.grid_rowconfigure(2, weight=1)  # Frame 2'nin esnek olmasını sağlar
root2.grid_columnconfigure(0, weight=1)

def run_mainloops():
    root.mainloop()  # Birinci pencere
    root2.mainloop()  # İkinci pencere

run_mainloops()
