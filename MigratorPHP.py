# import argparse
# import os
# import re
# import shutil
# import sys
# import tempfile
# import zipfile
# from urllib.request import urlopen
# from urllib.error import URLError
# from colorama import Fore, Style, init

# init(autoreset=True)

# # Configuraciones que queremos migrar de php.ini viejo al nuevo
# CONFIG_KEYS = [
#     "upload_max_filesize",
#     "post_max_size",
#     "memory_limit",
#     "max_execution_time",
#     "max_input_time",
#     "max_input_vars",
# ]



# # 🔍 Extrae las extensiones activas del archivo php.ini original
# def parse_ini_extensions(filepath):
#     exts = set()
#     with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
#         for line in f:
#             line = line.strip()
#             if line.startswith(';'):
#                 continue
#             m = re.match(r'^extension\s*=\s*(.+)$', line)
#             if m:
#                 ext = m.group(1).strip()
#                 ext = ext.replace('php_', '').replace('.dll', '').replace('.so', '')
#                 exts.add(ext)
#     return list(exts)




# # 🛠️ Extrae configuraciones clave del archivo php.ini original
# def parse_ini_configs(filepath):
#     configs = {}
#     with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
#         for line in f:
#             line = line.strip()
#             if line.startswith(';') or '=' not in line:
#                 continue
#             key, val = map(str.strip, line.split('=', 1))
#             if key in CONFIG_KEYS:
#                 configs[key] = val
#     return configs




# # 🌐 Descarga el ZIP oficial de PHP desde windows.php.net
# def download_php_zip(version, platform, dest):
#     base_url = "https://windows.php.net/downloads/releases/"
#     if platform == "windows":
#         filename = f"php-{version}-Win32-vs16-x64.zip"
#     else:
#         print(f"{Fore.RED}❌ Solo Windows soportado en este prototipo.")
#         sys.exit(1)
#     url = base_url + filename
#     print(f"{Fore.LIGHTBLACK_EX}🔽 Descargando {url} ...")
#     try:
#         with urlopen(url) as response, open(dest, 'wb') as out_file:
#             shutil.copyfileobj(response, out_file)
#     except URLError as e:
#         print(f"{Fore.RED}❌ Error al descargar PHP: {e}")
#         sys.exit(1)



# # 📦 Extrae el archivo ZIP descargado
# def extract_zip(zip_path, extract_to):
#     print(f"{Fore.LIGHTBLACK_EX}📦 Extrayendo {zip_path} ...")
#     with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#         zip_ref.extractall(extract_to)
#     print(f"{Fore.GREEN}✅ Extracción completa.")

# # 📁 Encuentra el root del ZIP extraído que contiene php.ini y carpeta ext
# def find_php_root_dir(base_path):
#     for root, dirs, files in os.walk(base_path):
#         if 'php.ini-production' in files and 'ext' in dirs:
#             return root
#     return None





# # 📝 Genera un nuevo php.ini basado en el template y migrando extensiones + configs
# def generate_new_ini(template_ini_path, extensions, configs, output_path):
#     print(f"{Fore.YELLOW} Generando nuevo php.ini ...")
#     with open(template_ini_path, 'r', encoding='utf-8', errors='ignore') as f:
#         lines = f.readlines()

#     extensions_set = set(extensions)

#     filtered = []
#     for line in lines:
#         # Detectar líneas extension=
#         m = re.match(r'^(\s*);?\s*(extension\s*=\s*(.+))', line, re.IGNORECASE)
#         if m:
#             ext_full = m.group(3).strip()
#             ext_name = ext_full.replace('php_', '').replace('.dll', '').replace('.so', '').lower()
#             if ext_name in extensions_set:
#                 filtered.append(f"extension={ext_name}\n")
#             else:
#                 filtered.append(';' + line if not line.startswith(';') else line)
#         else:
#             skip = False
#             for key in CONFIG_KEYS:
#                 if line.strip().startswith(key):
#                     skip = True
#                     break
#             if not skip:
#                 filtered.append(line)

