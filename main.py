import tkinter as tk
import unicodedata
import shutil
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from crud import agregar_plato, obtener_platos, actualizar_plato, eliminar_plato, obtener_categorias, existe_plato
from validaciones import validar_dinero
from Categoria import CategoriaGUI
COLOR_BG = "#f4f6f5"
COLOR_ACCENT = "#ff825a"
COLOR_BTN = "#14b0ab"
COLOR_IMP = "#2d3741"
COLOR_TXT = "#333"

class RestauranteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🍴 Restaurante App")
        self.root.geometry("900x600")
        self.root.config(bg=COLOR_BG)
        self.menu_principal()

    # --- MENÚ PRINCIPAL ---
    def menu_principal(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="🍽️ Restaurante", font=("Helvetica", 24, "bold"), bg=COLOR_BG, fg=COLOR_TXT).pack(pady=30)

        tk.Button(self.root, text="📋 Gestión de Platos", font=("Helvetica", 14), bg=COLOR_ACCENT, fg="white",
                  bd=0, width=25, cursor="hand2", command=self.ventana_platos).pack(pady=10)
        tk.Button(self.root, text="📂 Gestión de Categorías", font=("Helvetica", 14), bg=COLOR_BTN, fg="white",
                  bd=0, width=25, cursor="hand2", command=self.ventana_categorias).pack(pady=10)
        tk.Button(self.root, text="🖨️ Imprimir", font=("Helvetica", 14), bg=COLOR_IMP, fg="white",
                  bd=0, width=25, cursor="hand2", command=lambda: messagebox.showinfo("En desarrollo", "Funcionalidad de impresión en desarrollo")).pack(pady=10)

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

        vcmd = self.root.register(validar_dinero)
        
        # Campos
        self._add_field(form, "Nombre:", 0)
        self._add_field(form, "Descripción:", 1)

        # Campo de Precio con validación
        tk.Label(form, text="Precio:", bg=COLOR_BG, fg=COLOR_TXT).grid(
        row=2, column=0, sticky="e", pady=5)
        self.precio_var = tk.StringVar()
        entry_precio = tk.Entry(
            form, 
            textvariable=self.precio_var, 
            width=30,
            
            validate="key", 
            
            validatecommand=(vcmd, '%P') 
        )
        entry_precio.grid(row=2, column=1, columnspan=2, pady=5)

        # Categoría
        tk.Label(form, text="Categoría:", bg=COLOR_BG, fg=COLOR_TXT).grid(row=3, column=0, sticky="e", pady=5)
        self.categorias = obtener_categorias()
        self.categorias_dict = {nombre: id_ for id_, nombre in self.categorias}
        self.categoria_var = tk.StringVar()
        self.categoria_cb = ttk.Combobox(form, textvariable=self.categoria_var, values=list(self.categorias_dict.keys()), state="readonly", width=28, cursor="hand2")
        self.categoria_cb.grid(row=3, column=1, columnspan=2, pady=5)

        tk.Label(form, text="Imagen:", bg=COLOR_BG, fg=COLOR_TXT).grid(row=4, column=0, sticky="e", pady=5)
        self.imagen_path = tk.StringVar()
        tk.Entry(form, textvariable=self.imagen_path, width=30).grid(row=4, column=1, pady=5)
        tk.Button(form, text="Seleccionar", bg=COLOR_BTN, fg="white", cursor="hand2", bd=0, command=self.seleccionar_imagen).grid(row=4, column=2, padx=5)

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

        tk.Button(btn_frame, text="➕ Agregar", bg=COLOR_ACCENT, fg="white", cursor="hand2", bd=0, command=self.agregar).pack(side="left", padx=10)
        tk.Button(btn_frame, text="✏️ Actualizar", bg=COLOR_BTN, fg="white", cursor="hand2", bd=0, command=self.actualizar).pack(side="left", padx=10)
        tk.Button(btn_frame, text="❌ Eliminar", bg="#E94E77", fg="white", cursor="hand2", bd=0, command=self.eliminar).pack(side="left", padx=10)
        tk.Button(btn_frame, text="🧹 Limpiar", bg="#999", fg="white", cursor="hand2", bd=0, command=self.limpiar).pack(side="left", padx=10)
        tk.Button(btn_frame, text="🏠 Menú Principal", bg="#555", fg="white", cursor="hand2", bd=0, command=self.menu_principal).pack(side="left", padx=10)

        # Tabla
        self.tabla = ttk.Treeview(frame, columns=("ID", "Nombre", "Descripción", "Precio", "Categoría", "Imagen"), show="headings", height=10)
        for col in ("ID", "Nombre", "Descripción", "Precio", "Categoría", "Imagen"):
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
        path_origen = filedialog.askopenfilename(
            initialdir="img/platos", 
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
                ruta_completa_imagen = os.path.join(os.getcwd(), "img", "platos", path)
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

    def cargar_tabla(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        for plato in obtener_platos():
            self.tabla.insert("", "end", values=plato)

    # --- CRUD ---
    def agregar(self):
            nombre = self.nombre.get().strip()
            descripcion = self.descripcion.get().strip()
            precio_str = self.precio_var.get().strip()
            categoria = self.categoria_var.get()
            imagen = self.imagen_path.get()
            
            if not nombre or not descripcion or not precio_str or not categoria or not imagen:
                messagebox.showerror("Error de Validación", "Por favor, complete todos los campos.")
                return
            
            if existe_plato(nombre):
                messagebox.showerror("Error de Duplicado", "Este plato ya existe.")
                return
                
            if not hasattr(self, 'ruta_imagen_temporal') or not self.ruta_imagen_temporal:
                messagebox.showerror("Error de Imagen", "Por favor, seleccione una imagen válida.")
                return
                
            confirmar = messagebox.askokcancel("Confirmar", "¿Deseas agregar este plato?")
            if not confirmar:
                return
                
            try:
                CARPETA_DESTINO = os.path.join(os.getcwd(), "img", "platos")
                os.makedirs(CARPETA_DESTINO, exist_ok=True)
                path_destino = os.path.join(CARPETA_DESTINO, imagen)
                
                shutil.copy2(self.ruta_imagen_temporal, path_destino) 
                
                precio_float = float(precio_str) 
                id_categoria = self.categorias_dict.get(categoria)
                agregar_plato(nombre, descripcion, precio_float, id_categoria, imagen)
                
                self.ruta_imagen_temporal = None
                self.cargar_tabla()
                self.limpiar()
                messagebox.showinfo("Éxito", "Plato agregado.")
                
            except ValueError:
                messagebox.showerror("Error", "El valor del Precio no es un número válido.")
            except Exception as e:
                messagebox.showerror("Error de Archivo", f"Error al guardar la imagen o conectar con DB: {e}")

    def actualizar(self):
        selected = self.tabla.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona un plato para actualizar.")
            return

        # --- Obtener datos del formulario ---
        nombre = self.nombre.get().strip()
        descripcion = self.descripcion.get().strip()
        precio_str = self.precio_var.get().strip()
        categoria = self.categoria_var.get()
        imagen = self.imagen_path.get()

        # --- Validaciones ---
        if not nombre or not descripcion or not precio_str or not categoria or not imagen:
            messagebox.showerror("Error de Validación", "Por favor, complete todos los campos.")
            return

        try:
            precio_float = float(precio_str)
        except ValueError:
            messagebox.showerror("Error", "El valor del Precio no es un número válido.")
            return

        confirmar = messagebox.askokcancel("Confirmar", "¿Deseas actualizar este plato?")
        if not confirmar:
            return

        try:
            # --- ID del plato seleccionado ---
            id_ = int(self.tabla.item(selected[0])["values"][0])
            id_categoria = self.categorias_dict.get(categoria)

            # --- Carpeta donde se guardan las imágenes ---
            CARPETA_DESTINO = os.path.join(os.getcwd(), "img", "platos")
            os.makedirs(CARPETA_DESTINO, exist_ok=True)
            path_destino = os.path.join(CARPETA_DESTINO, imagen)

            # --- Si el usuario seleccionó una nueva imagen temporal ---
            if hasattr(self, 'ruta_imagen_temporal') and self.ruta_imagen_temporal:
                # Borrar imagen anterior si existe
                datos_actuales = self.tabla.item(selected[0])["values"]
                imagen_anterior = datos_actuales[5]  # columna "Imagen"
                path_imagen_anterior = os.path.join(CARPETA_DESTINO, imagen_anterior)
                if os.path.exists(path_imagen_anterior):
                    try:
                        os.remove(path_imagen_anterior)
                    except Exception as e:
                        print(f"No se pudo eliminar la imagen anterior: {e}")

                # Copiar la nueva imagen
                shutil.copy2(self.ruta_imagen_temporal, path_destino)
                self.ruta_imagen_temporal = None

            # --- Actualizar datos en la base de datos ---
            actualizar_plato(id_, nombre, descripcion, precio_float, id_categoria, imagen)

            # --- Refrescar tabla y limpiar formulario ---
            self.cargar_tabla()
            self.limpiar()

            messagebox.showinfo("Éxito", "Plato actualizado correctamente.")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un problema al actualizar el plato:\n{e}")


    def eliminar(self):
            selected = self.tabla.selection()
            if not selected:
                return messagebox.showwarning("Aviso", "Selecciona un plato.")
            
            vals = self.tabla.item(selected[0])["values"]
            id_ = int(vals[0])
            imagen_filename = str(vals[5])
            
            if messagebox.askyesno("Confirmar", "¿Eliminar este plato?"):
                try:
                    eliminar_plato(id_)
                    if imagen_filename:
                        CARPETA_IMAGENES = os.path.join(os.getcwd(), "img", "platos")
                        path_completo_imagen = os.path.join(CARPETA_IMAGENES, imagen_filename)
                        if os.path.exists(path_completo_imagen):
                            os.remove(path_completo_imagen)
                        else:
                            print(f"Advertencia: El archivo de imagen '{imagen_filename}' no se encontró localmente.")
                    self.cargar_tabla()
                    self.limpiar()
                    messagebox.showinfo("Eliminado", "Plato eliminado.")
                
                except Exception as e:
                    messagebox.showerror("Error", f"Ocurrió un error al eliminar: {e}")

    def limpiar(self):
        self.nombre.delete(0, tk.END)
        self.descripcion.delete(0, tk.END)
        self.precio_var.set("")
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
            self.precio_var.set(vals[3])
            self.categoria_var.set(vals[4] if len(vals) > 4 else "")
            self.imagen_path.set(vals[5] if len(vals) > 5 else "")
            self.mostrar_preview(self.imagen_path.get())

# --- INICIO APP ---
if __name__ == "__main__":
    root = tk.Tk()
    app = RestauranteApp(root)
    root.mainloop()
