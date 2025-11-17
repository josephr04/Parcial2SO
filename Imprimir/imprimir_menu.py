"""
Módulo para imprimir el menú del restaurante
"""
import platform
import win32print
import win32ui
if platform.system() == "Windows":
    import win32print
    import win32ui
from PIL import Image, ImageDraw, ImageFont, ImageWin
from database import conectar
import tempfile
import os

def obtener_platos_por_categoria():
    conn = conectar()
    cur = conn.cursor()
    """
    Obtiene todos los platos organizados por categoría
    """
    cur.execute("""
        SELECT c.nombre as categoria, p.nombre, p.precio, p.descripcion
        FROM platos p
        LEFT JOIN categorias c ON p.id_categoria = c.id
        ORDER BY c.nombre, p.nombre
    """)
    
    platos = cur.fetchall()
    
    # Organizar por categoría
    menu = {}
    for plato in platos:
        categoria = plato[0] if plato[0] else "Sin categoría"
        if categoria not in menu:
            menu[categoria] = []
        menu[categoria].append({
            'nombre': plato[1],
            'precio': plato[2],
            'descripcion': plato[3] if plato[3] else ""
        })
    conn.close()
    return menu

def crear_imagen_menu(menu_dict, nombre_restaurante="🍽️ Restaurante"):
    """
    Crea una imagen del menú para imprimir
    """
    # Dimensiones de la página (A4 en píxeles a 300 DPI)
    width, height = 2480, 3508
    
    # Crear imagen
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Intentar cargar fuentes
    try:
        font_titulo = ImageFont.truetype("arial.ttf", 80)
        font_categoria = ImageFont.truetype("arialbd.ttf", 60)
        font_plato = ImageFont.truetype("arial.ttf", 45)
        font_precio = ImageFont.truetype("arialbd.ttf", 45)
        font_desc = ImageFont.truetype("arial.ttf", 35)
    except:
        # Si no encuentra las fuentes, usar la predeterminada
        font_titulo = ImageFont.load_default()
        font_categoria = ImageFont.load_default()
        font_plato = ImageFont.load_default()
        font_precio = ImageFont.load_default()
        font_desc = ImageFont.load_default()
    
    y_position = 100
    margin = 150
    
    # Título
    draw.text((width//2, y_position), nombre_restaurante, 
              fill='#2c3e50', font=font_titulo, anchor="mm")
    
    # Línea decorativa
    y_position += 100
    draw.line([(margin, y_position), (width-margin, y_position)], 
              fill='#3498db', width=5)
    
    y_position += 120
    
    # Dibujar cada categoría
    for categoria, platos in menu_dict.items():
        # Nombre de categoría
        draw.text((margin, y_position), f"• {categoria.upper()}", 
                  fill='#2980b9', font=font_categoria)
        y_position += 100
        
        # Platos de la categoría
        for plato in platos:
            # Verificar si hay espacio suficiente
            if y_position > height - 300:
                break
            
            # Nombre del plato
            draw.text((margin + 50, y_position), plato['nombre'], 
                      fill='#34495e', font=font_plato)
            
            # Precio (alineado a la derecha)
            precio_text = f"${plato['precio']:.2f}"
            draw.text((width - margin - 50, y_position), precio_text, 
                      fill='#27ae60', font=font_precio, anchor="rm")
            
            y_position += 70
            
            # Descripción (si existe)
            if plato['descripcion']:
                # Dividir descripción en líneas si es muy larga
                desc = plato['descripcion']
                max_chars = 80
                if len(desc) > max_chars:
                    desc = desc[:max_chars] + "..."
                
                draw.text((margin + 50, y_position), desc, 
                          fill='#7f8c8d', font=font_desc)
                y_position += 60
            
            y_position += 40
        
        y_position += 80
    
    return img

def imprimir_menu(nombre_restaurante="Restaurante"):
    """
    Imprime el menú del restaurante (Windows y Linux)
    """
    try:
        menu_dict = obtener_platos_por_categoria()
        if not menu_dict:
            return False, "No hay platos en el menú para imprimir"

        # Crear imagen a imprimir
        img = crear_imagen_menu(menu_dict, nombre_restaurante)

        # Guardar en archivo temporal como PDF o PNG
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_path = temp_file.name
        temp_file.close()

        # Guardar imagen como PDF
        img.save(temp_path, "PDF")

        # Detectar Windows vs Linux
        sistema = platform.system()

        # ==============================
        #       IMPRESIÓN EN WINDOWS
        # ==============================
        if sistema == "Windows":
            printer_name = win32print.GetDefaultPrinter()

            hDC = win32ui.CreateDC()
            hDC.CreatePrinterDC(printer_name)
            hDC.StartDoc("Menú del Restaurante")
            hDC.StartPage()

            bmp = Image.open(temp_path)
            dib = ImageWin.Dib(bmp)

            printer_width = hDC.GetDeviceCaps(110)
            printer_height = hDC.GetDeviceCaps(111)

            scale = min(printer_width / bmp.size[0], printer_height / bmp.size[1])
            new_width = int(bmp.size[0] * scale)
            new_height = int(bmp.size[1] * scale)

            x = (printer_width - new_width) // 2
            y = (printer_height - new_height) // 2

            dib.draw(hDC.GetHandleOutput(), (x, y, x + new_width, y + new_height))

            hDC.EndPage()
            hDC.EndDoc()
            hDC.DeleteDC()

        # ==============================
        #        IMPRESIÓN EN LINUX
        # ==============================
        else:
            import cups
            conn = cups.Connection()

            printers = conn.getPrinters()
            if not printers:
                return False, "No hay impresoras disponibles en Linux"

            # Usa la primera impresora encontrada
            printer = list(printers.keys())[0]

            # Enviar PDF a la impresora
            conn.printFile(printer, temp_path, "Menú del Restaurante", {})

        # Eliminar archivo temporal
        os.unlink(temp_path)

        return True, "Impresión enviada correctamente"

    except Exception as e:
        return False, f"Error al imprimir: {str(e)}"

def vista_previa_menu(nombre_restaurante="🍽️ Restaurante"):
    """
    Muestra una vista previa del menú antes de imprimir
    """
    try:
        menu_dict = obtener_platos_por_categoria()
        
        if not menu_dict:
            return None, "No hay platos en el menú"
        
        img = crear_imagen_menu(menu_dict, nombre_restaurante)
        
        # Redimensionar para vista previa (más pequeño)
        img.thumbnail((800, 1131), Image.Resampling.LANCZOS)
        
        return img, "Vista previa generada"
        
    except Exception as e:
        return None, f"Error al generar vista previa: {str(e)}"