#     # Agrega las configuraciones migradas al final
#     filtered.append("\n; Migrated configs\n")
#     for key, val in configs.items():
#         filtered.append(f"{key} = {val}\n")

#     with open(output_path, 'w', encoding='utf-8') as f:
#         f.writelines(filtered)
#     print(f"{Fore.GREEN}✅ Nuevo php.ini guardado.")





# # 📁 Copia las DLLs de las extensiones activas a la nueva carpeta /ext
# def copy_extensions(ext_dir_src, ext_dir_dst, extensions):
#     os.makedirs(ext_dir_dst, exist_ok=True)
#     missing = []
#     for ext in extensions:
#         dll_name = f"php_{ext}.dll"
#         src_path = os.path.join(ext_dir_src, dll_name)
#         if os.path.isfile(src_path):
#             shutil.copy2(src_path, os.path.join(ext_dir_dst, dll_name))
#         else:
#             missing.append(ext)
#     if missing:
#         print(f"{Fore.YELLOW}⚠️ No se encontraron DLLs para: {', '.join(missing)}")





# # 🚀 Función principal que realiza la migración
# def main():
#     parser = argparse.ArgumentParser(description="Migrador PHP.ini automático descargando PHP oficial.")
#     parser.add_argument('--php_ini_old', required=True, help='Ruta a php.ini viejo')
#     parser.add_argument('--new_version', required=True, help='Versión PHP nueva (ej: 8.3.5)')
#     parser.add_argument('--platform', default='windows', help='Plataforma: windows (default)')
#     parser.add_argument('--safe', action='store_true', help='Usar php.ini-development en lugar de php.ini-production')
#     args = parser.parse_args()

#     with tempfile.TemporaryDirectory() as tmpdir:
#         zip_path = os.path.join(tmpdir, 'php_new.zip')
#         download_php_zip(args.new_version, args.platform, zip_path)
#         extract_zip(zip_path, tmpdir)

#         extracted_root = find_php_root_dir(tmpdir)
#         if extracted_root is None:
#             print(f"{Fore.RED}❌ No se encontró php.ini-production o carpeta ext.")
#             sys.exit(1)

#         ini_template_name = 'php.ini-development' if args.safe else 'php.ini-production'
#         ini_template = os.path.join(extracted_root, ini_template_name)
#         ext_src_dir = os.path.join(extracted_root, 'ext')

#         extensions = parse_ini_extensions(args.php_ini_old)
#         configs = parse_ini_configs(args.php_ini_old)
#         print("═════════════════════════════════════════════════════════════════════════════════════")
#         print(f"{Fore.CYAN}➠  Extensiones activas detectadas: {Fore.YELLOW}{extensions}{Fore.RESET}")
#         print(f"{Fore.CYAN}➠  Configuraciones migradas: {Fore.YELLOW}{configs}{Fore.RESET}")
#         print("═════════════════════════════════════════════════════════════════════════════════════")

#         output_dir = os.path.abspath(f'php_v{args.new_version}' + ('_safe' if args.safe else ''))
#         os.makedirs(output_dir, exist_ok=True)

#         new_ini_path = os.path.join(output_dir, 'php.ini')
#         generate_new_ini(ini_template, extensions, configs, new_ini_path)

#         ext_dst_dir = os.path.join(output_dir, 'ext')
#         copy_extensions(ext_src_dir, ext_dst_dir, extensions)

#         print(f"{Fore.GREEN}★ Migración completada ➠ : {Fore.LIGHTBLACK_EX}{output_dir}{Fore.RESET}")

       
# if __name__ == '__main__':
#     main()



import argparse
import os
import re
import shutil
import sys
import tempfile
import zipfile
from urllib.request import urlopen
from urllib.error import URLError
from colorama import Fore, Style, init

init(autoreset=True)

