"""
Generador de Contraseñas - Proyecto Final
"""

import random
from seguridad.analizador_fuerza import analizar_fuerza
from utilidades.registro_actividades import registrar_accion

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


def _guardar_contraseña(contraseña):
    """
    Guarda una contraseña generada en el gestor.
    """
    try:
        from core.gestor_contraseñas import agregar_contraseña_directa
        
        print("\n" + "="*40)
        print("  GUARDAR CONTRASEÑA GENERADA")
        print("="*40)
        
        # LISTA DE SERVICIOS COMUNES (local o importada)
        servicios_comunes = [
            "Gmail", "Facebook", "Instagram", "Twitter", "Netflix",
            "YouTube", "GitHub", "Spotify", "Amazon", "PayPal",
            "WhatsApp", "Telegram", "Discord", "LinkedIn", "Microsoft",
            "Dropbox", "Google Drive", "iCloud", "Steam", "Epic Games"
        ]
        
        # MOSTRAR CATÁLOGO
        print("\nServicios comunes:")
        for i, servicio in enumerate(servicios_comunes, 1):
            print(f"  {i:2}. {servicio}")
        print("  0. Otro (añadir nuevo servicio)")
        
        # SELECCIONAR SERVICIO
        while True:
            try:
                opcion = int(input("\nSelecciona un número o 0 para nuevo: "))
                
                if opcion == 0:
                    servicio = input("Nombre del nuevo servicio: ").strip()
                    if not servicio:
                        print("El servicio no puede estar vacío")
                        continue
                    break
                
                elif 1 <= opcion <= len(servicios_comunes):
                    servicio = servicios_comunes[opcion - 1]
                    break
                
                else:
                    print("Opción no válida")
                    
            except ValueError:
                print("Ingresa un número válido")
        
        # PEDIR USUARIO
        usuario = input("Usuario/email: ").strip()
        
        if not usuario:
            print("Usuario no puede estar vacío")
            return
        
        # MOSTRAR Y CONFIRMAR CONTRASEÑA
        print(f"\nContraseña generada: {contraseña}")
        confirmar = input("¿Usar esta contraseña? (s/n): ").lower().strip()
        
        if confirmar != 's':
            print("Operación cancelada")
            return
        
        # ELEGIR MÉTODO DE CIFRADO
        print("\nMétodo de cifrado:")
        print("1. César")
        print("2. Recursivo")
        
        metodo = 1
        try:
            opcion_cifrado = input("Opción (1/2): ").strip()
            if opcion_cifrado == "2":
                metodo = 2
        except:
            print("Usando César por defecto")
        
        # GUARDAR
        if agregar_contraseña_directa(servicio, usuario, contraseña, metodo):
            print(f"\n✓ Contraseña para '{servicio}' guardada exitosamente")
            registrar_accion(f"Contraseña generada guardada para '{servicio}'")
        else:
            print("\nError al guardar la contraseña")
            
    except KeyboardInterrupt:
        print("\nOperación cancelada")
    except Exception as e:
        print(f"Error: {e}")

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