import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, simpledialog
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

def export_to_py():
    file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python files", "*.py")])
    if file_path:
        with open("output.json", "r") as json_file:
            data = json.load(json_file)
        
        with open(file_path, "w") as py_file:
            # İlk listeyi yaz
            for line in data.get("list_1", []):
                py_file.write(line + "\n")
            
            # Fonksiyonları yaz
            for func in data.get("def_liste", []):
                py_file.write(func + "\n")
                
            # Buton komutlarını yaz
            for cmd in data.get("to_liste", []):
                py_file.write(cmd + "\n")

            for line in data.get("list_2", []):
                py_file.write(line + "\n")
         
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
        for cmd in data["to2_liste"]:
            exec(cmd)
        
        update_entries()  # Genişlik ve yüksekliği güncelle

# Menü oluşturma
menubar = tk.Menu(root2, bg="black", fg="white")

# 'File' menüsü
file_menu = tk.Menu(menubar, tearoff=0, bg="black", fg="white")
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save")
file_menu.add_command(label="Save As")
file_menu.add_command(label="Export.py", command=export_to_py)
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

buttons = []  # Butonları saklayacak liste
button_counter = 0  # Buton adlarını oluşturmak için sayaç


def create_button(x=100, y=100, width=100, height=30, text="New Button"):
    global button_counter
    button_counter += 1
    button_name = f"button{button_counter}"
    
    button = ctk.CTkButton(root, text=text, width=width, height=height)
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

    # Sağ tıklama ile boyutları ayarlama
    def on_right_click_start(event):
        button._resize_start_x = event.x
        button._resize_start_y = event.y
        button._initial_width = button.winfo_width()
        button._initial_height = button.winfo_height()

    def on_right_click_motion(event):
        width_delta = event.x - button._resize_start_x
        height_delta = event.y - button._resize_start_y
        new_width = max(30, button._initial_width + width_delta)  # Minimum genişlik
        new_height = max(30, button._initial_height + height_delta)  # Minimum yükseklik
        button.configure(width=new_width, height=new_height)  # `config` yerine `configure` kullanıyoruz
        update_json()  # JSON dosyasını güncelle

    button.bind("<Button-3>", on_right_click_start)
    button.bind("<B3-Motion>", on_right_click_motion)

    # Buton adı değiştirme
    def on_double_click(event):
        new_name = simpledialog.askstring("Buton Adı", "Yeni buton adını girin:")
        if new_name:
            button.configure(text=new_name)
            update_json()  # JSON dosyasını güncelle

    button.bind("<Double-1>", on_double_click)

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
    to2_liste = []
    
    def_liste = []  # Fonksiyonları saklayacak liste
    button_functions = []  # Butonların fonksiyon isimlerini saklayacak liste
    
    for i, button in enumerate(buttons):
        button_name = f"button{i+1}"  # Her buton için farklı bir isim oluştur
        button_func_name = f"{button_name}_click"  # Butonun tıklama fonksiyonunun ismi
        
        # Fonksiyon tanımları
        def_liste.append(f"def {button_func_name}():")
        def_liste.append(f"    print('Click Me-{button_name}')")  # Örnek işlev: console'a yazdır
        
        button_functions.append(button_func_name)
        
        new_x = button.winfo_x()
        new_y = button.winfo_y()
        button_width = button.winfo_width()
        button_height = button.winfo_height()
        button_text = button.cget("text")  # Butonun mevcut metnini al
        
        # Python dosyasına yazılacak komutlar
        button_cmd = f"{button_name} = ctk.CTkButton(root, text='{button_text}', width={button_width}, height={button_height}, command={button_func_name})\n{button_name}.place(x={new_x}, y={new_y})"
        to_liste.append(button_cmd)
        
        # Düzenleme için kullanılacak komutlar
        button_cmd_edit = f"create_button({new_x}, {new_y}, {button_width}, {button_height}, text='{button_text}')"
        to2_liste.append(button_cmd_edit)

    
    list_2 = [
        "root.mainloop()",
    ]

    # Fonksiyonları ve diğer komutları JSON dosyasına kaydetme
    with open("output.json", "w") as f:
        json.dump({
            "list_1": list_1,
            "def_liste": def_liste,
            "to_liste": to_liste,
            "to2_liste": to2_liste,
            "list_2": list_2
        }, f, indent=4)
    
def update_entries():
    # Genişlik ve yüksekliği güncelleme
    width = root.winfo_width()
    height = root.winfo_height()
    entry1.delete(0, tk.END)
    entry1.insert(0, str(width))
    entry2.delete(0, tk.END)
    entry2.insert(0, str(height))
    root2.after(1000, update_entries)  # Her 1000ms (1 saniye) sonra güncellemeye devam eder

# Başlangıçta güncellemeyi başlat
update_entries()

root2.mainloop()
root.mainloop()

