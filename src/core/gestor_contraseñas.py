from datetime import datetime
from utilidades.archivos import cargar_json, guardar_json
from seguridad.cifrado import cifrar_cesar, cifrar_recursivo, descifrar_cesar, descifrar_recursivo
from seguridad.analizador_fuerza import analizar_fuerza
from utilidades.registro_actividades import registrar_accion

ARCHIVO_CONTRASEÑAS = 'data/contraseñas.json'

def agregar_contraseña():
    """Agrega una nueva contraseña al sistema"""
    print("\n--- AGREGAR CONTRASEÑA ---")
    
    servicio = input("Servicio (ej: Gmail): ").strip()
    usuario = input("Usuario/email: ").strip()
    contraseña = input("Contraseña: ").strip()
    
    if not servicio or not usuario or not contraseña:
        print("Todos los campos son obligatorios")
        return
    
    # Analizar fortaleza
    fuerza, puntaje, _ = analizar_fuerza(contraseña)
    print(f"Fortaleza: {fuerza}")
    
    # Elegir método de cifrado
    print("\nMétodo de cifrado:")
    print("1. César")
    print("2. Recursivo")
    
    metodo = 1
    try:
        opcion = input("Opción (1/2): ")
        if opcion == "2":
            metodo = 2
    except:
        print("Usando César por defecto")
    
    # Cifrar
    if metodo == 1:
        contraseña_cifrada = cifrar_cesar(contraseña)
    else:
        contraseña_cifrada = cifrar_recursivo(contraseña)
    
    # Crear registro
    nueva = {
        "servicio": servicio,
        "usuario": usuario,
        "contraseña_cifrada": contraseña_cifrada,
        "metodo_cifrado": metodo,
        "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "fuerza": fuerza,
        "puntaje_fuerza": puntaje
    }
    
    # Guardar
    contraseñas = cargar_contraseñas()
    contraseñas.append(nueva)
    
    if guardar_contraseñas(contraseñas):
        print(f"Contraseña para '{servicio}' guardada")
        registrar_accion(f"Contraseña agregada para '{servicio}'")

def agregar_contraseña_directa(servicio, usuario, contraseña, metodo=1):
    """Agrega contraseña sin interacción (para generador)"""
    fuerza, puntaje, _ = analizar_fuerza(contraseña)
    
    if metodo == 1:
        contraseña_cifrada = cifrar_cesar(contraseña)
    else:
        contraseña_cifrada = cifrar_recursivo(contraseña)
    
    nueva = {
        "servicio": servicio,
        "usuario": usuario,
        "contraseña_cifrada": contraseña_cifrada,
        "metodo_cifrado": metodo,
        "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "fuerza": fuerza,
        "puntaje_fuerza": puntaje
    }
    
    contraseñas = cargar_contraseñas()
    contraseñas.append(nueva)
    
    if guardar_contraseñas(contraseñas):
        registrar_accion(f"Contraseña agregada para '{servicio}' (generada)")
        return True
    return False

def mostrar_contraseñas():
    """Muestra todas las contraseñas guardadas"""
    contraseñas = cargar_contraseñas()
    
    if not contraseñas:
        print("No hay contraseñas guardadas")
        return
    
    print(f"\n--- CONTRASEÑAS ({len(contraseñas)}) ---")
    
    for i, c in enumerate(contraseñas, 1):
        print(f"\n{i}. {c['servicio']}")
        print(f"   Usuario: {c['usuario']}")
        print(f"   Fortaleza: {c['fuerza']}")
        print(f"   Cifrada: {c['contraseña_cifrada'][:20]}...")

def consultar_contraseña():
    """Consulta y muestra una contraseña específica"""
    contraseñas = cargar_contraseñas()
    
    if not contraseñas:
        print("No hay contraseñas")
        return
    
    print("\nServicios:")
    for i, c in enumerate(contraseñas, 1):
        print(f"   {i}. {c['servicio']}")
    
    try:
        opcion = int(input("\nNúmero: ")) - 1
        
        if opcion < 0 or opcion >= len(contraseñas):
            print("Número no válido")
            return
        
        c = contraseñas[opcion]
        
        print(f"\n--- {c['servicio']} ---")
        print(f"Usuario: {c['usuario']}")
        
        if input("\n¿Mostrar contraseña? (s/n): ").lower() == 's':
            if c['metodo_cifrado'] == 1:
                descifrada = descifrar_cesar(c['contraseña_cifrada'])
            else:
                descifrada = descifrar_recursivo(c['contraseña_cifrada'])
            
            print(f"Contraseña: {descifrada}")
            registrar_accion(f"Contraseña consultada para '{c['servicio']}'")
            
    except ValueError:
        print("Ingresa un número")

def editar_contraseña():
    """Edita una contraseña existente"""
    contraseñas = cargar_contraseñas()
    
    if not contraseñas:
        print("No hay contraseñas")
        return
    
    print("\n--- EDITAR ---")
    for i, c in enumerate(contraseñas, 1):
        print(f"{i}. {c['servicio']}")
    
    try:
        opcion = int(input("\nNúmero: ")) - 1
        
        if opcion < 0 or opcion >= len(contraseñas):
            print("Número no válido")
            return
        
        c = contraseñas[opcion]
        
        print(f"\nEditando: {c['servicio']}")
        
        nuevo_servicio = input(f"Servicio [{c['servicio']}]: ").strip()
        nuevo_usuario = input(f"Usuario [{c['usuario']}]: ").strip()
        nueva_contraseña = input("Nueva contraseña (enter para no cambiar): ").strip()
        
        if nuevo_servicio:
            c['servicio'] = nuevo_servicio
        if nuevo_usuario:
            c['usuario'] = nuevo_usuario
        
        if nueva_contraseña:
            fuerza, puntaje, _ = analizar_fuerza(nueva_contraseña)
            
            if c['metodo_cifrado'] == 1:
                c['contraseña_cifrada'] = cifrar_cesar(nueva_contraseña)
            else:
                c['contraseña_cifrada'] = cifrar_recursivo(nueva_contraseña)
            
            c['fuerza'] = fuerza
            c['puntaje_fuerza'] = puntaje
        
        if guardar_contraseñas(contraseñas):
            print(f"'{c['servicio']}' actualizado")
            registrar_accion(f"Contraseña editada para '{c['servicio']}'")
            
    except ValueError:
        print("Ingresa un número")

def eliminar_contraseña():
    """Elimina una contraseña"""
    contraseñas = cargar_contraseñas()
    
    if not contraseñas:
        print("No hay contraseñas")
        return
    
    print("\n--- ELIMINAR ---")
    for i, c in enumerate(contraseñas, 1):
        print(f"{i}. {c['servicio']}")
    
    try:
        opcion = int(input("\nNúmero: ")) - 1
        
        if opcion < 0 or opcion >= len(contraseñas):
            print("Número no válido")
            return
        
        c = contraseñas[opcion]
        
        if input(f"¿Eliminar '{c['servicio']}'? (s/n): ").lower() == 's':
            contraseñas.pop(opcion)
            
            if guardar_contraseñas(contraseñas):
                print(f"'{c['servicio']}' eliminado")
                registrar_accion(f"Contraseña eliminada para '{c['servicio']}'")
                
    except ValueError:
        print("Ingresa un número")

def listar_servicios():
    """Lista todos los servicios guardados"""
    contraseñas = cargar_contraseñas()
    
    if not contraseñas:
        print("No hay servicios")
        return
    
    print(f"\n--- SERVICIOS ({len(contraseñas)}) ---")
    for i, c in enumerate(contraseñas, 1):
        print(f"{i:2}. {c['servicio']}")

def cargar_contraseñas():
    """Carga contraseñas desde archivo"""
    return cargar_json(ARCHIVO_CONTRASEÑAS)

def guardar_contraseñas(contraseñas):
    """Guarda contraseñas en archivo"""
    return guardar_json(ARCHIVO_CONTRASEÑAS, contraseñas)