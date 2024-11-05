import customtkinter as ctk
import tkinter as tk
root = ctk.CTk()
root.geometry("326x207+350+10")
root.title("My Program")
def button1_click():
    print('Click Me-button1')
button1 = ctk.CTkButton(root, text='Deneme', width=181, height=142, command=button1_click)
button1.place(x=75, y=17)
root.mainloop()
