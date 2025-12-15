# Aplicación web de HelpDesk

Este proyecto es un sistema de HelpDesk basado en web, desarrollado como proyecto final.
La aplicación permite a los usuarios crear tickets de soporte, ver su estado y comunicarse mediante comentarios. Los administradores y agentes pueden gestionar y eliminar tickets.

## Tecnologías utilizadas
- Python (Flask)
- MariaDB / MySQL
- HTML / CSS
- Bootstrap 5
- JavaScript (jQuery)

## Características
- Autenticación de usuario (inicio/cierre de sesión)
- Acceso basado en roles (ADMIN, AGENTE, USUARIO)
- Crear y ver tickets
- Sistema de comentarios en los tickets
- Eliminación de tickets (solo ADMIN/AGENTE)
- Interfaz de usuario responsiva con Bootstrap

## Instrucciones de configuración
1. Instalar Python 3
2. Instalar dependencias:
3. Create the database in MariaDB/MySQL
4. Configure database credentials in `.env` or `config.py`
5. Run the application:
