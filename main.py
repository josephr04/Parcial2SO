import tkinter as tk
import unicodedata
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from crud import agregar_plato, obtener_platos, actualizar_plato, eliminar_plato
from Categoria import CategoriaGUI
COLOR_BG = "#f6f6f6"
COLOR_ACCENT = "#FF6B6B"
COLOR_BTN = "#4ECDC4"
COLOR_TXT = "#333"

class RestauranteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🍴 Restaurante App")
        self.root.geometry("600x400")
        self.root.config(bg=COLOR_BG)
        self.menu_principal()

    # --- MENÚ PRINCIPAL ---
    def menu_principal(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="🍽️ Restaurante", font=("Helvetica", 24, "bold"), bg=COLOR_BG, fg=COLOR_TXT).pack(pady=30)

        tk.Button(self.root, text="📋 Gestión de Platos", font=("Helvetica", 14), bg=COLOR_ACCENT, fg="white",
                  bd=0, width=25, command=self.ventana_platos).pack(pady=10)
        tk.Button(self.root, text="📂 Gestión de Categorías", font=("Helvetica", 14), bg=COLOR_BTN, fg="white",
                  bd=0, width=25, command=self.ventana_categorias).pack(pady=10)
        tk.Button(self.root, text="🖨️ Imprimir", font=("Helvetica", 14), bg="#999", fg="white",
                  bd=0, width=25, command=lambda: messagebox.showinfo("En desarrollo", "Funcionalidad de impresión en desarrollo")).pack(pady=10)

    # --- VENTANA DE PLATOS ---
    def ventana_platos(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("900x600")
        frame = tk.Frame(self.root, bg=COLOR_BG)
        frame.pack(expand=True)

        tk.Label(frame, text="Gestión de Platos", font=("Helvetica", 20, "bold"), bg=COLOR_BG, fg=COLOR_TXT).pack(pady=10)

        form = tk.Frame(frame, bg=COLOR_BG)
        form.pack(pady=10)

        # Campos
        self._add_field(form, "Nombre:", 0)
        self._add_field(form, "Descripción:", 1)
        self._add_field(form, "Precio:", 2)

        tk.Label(form, text="Imagen:", bg=COLOR_BG, fg=COLOR_TXT).grid(row=3, column=0, sticky="e", pady=5)
        self.imagen_path = tk.StringVar()
        tk.Entry(form, textvariable=self.imagen_path, width=30).grid(row=3, column=1, pady=5)
        tk.Button(form, text="Seleccionar", bg=COLOR_BTN, fg="white", bd=0, command=self.seleccionar_imagen).grid(row=3, column=2, padx=5)

        # Miniatura
        self.preview = tk.Label(form, bg="#ddd", width=15, height=5, text="[Sin imagen]")
        self.preview.grid(row=0, column=3, rowspan=4, padx=10)

        # Botones
        btn_frame = tk.Frame(frame, bg=COLOR_BG)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="➕ Agregar", bg=COLOR_ACCENT, fg="white", bd=0, command=self.agregar).pack(side="left", padx=10)
        tk.Button(btn_frame, text="✏️ Actualizar", bg=COLOR_BTN, fg="white", bd=0, command=self.actualizar).pack(side="left", padx=10)
        tk.Button(btn_frame, text="❌ Eliminar", bg="#E94E77", fg="white", bd=0, command=self.eliminar).pack(side="left", padx=10)
        tk.Button(btn_frame, text="🧹 Limpiar", bg="#999", fg="white", bd=0, command=self.limpiar).pack(side="left", padx=10)
        tk.Button(btn_frame, text="🏠 Menú Principal", bg="#555", fg="white", bd=0, command=self.menu_principal).pack(side="left", padx=10)

        # Tabla
        self.tabla = ttk.Treeview(frame, columns=("ID", "Nombre", "Descripción", "Precio", "Imagen"), show="headings", height=10)
        for col in ("ID", "Nombre", "Descripción", "Precio", "Imagen"):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center", width=140)
        self.tabla.pack(pady=10)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_tabla)

        self.cargar_tabla()

    # --- VENTANA DE CATEGORÍAS ---
    def ventana_categorias(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("650x450")
        CategoriaGUI(self.root, on_back=self.menu_principal)

    # --- FUNCIONES AUXILIARES ---
    def _add_field(self, parent, label, row):
        tk.Label(parent, text=label, bg=COLOR_BG, fg=COLOR_TXT).grid(row=row, column=0, sticky="e", pady=5)
        entry = tk.Entry(parent, width=30)
        entry.grid(row=row, column=1, columnspan=2, pady=5)

        # quitar acentos y minúsculas para que el atributo sea fácil de usar
        attr_name = ''.join(
            c for c in unicodedata.normalize('NFD', label[:-1].lower())
            if unicodedata.category(c) != 'Mn'
        )
        setattr(self, attr_name, entry)

    def seleccionar_imagen(self):
        path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")])
        if path:
            self.imagen_path.set(path)
            self.mostrar_preview(path)

    def mostrar_preview(self, path):
        if not os.path.exists(path):
            self.preview.config(image="", text="[Sin imagen]")
            return
        img = Image.open(path)
        img.thumbnail((120, 120))
        self.tk_img = ImageTk.PhotoImage(img)
        self.preview.config(image=self.tk_img, text="")

    def cargar_tabla(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        for plato in obtener_platos():
            self.tabla.insert("", "end", values=plato)

    # --- CRUD ---
    def agregar(self):
        confirmar = messagebox.askokcancel("Confirmar", "¿Deseas agregar este plato?")
        if not confirmar:
            return
        try:
            agregar_plato(self.nombre.get(), self.descripcion.get(), float(self.precio.get()), None, self.imagen_path.get())
            self.cargar_tabla()
            self.limpiar()
            messagebox.showinfo("Éxito", "Plato agregado.")
        except ValueError:
            messagebox.showerror("Error", "Precio inválido.")

    def actualizar(self):
        selected = self.tabla.selection()
        if not selected:
            return messagebox.showwarning("Aviso", "Selecciona un plato.")
        confirmar = messagebox.askokcancel("Confirmar", "¿Deseas actualizar este plato?")
        if not confirmar:
            return
        try:
            id_ = int(self.tabla.item(selected[0])["values"][0])
            actualizar_plato(id_, self.nombre.get(), self.descripcion.get(), float(self.precio.get()), None, self.imagen_path.get())
            self.cargar_tabla()
            self.limpiar()
            messagebox.showinfo("Éxito", "Plato actualizado.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar(self):
        selected = self.tabla.selection()
        if not selected:
            return messagebox.showwarning("Aviso", "Selecciona un plato.")
        id_ = int(self.tabla.item(selected[0])["values"][0])
        if messagebox.askyesno("Confirmar", "¿Eliminar este plato?"):
            eliminar_plato(id_)
            self.cargar_tabla()
            self.limpiar()
            messagebox.showinfo("Eliminado", "Plato eliminado.")

    def limpiar(self):
        self.nombre.delete(0, tk.END)
        self.descripcion.delete(0, tk.END)
        self.precio.delete(0, tk.END)
        self.imagen_path.set("")
        self.preview.config(image="", text="[Sin imagen]")
        self.tabla.selection_remove(self.tabla.selection())

    def seleccionar_tabla(self, event):
        selected = self.tabla.selection()
        if selected:
            vals = self.tabla.item(selected[0])["values"]
            self.nombre.delete(0, tk.END)
            self.nombre.insert(0, vals[1])
            self.descripcion.delete(0, tk.END)
            self.descripcion.insert(0, vals[2])
            self.precio.delete(0, tk.END)
            self.precio.insert(0, vals[3])
            self.imagen_path.set(vals[4] if len(vals) > 4 else "")
            self.mostrar_preview(self.imagen_path.get())

# --- INICIO APP ---
if __name__ == "__main__":
    root = tk.Tk()
    app = RestauranteApp(root)
    root.mainloop()
