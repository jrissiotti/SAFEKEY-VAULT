import hashlib
import os
from utilidades.archivos import guardar_texto, cargar_texto

intentos_fallidos = 0

def guardar_contraseña_maestra(contraseña):
    """Guarda la contraseña maestra cifrada"""
    hash_contraseña = hashlib.sha256(contraseña.encode()).hexdigest()
    
    if guardar_texto('data/maestra.txt', hash_contraseña):
        return True
    return False

def verificar_contraseña_maestra(contraseña_ingresada):
    """Verifica si la contraseña es correcta"""
    global intentos_fallidos
    
    contraseña_guardada = cargar_texto('data/maestra.txt')
    
    if not contraseña_guardada:
        print("No hay contraseña configurada")
        return False
    
    contraseña_guardada = contraseña_guardada.strip()
    hash_ingresado = hashlib.sha256(contraseña_ingresada.encode()).hexdigest()
    
    if hash_ingresado == contraseña_guardada:
        intentos_fallidos = 0
        return True
    else:
        intentos_fallidos += 1
        print(f"Contraseña incorrecta. Intentos: {intentos_fallidos}/3")
        
        if intentos_fallidos >= 3:
            print("\nSistema bloqueado por seguridad")
            from utilidades.registro_actividades import registrar_accion
            registrar_accion("Sistema bloqueado por intentos fallidos")
            exit()
        
        return False

def cambiar_contraseña_maestra():
    """Permite cambiar la contraseña maestra"""
    contraseña_actual = input("Contraseña actual: ")
    
    if not verificar_contraseña_maestra(contraseña_actual):
        print("Contraseña actual incorrecta")
        return
    
    nueva = input("Nueva contraseña: ")
    confirmar = input("Confirmar contraseña: ")
    
    if nueva != confirmar:
        print("Las contraseñas no coinciden")
        return
    
    if len(nueva) < 6:
        print("La contraseña debe tener al menos 6 caracteres")
        return
    
    if guardar_contraseña_maestra(nueva):
        print("Contraseña cambiada exitosamente")
        from utilidades.registro_actividades import registrar_accion
        registrar_accion("Contraseña maestra cambiada")

def autenticar_usuario():
    """Función principal de autenticación"""
    global intentos_fallidos
    
    if not os.path.exists('data/maestra.txt'):
        print("\nPrimera vez - Configura tu contraseña maestra")
        
        while True:
            contraseña = input("Nueva contraseña maestra: ")
            confirmar = input("Confirmar contraseña: ")
            
            if contraseña != confirmar:
                print("Las contraseñas no coinciden")
                continue
            
            if len(contraseña) < 6:
                print("Mínimo 6 caracteres")
                continue
            
            if guardar_contraseña_maestra(contraseña):
                print("Contraseña configurada")
                from utilidades.registro_actividades import registrar_accion
                registrar_accion("Contraseña maestra configurada inicialmente")
                return True
            else:
                return False
    
    print("\n--- INICIO DE SESIÓN ---")
    
    # Reiniciar intentos si es nuevo inicio
    if intentos_fallidos > 0:
        print(f"Intentos fallidos previos: {intentos_fallidos}")
    
    # Dar hasta 3 intentos
    while intentos_fallidos < 3:
        contraseña = input("Contraseña maestra: ")
        
        # Verificar
        contraseña_guardada = cargar_texto('data/maestra.txt')
        contraseña_guardada = contraseña_guardada.strip()
        hash_ingresado = hashlib.sha256(contraseña.encode()).hexdigest()
        
        if hash_ingresado == contraseña_guardada:
            intentos_fallidos = 0  # Reiniciar contador
            print("Acceso concedido")
            from utilidades.registro_actividades import registrar_accion
            registrar_accion("Usuario autenticado")
            return True
        else:
            intentos_fallidos += 1
            print(f"Contraseña incorrecta. Intentos: {intentos_fallidos}/3")
            
            if intentos_fallidos >= 3:
                print("\nSistema bloqueado por seguridad")
                from utilidades.registro_actividades import registrar_accion
                registrar_accion("Sistema bloqueado por intentos fallidos")
                exit()
            else:
                # Continuar con siguiente intento
                continue
    
    return False