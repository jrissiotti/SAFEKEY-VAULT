"""
Generador de Contraseñas - Proyecto Final
"""

import random
from seguridad.analizador_fuerza import analizar_fuerza

# Caracteres disponibles (definidos manualmente sin usar string)
LETRAS = "abcdefghijklmnopqrstuvwxyz"
NUMEROS = "0123456789"
SIMBOLOS = "!@#$%&*"


def generar_contraseña():
    """Menú principal del generador"""
    print("\n=== GENERADOR DE CONTRASEÑAS ===")
    print("1. Generar contraseña segura")
    print("2. Ver fortaleza de contraseña")
    print("0. Volver")
    
    opcion = input("\nOpción: ")
    
    if opcion == "1":
        _menu_generacion()
    elif opcion == "2":
        _ver_fortaleza()
    elif opcion == "0":
        return
    else:
        print("Opción no válida")


def _menu_generacion():
    """Menú de generación"""
    print("\n--- GENERAR CONTRASEÑA ---")
    
    # Pedir longitud
    while True:
        try:
            longitud = int(input("Longitud (8-16): "))
            if 8 <= longitud <= 16:
                break
            print("Debe ser 8-16")
        except:
            print("Ingresa un número")
    
    # Generar
    contra = _crear_contraseña(longitud)
    
    if contra:
        print(f"\nContraseña: {contra}")
        
        # Mostrar fortaleza
        fuerza, puntaje, _ = analizar_fuerza(contra)
        print(f"Fortaleza: {fuerza}")
        
        # Preguntar si guardar
        if input("\n¿Guardar esta contraseña? (s/n): ").lower() == 's':
            _guardar_contraseña(contra)


def _crear_contraseña(longitud):
    """Crea una contraseña aleatoria"""
    # Mezclar todos los caracteres
    todos = LETRAS + LETRAS.upper() + NUMEROS + SIMBOLOS
    
    # Asegurar al menos uno de cada tipo
    contra = [
        random.choice(LETRAS),           # minúscula
        random.choice(LETRAS.upper()),   # mayúscula  
        random.choice(NUMEROS),          # número
        random.choice(SIMBOLOS)          # símbolo
    ]
    
    # Completar con caracteres aleatorios
    while len(contra) < longitud:
        contra.append(random.choice(todos))
    
    # Mezclar y convertir a string
    random.shuffle(contra)
    return ''.join(contra)


def _guardar_contraseña(contra):
    """Guarda la contraseña en el gestor"""
    try:
        from core.gestor_contraseñas import agregar_contraseña_directa
        
        servicio = input("Servicio: ").strip()
        usuario = input("Usuario: ").strip()
        
        if servicio and usuario:
            if agregar_contraseña_directa(servicio, usuario, contra, 1):
                print("Contraseña guardada")
            else:
                print("Error al guardar")
        else:
            print("Faltan datos")
            
    except ImportError:
        print("No se puede guardar ahora")


def _ver_fortaleza():
    """Analiza la fortaleza de una contraseña"""
    print("\n--- ANALIZAR FORTALEZA ---")
    contra = input("Ingresa contraseña: ")
    
    if contra:
        fuerza, puntaje, _ = analizar_fuerza(contra)
        print(f"\nResultado: {fuerza}")
        
        # Consejos simples
        if len(contra) < 8:
            print("- Muy corta, usa 8+ caracteres")
        if contra.islower():
            print("- Añade mayúsculas")
        if contra.isalpha():
            print("- Añade números")
        if contra.isalnum():
            print("- Añade símbolos (!@#$%&*)")
    else:
        print("No ingresaste contraseña")


# Para usar desde main.py
def main_generador():
    """Función principal para llamar desde main.py"""
    generar_contraseña()