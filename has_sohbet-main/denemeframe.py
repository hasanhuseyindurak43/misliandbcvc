import customtkinter as ctk
import tkinter as tk
import os

class ResizableFrame(ctk.CTkFrame):
    def __init__(self, master, update_text_function, **kwargs):
        super().__init__(master, **kwargs)
        self.update_text_function = update_text_function

        # Initialize frame color and click counter
        self.frame_color = "white"
        self.click_counter = 0
        self.configure(fg_color=self.frame_color)

        # Initialize theme and resize counters
        self.themes = ["green", "blue", "dark-blue"]
        self.current_theme_index = 0
        self.resize_click_counter = 0

        self.bind("<Button-1>", self.handle_click)
        self.bind("<B1-Motion>", self.do_move)
        self.bind("<ButtonRelease-1>", self.stop_move)

        # Resizing borders
        self.bind("<Button-3>", self.start_resize)
        self.bind("<B3-Motion>", self.do_resize)
        self.bind("<ButtonRelease-3>", self.stop_resize)

        # Initialize variables
        self._drag_data = {"x": 0, "y": 0}
        self._resize_data = {"width": 0, "height": 0, "x": 0, "y": 0}

    def handle_click(self, event):
        self.click_counter += 1
        if self.click_counter >= 3:
            self.frame_color = "black" if self.frame_color == "white" else "white"
            self.configure(fg_color=self.frame_color)
            self.click_counter = 0
            self.update_text()

    def start_move(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def do_move(self, event):
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]
        self.place(x=self.winfo_x() + dx, y=self.winfo_y() + dy)
        self.update_text()

    def stop_move(self, event):
        self._drag_data = {"x": 0, "y": 0}

    def start_resize(self, event):
        self._resize_data["width"] = self.winfo_width()
        self._resize_data["height"] = self.winfo_height()
        self._resize_data["x"] = event.x
        self._resize_data["y"] = event.y

        self.resize_click_counter += 1
        if self.resize_click_counter >= 2:
            # Cycle through themes
            self.current_theme_index = (self.current_theme_index + 1) % len(self.themes)
            self.resize_click_counter = 0

    def do_resize(self, event):
        dx = event.x - self._resize_data["x"]
        dy = event.y - self._resize_data["y"]

        new_width = self._resize_data["width"] + dx
        new_height = self._resize_data["height"] + dy

        if new_width > 50 and new_height > 50:  # Minimum size constraint
            self.configure(width=new_width, height=new_height)
            self.update_text()

    def stop_resize(self, event):
        self._resize_data = {"width": 0, "height": 0, "x": 0, "y": 0}

    def update_text(self):
        # Determine appearance mode based on frame color
        mode = "dark" if self.frame_color == "black" else "light"
        theme = self.themes[self.current_theme_index]

        # Update the text in Tab 2 with the new geometry and mode
        geometry = f'root.geometry("{self.winfo_width()}x{self.winfo_height()}+{self.winfo_rootx()}+{self.winfo_rooty()}")'
        code = f"import customtkinter as ctk\nimport tkinter as tk\n\nroot = ctk.CTk()\n{geometry}\nctk.set_appearance_mode(\"{mode}\")\nctk.set_default_color_theme(\"{theme}\")\nroot.mainloop()\n"
        self.update_text_function(code)

def update_text_widget(text_widget, content):
    text_widget.delete(1.0, tk.END)  # Clear existing text
    text_widget.insert(tk.END, content)
    text_widget.see(tk.END)

def save_and_execute_code():
    code = text_widget.get(1.0, tk.END)  # Get the content of the Text widget
    with open("output.py", "w") as file:
        file.write(code)  # Save the content to output.py
    os.system("python output.py")  # Execute the output.py file

# Create a root window and tab widget
root = ctk.CTk()
root.geometry("600x400")

tabview = ctk.CTkTabview(root)
tabview.pack(fill="both", expand=True)

tab1 = tabview.add("Tab 1")
tab2 = tabview.add("Tab 2")

# Create a frame to hold the Text widget and scrollbar
text_frame = ctk.CTkFrame(tab2)
text_frame.pack(fill="both", expand=True)

# Create the resizable frame in Tab 1
text_widget = tk.Text(text_frame)
scrollbar = tk.Scrollbar(text_frame, command=text_widget.yview)
text_widget.configure(yscrollcommand=scrollbar.set)

frame = ResizableFrame(tab1, lambda content: update_text_widget(text_widget, content), width=200, height=200,
                       fg_color="white")
frame.place(x=100, y=100)

# Place the Text widget and scrollbar in the frame
text_widget.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Add a button to save and execute the code below the Text widget
execute_button = ctk.CTkButton(tab2, text="Python Koduna Çevir ve Çalıştır", command=save_and_execute_code)
execute_button.pack(pady=10)

root.mainloop()
