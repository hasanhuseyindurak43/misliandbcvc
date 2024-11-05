import cv2
from pyzbar.pyzbar import decode
import customtkinter as ctk
from PIL import Image
import numpy as np
import time
from datetime import datetime, time as dt_time
import sqlite3

def create_database():
    conn = sqlite3.connect('company.db')  # Veritabanı dosyasını oluştur
    cursor = conn.cursor()

    # Admin tablosunu oluştur
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    # Çalışanlar tablosunu oluştur
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL
    )
    ''')

    # QR kod okuma bilgileri için yeni tablo oluştur
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS qr_read_log (
        qr_code_data TEXT PRIMARY KEY,
        read_date TEXT,
        read_time TEXT,
        read_slot TEXT
    )
    ''')

    # Admin kullanıcısını ekle
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', '123')")

    # Örnek çalışanları ekle
    cursor.execute("INSERT OR IGNORE INTO employees (id, first_name, last_name) VALUES (1, 'Murat', 'Kilicarslan')")

    conn.commit()
    conn.close()

class Panel():
    def __init__(self):
        # Initialize the customtkinter theme and mode
        ctk.set_appearance_mode("dark")  # Set the theme to dark mode
        ctk.set_default_color_theme("blue")  # Set the color theme to blue

        # Create the main window
        self.root = ctk.CTk()
        self.root.geometry('310x340')
        self.root.title('Login Panel')

        # Create the login label at the top center
        login_label = ctk.CTkLabel(self.root, text='PANEL GİRİŞ', font=('Arial', 24))
        login_label.pack(pady=(50, 20))  # Add padding to position it at the top

        # Create a frame for the input fields
        input_frame = ctk.CTkFrame(self.root, width=300, height=200)
        input_frame.pack(pady=10)

        # Username label and entry
        username_label = ctk.CTkLabel(input_frame, text='Kullanıcı Adı:', font=('Arial', 14))
        username_label.grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = ctk.CTkEntry(input_frame, width=150)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        # Password label and entry
        password_label = ctk.CTkLabel(input_frame, text='Kullanıcı Şifresi:', font=('Arial', 14))
        password_label.grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = ctk.CTkEntry(input_frame, width=150, show='*')
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Login button at the bottom center of the frame
        login_button = ctk.CTkButton(input_frame, text='GİRİŞ YAP',
                                     command=self.check_login)
        login_button.grid(row=2, columnspan=2, pady=20)

        self.root.mainloop()

    def check_login(self):
        # Get the entered username
        username = self.username_entry.get()
        password = self.password_entry.get()
        correct_username = "Admin"
        correct_password = "123"  # Replace with the actual correct username

        # Check if the username is correct
        if username == correct_username and password == correct_password:
            LoginControl(self.root, username)  # Proceed with login control
        else:
            print("Incorrect username or password. Please try again.")

class LoginControl():
    def __init__(self, root, kuladi):

        # Create a frame for the progress bar to avoid using pack and grid together
        progress_frame = ctk.CTkFrame(root)
        progress_frame.pack(pady=20)

        # Progress bar setup
        progressbar = ctk.CTkProgressBar(progress_frame, orientation="horizontal", width=200)
        progressbar.pack(side="left", padx=(0, 10))
        progressbar.set(0)

        # Progress label setup
        progress_label = ctk.CTkLabel(progress_frame, text="0%")
        progress_label.pack(side="left")

        # Simulate progress (for demonstration purposes)
        for i in range(101):
            root.update_idletasks()  # Update the UI
            progressbar.set(i / 100)  # Set the progress bar value
            progress_label.configure(text=f"{i}%")  # Update the progress label text
            time.sleep(0.05)  # Delay for simulation

        # Once the progress bar is full, close the Panel window after 3 seconds
        root.after(3000, self.close_and_open_panel_two, root)

    def close_and_open_panel_two(self, root):
        root.destroy()  # Close the Panel window
        app = PanelTwo()
        app.mainloop()  # Open PanelTwo

