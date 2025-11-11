import tkinter as tk
import unicodedata
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from crud import agregar_plato, obtener_platos, actualizar_plato, eliminar_plato, obtener_categorias

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
                  bd=0, width=25, command=lambda: messagebox.showinfo("En desarrollo", "Esta sección está en desarrollo")).pack(pady=10)
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

        # Categoría
        tk.Label(form, text="Categoría:", bg=COLOR_BG, fg=COLOR_TXT).grid(row=3, column=0, sticky="e", pady=5)
        self.categorias = obtener_categorias()
        self.categorias_dict = {nombre: id_ for id_, nombre in self.categorias}
        self.categoria_var = tk.StringVar()
        self.categoria_cb = ttk.Combobox(form, textvariable=self.categoria_var, values=list(self.categorias_dict.keys()), state="readonly", width=28)
        self.categoria_cb.grid(row=3, column=1, columnspan=2, pady=5)

        tk.Label(form, text="Imagen:", bg=COLOR_BG, fg=COLOR_TXT).grid(row=4, column=0, sticky="e", pady=5)
        self.imagen_path = tk.StringVar()
        tk.Entry(form, textvariable=self.imagen_path, width=30).grid(row=4, column=1, pady=5)
        tk.Button(form, text="Seleccionar", bg=COLOR_BTN, fg="white", bd=0, command=self.seleccionar_imagen).grid(row=4, column=2, padx=5)

        # Miniatura
        placeholder = Image.new('RGB', (148, 148), color='#ddd')
        self.placeholder_img = ImageTk.PhotoImage(placeholder)

        # Miniatura con texto centrado sobre la imagen
        self.preview = tk.Label(
            form,
            bg="#ddd",
            image=self.placeholder_img,
            text="Sin imagen",
            compound="center",  # <-- texto centrado sobre la imagen
            font=("Arial", 10, "italic"),
            fg="#555"  # <-- color del texto
        )
        self.preview.grid(row=0, column=3, rowspan=5, padx=10, pady=10)

        # Botones
        btn_frame = tk.Frame(frame, bg=COLOR_BG)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="➕ Agregar", bg=COLOR_ACCENT, fg="white", bd=0, command=self.agregar).pack(side="left", padx=10)
        tk.Button(btn_frame, text="✏️ Actualizar", bg=COLOR_BTN, fg="white", bd=0, command=self.actualizar).pack(side="left", padx=10)
        tk.Button(btn_frame, text="❌ Eliminar", bg="#E94E77", fg="white", bd=0, command=self.eliminar).pack(side="left", padx=10)
        tk.Button(btn_frame, text="🧹 Limpiar", bg="#999", fg="white", bd=0, command=self.limpiar).pack(side="left", padx=10)
        tk.Button(btn_frame, text="🏠 Menú Principal", bg="#555", fg="white", bd=0, command=self.menu_principal).pack(side="left", padx=10)

        # Tabla
        self.tabla = ttk.Treeview(frame, columns=("ID", "Nombre", "Descripción", "Precio", "Categoría", "Imagen"), show="headings", height=10)
        for col in ("ID", "Nombre", "Descripción", "Precio", "Categoría", "Imagen"):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center", width=140)
        self.tabla.pack(pady=10)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_tabla)

        self.cargar_tabla()

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
        path = filedialog.askopenfilename(
            initialdir="img/platos",  # Abrir directamente en esa carpeta
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")]
        )
        if path:
            # Guardar solo el nombre del archivo
            filename = os.path.basename(path)
            self.imagen_path.set(filename)
            self.mostrar_preview(filename)

    def mostrar_preview(self, path):
        if path and not os.path.isabs(path):
            path = os.path.join("img", "platos", path)

        if not path or not os.path.exists(path):
            self.preview.config(image=self.placeholder_img, text="Sin imagen")
            return

        try:
            img = Image.open(path)
            img = img.resize((150, 150))
            self.tk_img = ImageTk.PhotoImage(img)
            self.preview.config(image=self.tk_img, text="")
            self.preview.image = self.tk_img
        except Exception as e:
            self.preview.config(image=self.placeholder_img, text="[Error]")
            print(f"Error al cargar imagen: {e}")

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
            id_categoria = self.categorias_dict.get(self.categoria_var.get())
            agregar_plato(self.nombre.get(), self.descripcion.get(), float(self.precio.get()), id_categoria, self.imagen_path.get())
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
            id_categoria = self.categorias_dict.get(self.categoria_var.get())
            actualizar_plato(id_, self.nombre.get(), self.descripcion.get(), float(self.precio.get()), id_categoria, self.imagen_path.get())
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
        self.categoria_var.set("")
        self.imagen_path.set("")
        self.preview.config(image=self.placeholder_img, text="Sin imagen")
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
            self.categoria_var.set(vals[4] if len(vals) > 4 else "")
            self.imagen_path.set(vals[5] if len(vals) > 5 else "")
            self.mostrar_preview(self.imagen_path.get())

# --- INICIO APP ---
if __name__ == "__main__":
    root = tk.Tk()
    app = RestauranteApp(root)
    root.mainloop()
