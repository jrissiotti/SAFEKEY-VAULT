import os

def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

def validar_entrada_numerica(mensaje, min_valor, max_valor):
    """Pide un número y valida que esté en el rango"""
    while True:
        try:
            entrada = input(mensaje)
            numero = int(entrada)
            
            if min_valor <= numero <= max_valor:
                return numero
            else:
                print(f"Debe ser entre {min_valor} y {max_valor}")
        
        except ValueError:
            print("Ingresa un número válido")