class SolUst1(ctk.CTkFrame):
    def __init__(self, master, result_label, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(height=245, width=245)
        self.grid_propagate(False)
        self.result_label = result_label

        self.qr_read_log = {}

        try:
            self.cap = cv2.VideoCapture(0)
        except Exception as e:
            self.cap = cv2.VideoCapture(2)

        self.video_label = ctk.CTkLabel(self, text='')
        self.video_label.grid(row=0, column=0, padx=0, pady=0)

        self.qr_kod_oku()

    def qr_kod_oku(self):
        ret, frame = self.cap.read()
        if not ret:
            self.after(10, self.qr_kod_oku)
            return

        frame = cv2.resize(frame, (245, 245))
        decoded_objects = decode(frame)

        for obj in decoded_objects:
            points = obj.polygon
            if len(points) == 4:
                pts = [(point.x, point.y) for point in points]
                qr_kod_data = obj.data.decode("utf-8")

                if self.should_process_qr_code(qr_kod_data):
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 255)

                cv2.polylines(frame, [np.array(pts, np.int32)], True, color, 2)

                if self.should_process_qr_code(qr_kod_data):
                    self.check_employee(qr_kod_data)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        ctk_img = ctk.CTkImage(img, size=(245, 245))

        self.video_label.configure(image=ctk_img)
        self.video_label.image = ctk_img

        self.after(10, self.qr_kod_oku)

    def should_process_qr_code(self, qr_kod_data):
        current_time = datetime.now().time()
        current_date = datetime.now().date()

        first_time_slot = (dt_time(7, 19), dt_time(8, 25))
        second_time_slot = (dt_time(16, 50), dt_time(17, 0))

        is_in_first_slot = first_time_slot[0] <= current_time <= first_time_slot[1]
        is_in_second_slot = second_time_slot[0] <= current_time <= second_time_slot[1]

        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM qr_read_log WHERE qr_code_data = ?", (qr_kod_data,))
        result = cursor.fetchone()

        if result:
            last_read_date, last_read_time, last_read_slot = result[1], result[2], result[3]
            same_day = current_date.strftime("%Y-%m-%d") == last_read_date

            if same_day and ((is_in_first_slot and last_read_slot == 'first') or
                             (is_in_second_slot and last_read_slot == 'second')):
                conn.close()
                return False

        if is_in_first_slot:
            cursor.execute(
                "INSERT OR REPLACE INTO qr_read_log (qr_code_data, read_date, read_time, read_slot) VALUES (?, ?, ?, ?)",
                (qr_kod_data, current_date.strftime("%Y-%m-%d"), current_time.strftime("%H:%M:%S"), 'first'))
        elif is_in_second_slot:
            cursor.execute(
                "INSERT OR REPLACE INTO qr_read_log (qr_code_data, read_date, read_time, read_slot) VALUES (?, ?, ?, ?)",
                (qr_kod_data, current_date.strftime("%Y-%m-%d"), current_time.strftime("%H:%M:%S"), 'second'))

        conn.commit()
        conn.close()
        return is_in_first_slot or is_in_second_slot

    def check_employee(self, qr_kod_data):
        try:
            id_str, name = qr_kod_data.strip().split(',', 1)
            first_name, last_name = name.split(' ', 1)
            employee_id = int(id_str)
        except ValueError:
            self.result_label.configure(text='Hatalı QR kod verisi.')
            return

        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM employees WHERE id = ? AND first_name = ? AND last_name = ?",
                       (employee_id, first_name.strip(), last_name.strip()))
        result = cursor.fetchone()

        if result:
            self.result_label.configure(text=f'{first_name} {last_name} adlı çalışan giriş yaptı.')
        else:
            self.result_label.configure(text='Bu bilgilerle eşleşen bir çalışan bulunamadı.')

        conn.close()

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

class SolAlt1(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(height=200)  # Yüksekliği sabit olarak 200 piksel ayarla
        self.grid_propagate(False)  # Otomatik boyutlandırmayı devre dışı bırak

        # Çerçeveye widget ekle, örneğin:
        self.label = ctk.CTkLabel(self, text="Sol Alt Frame")
        self.label.grid(row=0, column=0, padx=20)

class SagOrta1(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Sonuç etiketi
        self.result_label = ctk.CTkLabel(self, text="QR Kod Sonucu: ")
        self.result_label.grid(row=0, column=0, padx=20)

    def update_result(self, text):
        self.result_label.configure(text=text)

class PanelTwo(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")  # Koyu tema ayarla
        ctk.set_default_color_theme("blue")  # Renk temasını mavi yap

        # Ana pencereyi oluştur
        self.geometry('900x500')
        self.title('Panel')

        # Grid satır ve sütun yapılandırmasını ayarla
        self.grid_rowconfigure(0, weight=1)  # Sol üst çerçevenin yüksekliği sabit
        self.grid_rowconfigure(1, weight=1)  # Sol alt çerçevenin yüksekliği sabit
        self.grid_columnconfigure(0, minsize=250)  # Soldaki çerçevelerin genişliği minimum 250 piksel olmalı
        self.grid_columnconfigure(1, weight=1)  # Sağdaki çerçeve kalan alanı kaplayacak şekilde genişleyecek

        # Sağ orta çerçeveyi oluştur ve sonuca göre güncelleme yapabilecek şekilde
        self.sagorta = SagOrta1(master=self)
        self.sagorta.grid(row=0, column=1, rowspan=2, padx=(1, 20), pady=20, sticky="nswe")

        # Sol üst çerçeveyi oluştur ve QR kod okuyucu olarak kullan
        self.solust = SolUst1(master=self, result_label=self.sagorta.result_label)
        self.solust.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="ew")

        # Sol alt çerçeveyi oluştur
        self.solalt = SolAlt1(master=self)
        self.solalt.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")

if __name__ == '__main__':
    create_database()
    Panel()
