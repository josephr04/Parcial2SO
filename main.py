import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class TablaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("App de Restaurante")
        self.root.geometry("600x400")
        self.root.config(bg="#f2f2f2")

        # --- Texto centrado ---
        label_contenido = tk.Label(
            root,
            text="Contenido",
            font=("Arial", 20, "bold"),
            bg="#f2f2f2",
            fg="#333"
        )
        label_contenido.place(relx=0.5, rely=0.5, anchor="center")

# --- Ejecucion ---
if __name__ == "__main__":
    root = tk.Tk()
    app = TablaApp(root)
    root.mainloop()