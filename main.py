import tkinter as tk
import unicodedata
import shutil
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image, ImageTk
import os
from crud import agregar_plato, obtener_platos, actualizar_plato, eliminar_plato, obtener_categorias, existe_plato
from validaciones import validar_dinero
from Categoria import CategoriaGUI
from Imprimir.imprimir_menu import imprimir_menu, vista_previa_menu

COLOR_BG = "#f9f9f9"
COLOR_ACCENT = "#ff825a"
COLOR_BTN = "#14b0ab"
COLOR_IMP = "#2d3741"
COLOR_TXT = "#333"
FUENTE_TXT = "Inter" 

class RestauranteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🍴 Restaurante App")

        ancho, alto = 900, 600
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2) - 50
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

        # Cargar imagen de fondo UNA sola vez
        img = Image.open("img/fondo_restaurante.png")
        self.bg_img = CTkImage(light_image=img, size=(1000, 600))

        self.root.config(bg=COLOR_BG)
        self.menu_principal()

    # --- MENÚ PRINCIPAL ---
    def menu_principal(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.poner_fondo()  # ← Fondo en esta pantalla
        
        center_frame = tk.Frame(self.root, bg=COLOR_BG, padx=20)
        center_frame.pack(expand=True, anchor="n", pady=(80, 0))

        # Logo
        img_logo = Image.open("img/logo.png")
        logo = CTkImage(light_image=img_logo, size=(100, 100))
        
        ctk.CTkLabel(
            master=center_frame,
            image=logo,
            text="",
            fg_color="transparent"
        ).pack(pady=(10, 0))

        ctk.CTkLabel(
            master=center_frame,
            text="RESTAURANTE",
            font=("Arial Black", 30, "bold"),
            text_color=COLOR_TXT,
            fg_color="transparent"
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            master=center_frame,
            text="Menú Principal",
            font=(FUENTE_TXT, 20),
            text_color=COLOR_TXT,
            fg_color="transparent"
        ).pack(pady=(0, 25))    

        ctk.CTkButton(center_frame, 
                    text="📋 Gestión de Platos", 
                    font=(FUENTE_TXT, 18, "bold"),
                    fg_color=COLOR_ACCENT,
                    hover_color="#e6734d",
                    text_color="white",
                    corner_radius=10,
                    width=250,
                    height=45,
                    cursor="hand2",
                    command=self.ventana_platos).pack(pady=10)

        ctk.CTkButton(center_frame, 
                    text="📂 Gestión de Categorías", 
                    font=(FUENTE_TXT, 18, "bold"),
                    fg_color=COLOR_BTN,
                    hover_color="#119b97",
                    text_color="white",
                    corner_radius=10,
                    width=250,
                    height=45,
                    cursor="hand2",
                    command=self.ventana_categorias).pack(pady=10)

        ctk.CTkButton(center_frame, 
                    text="🖨️ Imprimir Menú", 
                    font=(FUENTE_TXT, 18, "bold"),
                    fg_color=COLOR_IMP,
                    hover_color="#1f2933",
                    text_color="white",
                    corner_radius=10,
                    width=250,
                    height=45,
                    cursor="hand2",
                    command=self.ventana_imprimir).pack(pady=10)
        
    def ventana_imprimir(self):
        """
        Ventana para vista previa e impresión del menú
        """
        ventana = tk.Toplevel(self.root)
        ventana.title("Imprimir Menú")
        ventana.geometry("900x700")
   
        ancho, alto = 900, 750
        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2) + 110
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

        ventana.config(bg="#f0f0f0")
        
        # Título
        tk.Label(ventana, text="Vista Previa", 
                font=(FUENTE_TXT, 25, "bold"), fg="#333", 
                bg="#f0f0f0").pack(pady=20)
        
        # Frame para la vista previa
        preview_frame = tk.Frame(ventana, bg="white", relief="solid", bd=2)
        preview_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Canvas con scrollbar para la vista previa
        canvas = tk.Canvas(preview_frame, bg="white")
        scrollbar = tk.Scrollbar(preview_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Generar vista previa
        try:
            img, mensaje = vista_previa_menu("Menú del Restaurante")
            
            if img:
                # Convertir a PhotoImage para mostrar en Tkinter
                photo = ImageTk.PhotoImage(img)
                label_img = tk.Label(scrollable_frame, image=photo, bg="white")
                label_img.image = photo  # Mantener referencia
                label_img.pack(pady=20)
            else:
                tk.Label(scrollable_frame, text=mensaje, 
                        font=(FUENTE_TXT, 14), 
                        fg="red", bg="white").pack(pady=50)
        except Exception as e:
            tk.Label(scrollable_frame, text=f"Error al generar vista previa:\n{str(e)}", 
                    font=(FUENTE_TXT, 12), 
                    fg="red", bg="white").pack(pady=50)
        
        # Frame de botones
        button_frame = tk.Frame(ventana, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        # Botón imprimir
        ctk.CTkButton(button_frame, 
            text="🖨️Imprimir",
            font=(FUENTE_TXT, 15, "bold"),
            fg_color="#27ae60",
            hover_color="#229954",
            text_color="white",
            corner_radius=10,
            width=150,
            height=30,
            cursor="hand2",
            command=lambda: self.ejecutar_impresion()).pack(side="left", padx=10)
        
        # Botón cancelar
        ctk.CTkButton(button_frame, 
            text="❌ Cancelar",
            font=(FUENTE_TXT, 15, "bold"),
            fg_color="#e74c3c",
            hover_color="#c0392b",
            text_color="white",
            corner_radius=10,
            width=150,
            height=30,
            cursor="hand2",
            command=ventana.destroy).pack(side="left", padx=10)
        
        self.ventana_imprimir_ref = ventana


    def ejecutar_impresion(self):
            """
            Ejecuta la impresión del menú
            """
            respuesta = messagebox.askyesno(
                "Confirmar Impresión",
                "¿Deseas imprimir el menú?",
                parent=self.ventana_imprimir_ref
            )
            
            if respuesta:
                try:
                    exito = imprimir_menu("Menú del Restaurante")
                    
                    if exito:
                        if hasattr(self, 'ventana_imprimir_ref'):
                            self.ventana_imprimir_ref.destroy()
                        
                except Exception as e:
                    messagebox.showerror("Error", f"Error al imprimir:\n{str(e)}")

    # --- VENTANA DE PLATOS ---
    def ventana_platos(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        if not hasattr(self, 'titulo_original'):
            self.titulo_original = self.root.title()

        self.root.title("📋 Gestión de Platos")

        self.root.geometry("900x600")
        frame = tk.Frame(self.root, bg=COLOR_BG)
        frame.pack(expand=True)

        tk.Label(frame, text="Gestión de Platos", font=(FUENTE_TXT, 25, "bold"), bg=COLOR_BG, fg=COLOR_TXT).pack(pady=10)

        form = tk.Frame(frame, bg=COLOR_BG)
        form.pack(pady=10)

        vcmd = self.root.register(validar_dinero)
        
        # Campos
        self._add_field(form, "Nombre:", 0)
        self._add_field(form, "Descripción:", 1)

        # Campo de Precio con validación
        tk.Label(form, text="Precio:", bg=COLOR_BG, fg=COLOR_TXT, anchor="w", font=(FUENTE_TXT, 12)).grid(
        row=2, column=0, sticky="w", pady=5)
        self.precio_var = tk.StringVar()
        entry_precio = ctk.CTkEntry(
            form,
            textvariable=self.precio_var,
            height=21,
            width=185,
            border_width=1,
            border_color="#A2A2A2",
            corner_radius=0,
            fg_color="#ffffff",
            text_color="black",
            placeholder_text="Precio...",
            validate="key",
            validatecommand=(vcmd, "%P")
        )
        entry_precio.grid(row=2, column=1, columnspan=2, pady=5)

        # Crear y configurar el estilo del Combobox (ponlo ANTES de crear el combobox)
        estilo_combo = ttk.Style()

        # Configurar la fuente del texto mostrado en el Combobox
        estilo_combo.configure("Modern.TCombobox", 
                            font=(FUENTE_TXT, 14))  # Aumenta el tamaño aquí

        # Configurar la fuente de la lista desplegable
        self.root.option_add("*TCombobox*Listbox*Font", (FUENTE_TXT, 12))  # Para la lista

        # Categoría
        tk.Label(form, text="Categoría:", bg=COLOR_BG, fg=COLOR_TXT, anchor="w", font=(FUENTE_TXT, 12)).grid(row=3, column=0, sticky="w", pady=5)
        self.categorias = obtener_categorias()
        self.categorias_dict = {nombre: id_ for id_, nombre in self.categorias}
        self.categoria_var = tk.StringVar()
        self.categoria_cb = ttk.Combobox(
            form,
            textvariable=self.categoria_var,
            values=list(self.categorias_dict.keys()),
            state="readonly",
            width=35,
            style="Modern.TCombobox"
        )
        self.categoria_cb.grid(row=3, column=1, columnspan=2, pady=5, ipady=3)

        tk.Label(form, text="Imagen:", bg=COLOR_BG, fg=COLOR_TXT, anchor="w", font=(FUENTE_TXT, 12)).grid(row=4, column=0, sticky="w", pady=5)
        self.imagen_path = tk.StringVar()
        ctk.CTkEntry(
            form,
            textvariable=self.imagen_path,
            height=21,
            width=180,
            border_width=1,
            border_color="#A2A2A2",
            corner_radius=0,
            fg_color="#ffffff",
            text_color="black",
            placeholder_text="Ruta de la imagen..."
        ).grid(row=4, column=1, pady=5)

        ctk.CTkButton(form, 
                    text="Seleccionar",
                    font=(FUENTE_TXT, 12, "bold"),
                    fg_color=COLOR_BTN,
                    hover_color="#119b97",
                    text_color="white",
                    corner_radius=6,    
                    width=80,
                    height=21,
                    cursor="hand2",
                    command=self.seleccionar_imagen).grid(row=4, column=2, padx=5)

        # Miniatura
        placeholder = Image.new('RGB', (188, 188), color='#ddd')
        self.placeholder_img = ImageTk.PhotoImage(placeholder)

        # Miniatura con texto centrado sobre la imagen
        self.preview = tk.Label(
            form,
            bg="#ddd",
            image=self.placeholder_img,
            text="Sin imagen",
            compound="center",  # <-- texto centrado sobre la imagen
            font=("Arial", 12, "italic"),
            fg="#555"  # <-- color del texto
        )
        self.preview.grid(row=0, column=3, rowspan=5, padx=10, pady=10)

        # Botones
        btn_frame = tk.Frame(frame, bg=COLOR_BG)
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, 
                 text="➕ Agregar",
                 font=(FUENTE_TXT, 13, "bold"),
                 fg_color=COLOR_ACCENT,
                 hover_color="#e6734d",
                 text_color="white",
                 corner_radius=6,
                 width=80,
                 height=22,
                 cursor="hand2",
                 command=self.agregar).pack(side="left", padx=8)   
             
        ctk.CTkButton(btn_frame, 
                text="✏️ Actualizar",
                font=(FUENTE_TXT, 13, "bold"),
                fg_color=COLOR_BTN,
                hover_color="#119b97",
                text_color="white",
                corner_radius=6,
                width=80,
                height=22,
                cursor="hand2",
                command=self.actualizar).pack(side="left", padx=8)
            
        ctk.CTkButton(btn_frame, 
                    text="❌ Eliminar",
                    font=(FUENTE_TXT, 13, "bold"),
                    fg_color="#E94E77",
                    hover_color="#d63860",
                    text_color="white",
                    corner_radius=6,
                    width=80,
                    height=22,
                    cursor="hand2",
                    command=self.eliminar).pack(side="left", padx=8)
        
        ctk.CTkButton(btn_frame, 
                    text="🧹 Limpiar",
                    font=(FUENTE_TXT, 13, "bold"),
                    fg_color="#999",
                    hover_color="#777",
                    text_color="white",
                    corner_radius=6,
                    width=80,
                    height=22,
                    cursor="hand2",
                    command=self.limpiar).pack(side="left", padx=8)
        
        ctk.CTkButton(btn_frame, 
                    text="🏠 Menú Principal",
                    font=(FUENTE_TXT, 13, "bold"),
                    fg_color="#555",
                    hover_color="#333",
                    text_color="white",
                    corner_radius=6,
                    width=80,
                    height=22,
                    cursor="hand2",
                    command=self.volver_menu_principal).pack(side="left", padx=8)

        # Tabla
        # Crear un estilo para la tabla
        estilo = ttk.Style()
        estilo.configure("Treeview", 
                        font=('Inter', 12),  # Fuente para las filas
                        rowheight=30)        # Altura de las filas (ajusta según el tamaño de fuente)

        estilo.configure("Treeview.Heading", 
                        font=('Inter', 13, 'bold'),
                        foreground=COLOR_TXT)  # Fuente para los encabezados
        
        estilo.map('Treeview',
          background=[('selected', "#9D9D9E")],  # Color de fondo al seleccionar
          foreground=[('selected', '#FFFFFF')]) 

        # Tabla
        self.tabla = ttk.Treeview(frame, columns=("ID", "Nombre", "Descripción", "Precio", "Categoría", "Imagen"), show="headings", height=10)

        # Configurar cada columna con su propio tamaño
        self.tabla.heading("ID", text="ID")
        self.tabla.column("ID", anchor="center", width=50, minwidth=50)

        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.column("Nombre", anchor="center", width=190, minwidth=100)

        self.tabla.heading("Descripción", text="Descripción")
        self.tabla.column("Descripción", anchor="w", width=390, minwidth=150)

        self.tabla.heading("Precio", text="Precio")
        self.tabla.column("Precio", anchor="center", width=100, minwidth=80)

        self.tabla.heading("Categoría", text="Categoría")
        self.tabla.column("Categoría", anchor="center", width=130, minwidth=100)

        self.tabla.heading("Imagen", text="Imagen")
        self.tabla.column("Imagen", anchor="center", width=150, minwidth=100)

        self.tabla.pack(pady=10)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_tabla)

        self.cargar_tabla()

    def volver_menu_principal(self):
        if hasattr(self, 'titulo_original'):
            self.root.title(self.titulo_original)
        
        self.menu_principal()

    # --- VENTANA DE CATEGORÍAS ---
    def ventana_categorias(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("650x450")
        CategoriaGUI(self.root, on_back=self.menu_principal)

    # --- FUNCIONES AUXILIARES ---
    def _add_field(self, parent, label, row):
        tk.Label(parent, text=label, bg=COLOR_BG, fg=COLOR_TXT, anchor="w", font=(FUENTE_TXT, 12)).grid(row=row, column=0, sticky="w", pady=5)
        entry = ctk.CTkEntry(
            parent,
            height=21,
            width=185,
            border_width=1,
            border_color="#A2A2A2",
            corner_radius=0,
            fg_color="#ffffff",
            text_color="black",
        )
        entry.grid(row=row, column=1, columnspan=2, pady=5)

        # quitar acentos y minúsculas para que el atributo sea fácil de usar
        attr_name = ''.join(
            c for c in unicodedata.normalize('NFD', label[:-1].lower())
            if unicodedata.category(c) != 'Mn'
        )
        setattr(self, attr_name, entry)

    def poner_fondo(self):
        fondo = ctk.CTkLabel(self.root, text="", image=self.bg_img)
        fondo.place(x=0, y=0, relwidth=1, relheight=1)

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
                img = img.resize((190, 190))
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
    root = ctk.CTk()
    app = RestauranteApp(root)
    root.mainloop()
