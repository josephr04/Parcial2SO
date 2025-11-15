import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
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
		self.root.geometry("650x450")
		self.root.config(bg=COLOR_BG)

		self._build_ui()
		self.cargar_categorias()

	def _build_ui(self):
		header = tk.Label(self.root, text="Categorías del Menú", font=(None, 18, "bold"), bg=COLOR_BG)
		header.pack(pady=10)

		form = tk.Frame(self.root, bg=COLOR_BG)
		form.pack(pady=5)

		tk.Label(form, text="Nombre:", bg=COLOR_BG).grid(row=0, column=0, sticky="e", padx=5, pady=5)
		self.entry_nombre = tk.Entry(form, width=40)
		self.entry_nombre.grid(row=0, column=1, pady=5)

		tk.Label(form, text="Imagen:", bg=COLOR_BG).grid(row=1, column=0, sticky="e", padx=5, pady=5)
		self.imagen_path = tk.StringVar()
		tk.Entry(form, textvariable=self.imagen_path, width=30).grid(row=1, column=1, sticky="w", pady=5)
		tk.Button(form, text="Seleccionar...", bg=COLOR_BTN, fg="white", bd=0, command=self.seleccionar_imagen).grid(row=1, column=2, padx=5)

		# Preview
		self.preview = tk.Label(form, text="[Sin imagen]", bg="#ddd", width=18, height=6)
		self.preview.grid(row=0, column=3, rowspan=2, padx=10)

		# Botones
		btn_frame = tk.Frame(self.root, bg=COLOR_BG)
		btn_frame.pack(pady=8)

		tk.Button(btn_frame, text="➕ Agregar", bg=COLOR_ACC, fg="white", bd=0, width=12, command=self.agregar).pack(side="left", padx=6)
		tk.Button(btn_frame, text="✏️ Actualizar", bg=COLOR_BTN, fg="white", bd=0, width=12, command=self.actualizar).pack(side="left", padx=6)
		tk.Button(btn_frame, text="❌ Eliminar", bg="#E94E77", fg="white", bd=0, width=12, command=self.eliminar).pack(side="left", padx=6)
		tk.Button(btn_frame, text="🧹 Limpiar", bg="#999", fg="white", bd=0, width=12, command=self.limpiar).pack(side="left", padx=6)
		if self.on_back:
			tk.Button(btn_frame, text="🏠 Menú Principal", bg="#555", fg="white", bd=0, width=12, command=self.on_back).pack(side="left", padx=6)

		# Tabla
		cols = ("ID", "Nombre", "Imagen")
		self.tree = ttk.Treeview(self.root, columns=cols, show="headings", height=10)
		for c in cols:
			self.tree.heading(c, text=c)
			self.tree.column(c, anchor="center")
		self.tree.pack(padx=10, pady=6, fill="both", expand=True)
		self.tree.bind("<<TreeviewSelect>>", self.seleccionar)

	def seleccionar_imagen(self):
		path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.gif")])
		if path:
			self.imagen_path.set(path)
			self.mostrar_preview(path)

	def mostrar_preview(self, path):
		if not os.path.exists(path):
			self.preview.config(image="", text="[Sin imagen]")
			return
		try:
			img = Image.open(path)
			img.thumbnail((120, 120))
			self._tkimg = ImageTk.PhotoImage(img)
			self.preview.config(image=self._tkimg, text="")
		except Exception:
			self.preview.config(image="", text="[No se puede mostrar]")

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
		ruta = self.imagen_path.get().strip()
		if not nombre:
			return messagebox.showwarning("Aviso", "El nombre es requerido.")
		try:
			controller.crear_categoria(nombre, ruta)
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
		ruta = self.imagen_path.get().strip()
		if not nombre:
			return messagebox.showwarning("Aviso", "El nombre es requerido.")
		try:
			controller.actualizar_categoria(id_, nombre, ruta)
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
		if not messagebox.askyesno("Confirmar", "¿Eliminar esta categoría?"):
			return
		try:
			controller.eliminar_categoria(id_)
			self.cargar_categorias()
			self.limpiar()
			messagebox.showinfo("Eliminado", "Categoría eliminada.")
		except Exception as e:
			messagebox.showerror("Error", str(e))

	def limpiar(self):
		self.entry_nombre.delete(0, tk.END)
		self.imagen_path.set("")
		self.preview.config(image="", text="[Sin imagen]")
		for sel in self.tree.selection():
			self.tree.selection_remove(sel)

	def seleccionar(self, event):
		sel = self.tree.selection()
		if not sel:
			return
		item = self.tree.item(sel[0])["values"]
		self.entry_nombre.delete(0, tk.END)
		self.entry_nombre.insert(0, item[1])
		ruta = item[2] if len(item) > 2 else ""
		self.imagen_path.set(ruta)
		self.mostrar_preview(ruta)


if __name__ == "__main__":
	root = tk.Tk()
	app = CategoriaGUI(root)
	root.mainloop()
