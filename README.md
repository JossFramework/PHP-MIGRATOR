# PHP-MIGRATOR ★

Herramienta automática para migrar configuraciones y extensiones de un php.ini antiguo a una versión nueva de PHP descargada desde el sitio oficial de Windows.



## Instalación

1. Clona este repositorio:

   `git clone https://github.com/JossFramework/PHP-MIGRATOR.git`

2. Entra a la carpeta:

   `cd PHP-MIGRATOR`

3. Instala la dependencia `colorama` para colores en la terminal (requiere Python 3):

   `pip install colorama`



## Uso

Ejecuta el script `MigratorPHP.py` con los siguientes parámetros:

- `--php_ini_old`: Ruta al archivo `php.ini` viejo que quieres migrar.
- `--new_version`: Versión nueva de PHP a descargar (ejemplo: `8.3.5`).
- `--platform`: Plataforma (por ahora solo `windows` está soportado, es el valor por defecto).
- `--safe`: Parámetro opcional para usar la plantilla `php.ini-development` en lugar de la `php.ini-production`.



## Ejemplos de uso

     python3 MigratorPHP.py --php_ini_old ./php.ini.old --new_version 8.2.29 --safe
 
 ⭐ El parámetro `--safe` es opcional para descargar ➜ `php.ini-development`. Si no se usa, por defecto usa ➜ `php.ini-production`.




## ¿Qué hace?

- Descarga la versión oficial de PHP para Windows en zip.
- Extrae el archivo `php.ini-production` o `php.ini-development` según el parámetro.
- Crea la carpeta `ext` con las extensiones activas.
- Lee las extensiones y configuraciones clave activas en el php.ini.old.
- Genera un nuevo php.ini basado en la plantilla oficial, activando solo las extensiones que tenías y migrando configuraciones importantes (como upload_max_filesize, memory_limit, etc).
- Copia las DLLs necesarias a la nueva carpeta.
- Todo queda en una carpeta nueva llamada `php_version` o `php_version_safe`.



## Beneficios

- Evita tener que hacer la migración manual de configuraciones y extensiones.
- Garantiza que usas la plantilla oficial correcta de PHP para la versión nueva.
- Facilita la actualización de PHP en ambientes Windows con Apache/XAMPP.



## Requisitos

- Python 3
- Paquete `colorama` (`pip install colorama`)
- Windows (por ahora)



## Licencia

MIT License


¡Gracias por usar PHP-MIGRATOR!
