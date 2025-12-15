# Manual Técnico – HelpDesk

## Descripción General
El sistema HelpDesk es una aplicación web desarrollada con Flask y MariaDB
que permite la gestión de tickets de soporte.

## Tecnologías Utilizadas
- Python con Flask
- MariaDB / MySQL
- HTML, CSS, Bootstrap
- JavaScript y jQuery

## Estructura del Proyecto
- app.py: lógica principal del sistema
- templates/: archivos HTML
- static/: archivos CSS y JavaScript
- docs/: documentación del proyecto

## Base de Datos
La base de datos contiene las siguientes tablas:
- users
- tickets
- ticket_comments

## Instalación
1. Clonar o copiar el proyecto.
2. Crear la base de datos.
3. Configurar credenciales en `config.py` o `.env`.
4. Instalar dependencias con:
5. Ejecutar:


## Roles del Sistema
- ADMIN: gestión total del sistema.
- AGENT: manejo de tickets.
- USER: creación y seguimiento de tickets.

*Existe una vista exclusiva para ADMIN que muestra los usuarios del sistema.