# Configuraciones que queremos migrar de php.ini viejo al nuevo
CONFIG_KEYS = [
    "upload_max_filesize",
    "post_max_size",
    "memory_limit",
    "max_execution_time",
    "max_input_time",
    "max_input_vars",
]

# 🔍 Extrae las extensiones activas del archivo php.ini original
def parse_ini_extensions(filepath):
    exts = set()
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if line.startswith(';'):
                continue
            m = re.match(r'^extension\s*=\s*(.+)$', line)
            if m:
                ext = m.group(1).strip()
                ext = ext.replace('php_', '').replace('.dll', '').replace('.so', '')
                exts.add(ext)
    return list(exts)

# 🛠️ Extrae configuraciones clave del archivo php.ini original
def parse_ini_configs(filepath):
    configs = {}
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if line.startswith(';') or '=' not in line:
                continue
            key, val = map(str.strip, line.split('=', 1))
            if key in CONFIG_KEYS:
                configs[key] = val
    return configs

# 🌐 Descarga el ZIP oficial de PHP desde windows.php.net
def download_php_zip(version, platform, dest):
    base_url = "https://windows.php.net/downloads/releases/"
    if platform == "windows":
        filename = f"php-{version}-Win32-vs16-x64.zip"
    else:
        print(f"{Fore.RED}❌ Solo Windows soportado en este prototipo.")
        sys.exit(1)
    url = base_url + filename
    print(f"{Fore.LIGHTBLACK_EX}🔽 Descargando {url} ...")
    try:
        with urlopen(url) as response, open(dest, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
    except URLError as e:
        print(f"{Fore.RED}❌ Error al descargar PHP: {e}")
        sys.exit(1)

# 📦 Extrae el archivo ZIP descargado
def extract_zip(zip_path, extract_to):
    print(f"{Fore.LIGHTBLACK_EX}📦 Extrayendo {zip_path} ...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"{Fore.GREEN}✅ Extracción completa.")

# 📁 Encuentra el root del ZIP extraído que contiene php.ini y carpeta ext
def find_php_root_dir(base_path):
    for root, dirs, files in os.walk(base_path):
        if 'php.ini-production' in files and 'ext' in dirs:
            return root
    return None

# 🧩 Extrae el bloque completo "Module Settings" (comentarios + config) del php.ini viejo
def extract_module_settings_block(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    start_idx = None
    end_idx = None

    def is_delimiter(line):
        line = line.strip()
        return line and set(line) == {';'} and len(line) >= 10

    for i in range(len(lines)-2):
        if is_delimiter(lines[i]) and lines[i+1].strip() == "; Module Settings ;" and is_delimiter(lines[i+2]):
            start_idx = i
            break

    if start_idx is None:
        return []  # No encontrado, devuelve vacío

    for j in range(start_idx+3, len(lines)):
        if is_delimiter(lines[j]):
            end_idx = j
            break

    if end_idx is None:
        end_idx = len(lines)

    return lines[start_idx:end_idx+1]

# 📝 Genera un nuevo php.ini basado en el template y migrando extensiones + configs + bloque Module Settings
def generate_new_ini(template_ini_path, extensions, configs, output_path, module_settings_block=None):
    print(f"{Fore.YELLOW} Generando nuevo php.ini ...")
    with open(template_ini_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    extensions_set = set(extensions)
    filtered = []

    for line in lines:
        m = re.match(r'^(\s*);?\s*(extension\s*=\s*(.+))', line, re.IGNORECASE)
        if m:
            ext_full = m.group(3).strip()
            ext_name = ext_full.replace('php_', '').replace('.dll', '').replace('.so', '').lower()
            if ext_name in extensions_set:
                filtered.append(f"extension={ext_name}\n")
            else:
                filtered.append(';' + line if not line.startswith(';') else line)
        else:
            skip = False
            for key in CONFIG_KEYS:
                if line.strip().startswith(key):
                    skip = True
                    break
            if not skip:
                filtered.append(line)

    # Insertar bloque completo "Module Settings" si existe
    if module_settings_block:
        filtered.append('\n')
        filtered.extend(module_settings_block)
        filtered.append('\n')

    # Finalmente agrega las configuraciones migradas
    filtered.append("; Migrated configs\n")
    for key, val in configs.items():
        filtered.append(f"{key} = {val}\n")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(filtered)

    print(f"{Fore.GREEN}✅ Nuevo php.ini guardado.")

# 📁 Copia las DLLs de las extensiones activas a la nueva carpeta /ext
def copy_extensions(ext_dir_src, ext_dir_dst, extensions):
    os.makedirs(ext_dir_dst, exist_ok=True)
    missing = []
    for ext in extensions:
        dll_name = f"php_{ext}.dll"
        src_path = os.path.join(ext_dir_src, dll_name)
        if os.path.isfile(src_path):
            shutil.copy2(src_path, os.path.join(ext_dir_dst, dll_name))
        else:
            missing.append(ext)
    if missing:
        print(f"{Fore.YELLOW}⚠️ No se encontraron DLLs para: {', '.join(missing)}")

# 🚀 Función principal que realiza la migración
def main():
    parser = argparse.ArgumentParser(description="Migrador PHP.ini automático descargando PHP oficial.")
    parser.add_argument('--php_ini_old', required=True, help='Ruta a php.ini viejo')
    parser.add_argument('--new_version', required=True, help='Versión PHP nueva (ej: 8.3.5)')
    parser.add_argument('--platform', default='windows', help='Plataforma: windows (default)')
    parser.add_argument('--safe', action='store_true', help='Usar php.ini-development en lugar de php.ini-production')
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, 'php_new.zip')
        download_php_zip(args.new_version, args.platform, zip_path)
        extract_zip(zip_path, tmpdir)

        extracted_root = find_php_root_dir(tmpdir)
        if extracted_root is None:
            print(f"{Fore.RED}❌ No se encontró php.ini-production o carpeta ext.")
            sys.exit(1)

        ini_template_name = 'php.ini-development' if args.safe else 'php.ini-production'
        ini_template = os.path.join(extracted_root, ini_template_name)
        ext_src_dir = os.path.join(extracted_root, 'ext')

        extensions = parse_ini_extensions(args.php_ini_old)
        configs = parse_ini_configs(args.php_ini_old)

        # Extraemos el bloque completo "Module Settings" del php.ini viejo
        module_settings_block = extract_module_settings_block(args.php_ini_old)

        print("═════════════════════════════════════════════════════════════════════════════════════")
        print(f"{Fore.CYAN}➠  Extensiones activas detectadas: {Fore.YELLOW}{extensions}{Fore.RESET}")
        print(f"{Fore.CYAN}➠  Configuraciones migradas: {Fore.YELLOW}{configs}{Fore.RESET}")
        if module_settings_block:
            print(f"{Fore.CYAN}➠  Bloque 'Module Settings' extraído y será insertado en el nuevo php.ini.{Fore.RESET}")
        else:
            print(f"{Fore.YELLOW}⚠️ No se encontró bloque 'Module Settings' para copiar.{Fore.RESET}")
        print("═════════════════════════════════════════════════════════════════════════════════════")

        output_dir = os.path.abspath(f'php_v{args.new_version}' + ('_safe' if args.safe else ''))
        os.makedirs(output_dir, exist_ok=True)

        new_ini_path = os.path.join(output_dir, 'php.ini')
        generate_new_ini(ini_template, extensions, configs, new_ini_path, module_settings_block=module_settings_block)

        ext_dst_dir = os.path.join(output_dir, 'ext')
        copy_extensions(ext_src_dir, ext_dst_dir, extensions)

        print(f"{Fore.GREEN}★ Migración completada ➠ : {Fore.LIGHTBLACK_EX}{output_dir}{Fore.RESET}")

if __name__ == '__main__':
    main()
