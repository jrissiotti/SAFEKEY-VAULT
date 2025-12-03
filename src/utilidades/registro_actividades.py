import os
from datetime import datetime

ARCHIVO_LOG = 'data/log_actividades.txt'

def registrar_accion(accion):
    """Registra una acción en el log"""
    try:
        os.makedirs(os.path.dirname(ARCHIVO_LOG), exist_ok=True)
        
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entrada = f"[{fecha_hora}] {accion}\n"
        
        with open(ARCHIVO_LOG, 'a', encoding='utf-8') as archivo:
            archivo.write(entrada)
        
        return True
    except Exception as e:
        print(f"Error al registrar acción: {e}")
        return False

def mostrar_log():
    """Muestra el contenido del log"""
    try:
        if not os.path.exists(ARCHIVO_LOG):
            print("El archivo de log no existe")
            return
        
        print("\n=== REGISTRO DE ACTIVIDADES ===")
        
        with open(ARCHIVO_LOG, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
        
        if not lineas:
            print("No hay actividades registradas")
            return
        
        # Mostrar las últimas 20
        if len(lineas) > 20:
            print(f"Mostrando las últimas 20 de {len(lineas)} actividades:")
            lineas = lineas[-20:]
        
        for i, linea in enumerate(lineas, 1):
            print(f"{i:3}. {linea.strip()}")
            
    except Exception as e:
        print(f"Error al leer el log: {e}")