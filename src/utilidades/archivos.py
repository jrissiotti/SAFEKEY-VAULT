import json
import os

def guardar_json(ruta, datos):
    """Guarda datos en formato JSON"""
    try:
        directorio = os.path.dirname(ruta)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
        
        with open(ruta, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error al guardar JSON: {e}")
        return False

def cargar_json(ruta):
    """Carga datos desde archivo JSON"""
    try:
        if not os.path.exists(ruta):
            return []
        
        with open(ruta, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    except json.JSONDecodeError:
        print(f"Error: Archivo JSON inválido: {ruta}")
        return []
    except Exception as e:
        print(f"Error al cargar JSON: {e}")
        return []

def guardar_texto(ruta, texto):
    """Guarda texto en archivo"""
    try:
        directorio = os.path.dirname(ruta)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
        
        with open(ruta, 'w', encoding='utf-8') as archivo:
            archivo.write(texto)
        return True
    except Exception as e:
        print(f"Error al guardar texto: {e}")
        return False

def cargar_texto(ruta):
    """Carga texto desde archivo"""
    try:
        if not os.path.exists(ruta):
            return ""
        
        with open(ruta, 'r', encoding='utf-8') as archivo:
            return archivo.read()
    except Exception as e:
        print(f"Error al cargar texto: {e}")
        return ""