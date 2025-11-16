import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
import mysql.connector
from PIL import Image, ImageTk
from . import controller

COLOR_BG = "#f5f5f5"
COLOR_BTN = "#4ECDC4"
COLOR_ACC = "#FF6B6B"


class CategoriaGUI:
    """Interfaz sencilla para CRUD de categorías (id, nombre, ruta_imagen)."""
    def __init__(self, root, on_back=None):
        self.root = root
        self.on_back = on_back
        self.root.title("Gestión de Categorías")
        self.root.geometry("900x600")
        self.root.config(bg=COLOR_BG)

        self._build_ui()
        self.cargar_categorias()

    def _build_ui(self):

        # ESPACIADOR SUPERIOR PARA BAJAR TODO
        spacer = tk.Frame(self.root, bg=COLOR_BG, height=40)
        spacer.pack()

        header = tk.Label(self.root, text="Categorías del Menú", font=(None, 18, "bold"), bg=COLOR_BG)
        header.pack(pady=20)  # aumentado

        form = tk.Frame(self.root, bg=COLOR_BG)
        form.pack(pady=15)  # aumentado

        tk.Label(form, text="Nombre:", bg=COLOR_BG).grid(row=0, column=0, sticky="e", padx=5, pady=10)
        self.entry_nombre = tk.Entry(form, width=40)
        self.entry_nombre.grid(row=0, column=1, pady=10)

        tk.Label(form, text="Imagen:", bg=COLOR_BG).grid(row=1, column=0, sticky="e", padx=5, pady=10)
        self.imagen_path = tk.StringVar()
        tk.Entry(form, textvariable=self.imagen_path, width=30).grid(row=1, column=1, sticky="w", pady=10)
        tk.Button(form, text="Seleccionar", bg=COLOR_BTN, fg="white", bd=0, 
                  command=self.seleccionar_imagen).grid(row=1, column=2, padx=5)

        # Preview
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
        btn_frame = tk.Frame(self.root, bg=COLOR_BG)
        btn_frame.pack(pady=0)  # aumentado

        tk.Button(btn_frame, text="➕ Agregar", bg=COLOR_ACC, fg="white", bd=0, width=12,
                  command=self.agregar).pack(side="left", padx=8)
        tk.Button(btn_frame, text="✏️ Actualizar", bg=COLOR_BTN, fg="white", bd=0, width=12,
                  command=self.actualizar).pack(side="left", padx=8)
        tk.Button(btn_frame, text="❌ Eliminar", bg="#E94E77", fg="white", bd=0, width=12,
                  command=self.eliminar).pack(side="left", padx=8)
        tk.Button(btn_frame, text="🧹 Limpiar", bg="#999", fg="white", bd=0, width=12,
                  command=self.limpiar).pack(side="left", padx=8)
        if self.on_back:
            tk.Button(btn_frame, text="🏠 Menú Principal", bg="#555", fg="white", bd=0, width=14,
                      command=self.on_back).pack(side="left", padx=8)

        # Tabla
        cols = ("ID", "Nombre", "Imagen")
        self.tree = ttk.Treeview(self.root, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor="center")

        self.tree.pack(padx=30, pady=40, fill="both", expand=True)  # aumentado
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar)

    def seleccionar_imagen(self):
        path_origen = filedialog.askopenfilename(
            initialdir="img/categorias", 
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")]
        )
        
        if path_origen:
            self.ruta_imagen_temporal = path_origen 
            filename = os.path.basename(path_origen)
            self.imagen_path.set(filename)
            self.mostrar_preview(path_origen)

    def mostrar_preview(self, path):
            ruta_completa_imagen = path
            if path and not os.path.isabs(path):
                ruta_completa_imagen = os.path.join(os.getcwd(), "img", "categorias", path)
            if not ruta_completa_imagen or not os.path.exists(ruta_completa_imagen):
                self.preview.config(image=self.placeholder_img, text="Sin imagen")
                return

            try:
                img = Image.open(ruta_completa_imagen)
                img = img.resize((150, 150))
                self.tk_img = ImageTk.PhotoImage(img)
                self.preview.config(image=self.tk_img, text="")
                self.preview.image = self.tk_img
            except Exception as e:
                self.preview.config(image=self.placeholder_img, text="[Error]")
                print(f"Error al cargar imagen: {e}")

    def cargar_categorias(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        try:
            categorias = controller.obtener_categorias()
            for cat in categorias:
                self.tree.insert("", "end", values=cat)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las categorías:\n{e}")

    def agregar(self):
        nombre = self.entry_nombre.get().strip()
        imagen = self.imagen_path.get()
        if not nombre:
            return messagebox.showwarning("Aviso", "El nombre es requerido.")
        
        if not hasattr(self, 'ruta_imagen_temporal') or not self.ruta_imagen_temporal:
                messagebox.showerror("Error de Imagen", "Por favor, seleccione una imagen válida.")
                return
        
        confirmar = messagebox.askokcancel("Confirmar", "¿Deseas agregar esta categoría?")
        if not confirmar:
            return
        
        try:
            CARPETA_DESTINO = os.path.join(os.getcwd(), "img", "categorias")
            os.makedirs(CARPETA_DESTINO, exist_ok=True)
            path_destino = os.path.join(CARPETA_DESTINO, imagen)
            
            shutil.copy2(self.ruta_imagen_temporal, path_destino) 

            controller.crear_categoria(nombre, imagen)
            self.ruta_imagen_temporal = None
            self.cargar_categorias()
            self.limpiar()
            messagebox.showinfo("Éxito", "Categoría agregada.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar(self):
        sel = self.tree.selection()
        if not sel:
            return messagebox.showwarning("Aviso", "Selecciona una categoría.")
        item = self.tree.item(sel[0])["values"]
        id_ = item[0]
        nombre = self.entry_nombre.get().strip()
        imagen = self.imagen_path.get()
        if not nombre:
            return messagebox.showwarning("Aviso", "El nombre es requerido.")
        
        confirmar = messagebox.askokcancel("Confirmar", "¿Deseas actualizar este plato?")
        if not confirmar:
            return
        try:
            # --- Carpeta donde se guardan las imágenes ---
            CARPETA_DESTINO = os.path.join(os.getcwd(), "img", "categorias")
            os.makedirs(CARPETA_DESTINO, exist_ok=True)
            path_destino = os.path.join(CARPETA_DESTINO, imagen)

            # --- Si el usuario seleccionó una nueva imagen temporal ---
            if hasattr(self, 'ruta_imagen_temporal') and self.ruta_imagen_temporal:
                # Borrar imagen anterior si existe
                datos_actuales = self.tree.item(sel[0])["values"]
                imagen_anterior = datos_actuales[2]  # columna "Imagen"
                path_imagen_anterior = os.path.join(CARPETA_DESTINO, imagen_anterior)
                if os.path.exists(path_imagen_anterior):
                    try:
                        os.remove(path_imagen_anterior)
                    except Exception as e:
                        print(f"No se pudo eliminar la imagen anterior: {e}")

                # Copiar la nueva imagen
                shutil.copy2(self.ruta_imagen_temporal, path_destino)
                self.ruta_imagen_temporal = None

            controller.actualizar_categoria(id_, nombre, imagen)
            self.cargar_categorias()
            self.limpiar()
            messagebox.showinfo("Éxito", "Categoría actualizada.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar(self):
        sel = self.tree.selection()
        if not sel:
            return messagebox.showwarning("Aviso", "Selecciona una categoría.")
        
        item = self.tree.item(sel[0])["values"]
        id_ = item[0]
        imagen_filename = str(item[2])

        if not messagebox.askyesno("Confirmar", "¿Eliminar esta categoría?"):
            return
        try:
            controller.eliminar_categoria(id_)
            if imagen_filename:
                CARPETA_IMAGENES = os.path.join(os.getcwd(), "img", "categorias")
                path_completo_imagen = os.path.join(CARPETA_IMAGENES, imagen_filename)
            if os.path.exists(path_completo_imagen):
                os.remove(path_completo_imagen)
            else:
                print(f"Advertencia: El archivo de imagen '{imagen_filename}' no se encontró localmente.")
            self.cargar_categorias()
            self.limpiar()
            messagebox.showinfo("Eliminado", "Categoría eliminada.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def limpiar(self):
        self.entry_nombre.delete(0, tk.END)
        self.imagen_path.set("")
        self.preview.config(image=self.placeholder_img, text="Sin imagen")
        for sel in self.tree.selection():
            self.tree.selection_remove(sel)

    def seleccionar(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])["values"]
        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, item[1])
        self.imagen_path.set(item[2] if len(item) > 2 else "")  # Cambiado vals por item
        self.mostrar_preview(self.imagen_path.get())


if __name__ == "__main__":
    root = tk.Tk()
    app = CategoriaGUI(root)
    root.mainloop()
