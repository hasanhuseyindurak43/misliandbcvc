import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import json

# Dark mod ayarları
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# İlk pencere
root = ctk.CTk()
root.geometry("500x500+350+10")
root.title("UI Tasarlama")

# İkinci pencere
root2 = ctk.CTk()
root2.geometry("328x600+10+10")
root2.title("UI Widgetler")

buttons = []  # Butonları saklayacak liste

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, "r") as file:
            data = json.load(file)
        
        # Pencereyi güncelle
        root.geometry(data["list_1"][3].split("\"")[1])
        
        # Mevcut butonları kaldır
        for button in buttons:
            button.destroy()
        buttons.clear()
        
        # JSON'dan butonları oluştur
        for cmd in data["to_liste"]:
            exec(cmd)
        
        update_entries()  # Genişlik ve yüksekliği güncelle

# Menü oluşturma
menubar = tk.Menu(root2, bg="black", fg="white")

# 'File' menüsü
file_menu = tk.Menu(menubar, tearoff=0, bg="black", fg="white")
file_menu.add_command(label="Open", command=open_file)
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
frame1 = ctk.CTkFrame(root2, height=100)
frame1.grid(row=1, column=0, padx=5, pady=0, sticky="ew")

# Frame 1 içeriği
label1 = ctk.CTkLabel(frame1, text="Ekran genişliği", font=("Arial", 14))
label1.grid(row=0, column=0, columnspan=3, pady=(0, 5), sticky="ew")

entry1 = ctk.CTkEntry(frame1)
entry1.grid(row=1, column=0, padx=(5, 0), pady=5, sticky="ew")
entry1.insert(0, "500")  # Varsayılan metin "500"

label_x1 = ctk.CTkLabel(frame1, text="x", font=("Arial", 14))
label_x1.grid(row=1, column=1, padx=10, pady=5)

entry2 = ctk.CTkEntry(frame1)
entry2.grid(row=1, column=2, padx=(0, 5), pady=5, sticky="ew")
entry2.insert(0, "500")  # Varsayılan metin "500"

# Frame 2 oluşturma
frame2 = ctk.CTkFrame(root2, height=500)
frame2.grid(row=2, column=0, padx=5, pady=0, sticky="nsew")  # Sticky ayarını "nsew" yaparak tüm alanı kaplamasını sağlar

# Frame 2'yi tam olarak genişletmek için row ve column konfigürasyonu
root2.grid_rowconfigure(2, weight=1)  # Frame 2'nin bulunduğu satırı genişletme
root2.grid_columnconfigure(0, weight=1)  # Frame 2'nin bulunduğu sütunu genişletme

def create_button(x=100, y=100):
    button = ctk.CTkButton(root, text="New Button")
    button.place(x=x, y=y)  # Başlangıç konumu
    buttons.append(button)  # Butonu listeye ekle

    # Sürükleme ve bırakma işlevselliği
    def on_drag_start(event):
        button._drag_start_x = event.x
        button._drag_start_y = event.y

    def on_drag_motion(event):
        deltax = event.x - button._drag_start_x
        deltay = event.y - button._drag_start_y
        new_x = button.winfo_x() + deltax
        new_y = button.winfo_y() + deltay
        button.place(x=new_x, y=new_y)
        update_json()  # JSON dosyasını güncelle

    button.bind("<Button-1>", on_drag_start)
    button.bind("<B1-Motion>", on_drag_motion)

# Frame 2'ye Button isminde bir Label ekleme
label_button = ctk.CTkLabel(frame2, text="Button", font=("Arial", 14))
label_button.pack(pady=20)  # Label'ı merkezde konumlandırmak için pady kullanabilirsiniz
label_button.bind("<Button-1>", lambda e: create_button())  # Label'a tıklama olayı ekleme

def update_json():
    width = entry1.get()
    height = entry2.get()
    
    list_1 = [
        "import customtkinter as ctk",
        "import tkinter as tk",
        f"root = ctk.CTk()",
        f"root.geometry(\"{width}x{height}+350+10\")",
        "root.title(\"My Program\")"
    ]
    
    to_liste = []
    for button in buttons:
        new_x = button.winfo_x()
        new_y = button.winfo_y()
        button_cmd = f"create_button({new_x}, {new_y})"
        to_liste.append(button_cmd)
    
    three_liste = [
        "root.mainloop()"
    ]
    
    data = {
        "list_1": list_1,
        "to_liste": to_liste,
        "three_liste": three_liste
    }
    
    with open("output.json", "w") as file:
        json.dump(data, file, indent=4)

def update_entries():
    width = root.winfo_width()
    height = root.winfo_height()
    entry1.delete(0, tk.END)
    entry1.insert(0, str(width))
    entry2.delete(0, tk.END)
    entry2.insert(0, str(height))
    root2.after(1000, update_entries)  # Her 1000ms (1 saniye) sonra güncellemeye devam eder

# Başlangıçta güncellemeyi başlat
update_entries()


def run_mainloops():
    root.mainloop()
    root2.mainloop()

run_mainloops()

