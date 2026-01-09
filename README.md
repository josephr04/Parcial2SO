# Sistema de Gestión de Restaurante

Este es un programa que se encarga de la gestión de platos, menús y generar reportes para un restaurante ficticio. 
Los módulos de plato y menú permiten crear, editar y eliminar datos e incluyen la opción de agregar imágenes representativas. 
El módulo de reportes permite imprimir los menús con sus respectivos platos y precios correspondientes, también incluye la opción de guardar una copia PDF en la dirección especificada.

## Herramientas y Tecnologías
- **Visual Studio Code**: Entorno de desarrollo
- **Python**: Lenguaje de programación principal
- **phpMyAdmin**: Base de datos local para el manejo de datos
- **mysql-connector-python**: Librería para manejar la conexión con la base de datos
- **CustomTkinter**: Framework de diseño que permite crear interfaces modernas 
- **Pillow**: Librería para el manejo de imágenes
- **Shutil**: Módulo para gestionar los archivos del sistema operativo

## Arquitectura de la Aplicación
La aplicación sigue el patrón de diseño **MVC (Modelo–Vista–Controlador)**:

- **Modelo**:  
  Clases que representan los datos del sistema.

- **Vista**:  
  Actividades y fragmentos encargados de mostrar la interfaz de usuario.

- **Controlador**:  
  Manejo de la lógica de negocio, navegación entre pantallas y validaciones.

## Funciones Principales
- Crear, editar y eliminar platos
- Crear, editar y eliminar menús
- Generar reportes e imprimirlos o guardarlos en PDF

## Cómo Ejecutar la Aplicación: 
1. Descarga el proyecto y abre VS Code
2. Instala las librerías especificadas
3. Inicia apache y MySQL en la aplicación de XAMM y entra a la página 
de phpMyAdmin. 
4. En phpMyAdmin importa la base de datos llamada **restaurante.sql** que 
se encuentra dentro de la carpeta raíz del proyecto.
5. Inicia la aplicación desde el archivo **main** en VS Code.

## Colaboradores
- [@Vanegas25](https://github.com/Vanegas25)
- [@josephr04](https://github.com/josephr04)
- [@Moises507](https://github.com/MangoDingo)

## Pantallas
<p align="center">
  <img src="https://github.com/user-attachments/assets/c89b11b9-4970-4436-bbcc-765152a77ac2" width="80%"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/bb615eb6-c332-4ddd-92b9-e884108cd377" width="80%"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/882852f4-075b-4e45-aeb0-e4ea90fa0c9b" width="80%"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/8894212c-7253-4dd2-8709-383fa48ab556" width="80%"/>
</p>


