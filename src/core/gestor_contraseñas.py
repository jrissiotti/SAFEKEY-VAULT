from datetime import datetime
from utilidades.archivos import cargar_json, guardar_json
from seguridad.cifrado import cifrar_cesar, cifrar_recursivo, descifrar_cesar, descifrar_recursivo
from seguridad.analizador_fuerza import analizar_fuerza
from utilidades.registro_actividades import registrar_accion

# Catálogo de servicios comunes
SERVICIOS_COMUNES = [
    "Gmail", "Facebook", "Instagram", "Twitter", "Netflix",
    "YouTube", "GitHub", "Spotify", "Amazon", "PayPal",
    "WhatsApp", "Telegram", "Discord", "LinkedIn", "Microsoft"
    , "Google Drive", "Steam", "Epic Games"
]

ARCHIVO_CONTRASEÑAS = 'data/contraseñas.json'

def agregar_contraseña():
    """Agrega una nueva contraseña al sistema"""
    print("\n--- AGREGAR CUENTA ---")
    
    # MOSTRAR CATÁLOGO DE SERVICIOS
    print("\nServicios comunes:")
    for i, servicio in enumerate(SERVICIOS_COMUNES, 1):
        print(f"  {i:2}. {servicio}")
    print("  0. Otro (añadir nuevo servicio)")
    
    # SELECCIONAR O AÑADIR SERVICIO
    while True:
        try:
            opcion = int(input("\nSelecciona un número o 0 para nuevo: "))
            
            if opcion == 0:
                servicio = input("Nombre del nuevo servicio: ").strip()
                if servicio:
                    # Añadir al catálogo si no existe
                    if servicio not in SERVICIOS_COMUNES:
                        SERVICIOS_COMUNES.append(servicio)
                    break
                else:
                    print("El servicio no puede estar vacío")
            
            elif 1 <= opcion <= len(SERVICIOS_COMUNES):
                servicio = SERVICIOS_COMUNES[opcion - 1]
                break
            
            else:
                print("Opción no válida")
                
        except ValueError:
            print("Ingresa un número válido")
    
    # PEDIR USUARIO
    usuario = input("Usuario/email: ").strip()
    
    # PEDIR CONTRASEÑA CON CONFIRMACIÓN
    while True:
        contraseña = input("Contraseña: ").strip()
        confirmar = input("Confirmar contraseña: ").strip()
        
        if contraseña != confirmar:
            print("Las contraseñas no coinciden. Intenta de nuevo.")
            continue
        
        if len(contraseña) < 4:
            print("La contraseña debe tener al menos 4 caracteres.")
            continue
        
        break
    
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
        print(f"✓ Contraseña para '{servicio}' guardada")
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


def consultar_contraseña():
    """Consulta contraseñas por servicio - Muestra cifrada y opción para descifrar"""
    contraseñas = cargar_contraseñas()
    
    if not contraseñas:
        print("No hay contraseñas guardadas")
        return
    
    print("\n" + "="*40)
    print("       CONSULTAR CONTRASEÑA")
    print("="*40)
    
    # 1. OBTENER LISTA ÚNICA DE SERVICIOS
    servicios_unicos = []
    for c in contraseñas:
        if c['servicio'] not in servicios_unicos:
            servicios_unicos.append(c['servicio'])
    
    # 2. MOSTRAR SERVICIOS
    print("\nSelecciona un servicio:")
    for i, servicio in enumerate(servicios_unicos, 1):
        # Contar cuántas cuentas tiene este servicio
        cantidad = sum(1 for c in contraseñas if c['servicio'] == servicio)
        print(f"  {i:2}. {servicio} ({cantidad} cuenta{'s' if cantidad > 1 else ''})")
    
    try:
        # 3. SELECCIONAR SERVICIO
        servicio_opcion = int(input("\nNúmero del servicio: ")) - 1
        
        if servicio_opcion < 0 or servicio_opcion >= len(servicios_unicos):
            print("Número no válido")
            return
        
        servicio_seleccionado = servicios_unicos[servicio_opcion]
        
        # 4. OBTENER CUENTAS DE ESE SERVICIO
        cuentas_del_servicio = []
        for c in contraseñas:
            if c['servicio'] == servicio_seleccionado:
                cuentas_del_servicio.append(c)
        
        # 5. MENÚ DE USUARIOS
        print(f"\n" + "-"*40)
        print(f"SERVICIO: {servicio_seleccionado}")
        print(f"CANTIDAD: {len(cuentas_del_servicio)} cuenta{'s' if len(cuentas_del_servicio) > 1 else ''}")
        print("-"*40)
        
        for i, cuenta in enumerate(cuentas_del_servicio, 1):
            print(f"\n{i}. USUARIO: {cuenta['usuario']}")
            print(f"   Fortaleza: {cuenta['fuerza']}")
            print(f"   Fecha: {cuenta['fecha_registro']}")
            
            # MOSTRAR CONTRASEÑA CIFRADA (como en la antigua opción 2)
            cifrada = cuenta['contraseña_cifrada']
            if len(cifrada) > 20:
                mostrar_cifrado = cifrada[:10] + "..." + cifrada[-10:]
            else:
                mostrar_cifrado = cifrada
            
            print(f"   Contraseña (CIFRADA): {mostrar_cifrado}")
            print(f"   Método: {'César' if cuenta['metodo_cifrado'] == 1 else 'Recursivo'}")
        
        print(f"\n{len(cuentas_del_servicio) + 1}. Mostrar TODAS las contraseñas DESCIFRADAS")
        print(f"  0. Volver al menú principal")
        
        # 6. SELECCIONAR OPCIÓN
        usuario_opcion = int(input("\nOpción: "))
        
        if usuario_opcion == 0:
            return
        
        elif usuario_opcion == len(cuentas_del_servicio) + 1:
            # MOSTRAR TODAS DESCIFRADAS
            print(f"\n" + "="*50)
            print(f"  TODAS LAS CONTRASEÑAS DE: {servicio_seleccionado}")
            print("="*50)
            
            for cuenta in cuentas_del_servicio:
                print(f"\n• Usuario: {cuenta['usuario']}")
                
                if input("  ¿Mostrar contraseña DESCIFRADA? (s/n): ").lower() == 's':
                    if cuenta['metodo_cifrado'] == 1:
                        descifrada = descifrar_cesar(cuenta['contraseña_cifrada'])
                    else:
                        descifrada = descifrar_recursivo(cuenta['contraseña_cifrada'])
                    
                    print(f"  Contraseña: {descifrada}")
                    registrar_accion(f"Contraseña consultada para '{servicio_seleccionado}'")
                else:
                    print("  (Contraseña oculta)")
            
        elif 1 <= usuario_opcion <= len(cuentas_del_servicio):
            # MOSTRAR UNA ESPECÍFICA CON OPCIÓN PARA DESCIFRAR
            cuenta = cuentas_del_servicio[usuario_opcion - 1]
            
            print(f"\n" + "="*40)
            print(f"  DETALLE COMPLETO")
            print("="*40)
            print(f"Servicio: {servicio_seleccionado}")
            print(f"Usuario: {cuenta['usuario']}")
            print(f"Fortaleza: {cuenta['fuerza']}")
            print(f"Fecha: {cuenta['fecha_registro']}")
            print(f"Método cifrado: {'César' if cuenta['metodo_cifrado'] == 1 else 'Recursivo'}")
            
            # Mostrar cifrada completa
            print(f"Contraseña CIFRADA: {cuenta['contraseña_cifrada']}")
            
            # Opción para ver descifrada
            if input("\n¿Mostrar contraseña DESCIFRADA? (s/n): ").lower() == 's':
                if cuenta['metodo_cifrado'] == 1:
                    descifrada = descifrar_cesar(cuenta['contraseña_cifrada'])
                else:
                    descifrada = descifrar_recursivo(cuenta['contraseña_cifrada'])
                
                print(f"\nContraseña DESCIFRADA: {descifrada}")
                registrar_accion(f"Contraseña consultada para '{servicio_seleccionado}'")
        
        else:
            print("Opción no válida")
            
    except ValueError:
        print("Ingresa un número válido")
    except Exception as e:
        print(f"Error: {e}")
        
def editar_contraseña():
    """Edita una contraseña existente - Selecciona servicio primero"""
    contraseñas = cargar_contraseñas()
    
    if not contraseñas:
        print("No hay contraseñas guardadas")
        return
    
    print("\n--- EDITAR CUENTA ---")
    
    # Mostrar CATÁLOGO DE TUS SERVICIOS GUARDADOS
    print("Tus servicios guardados:")
    
    # Crear lista única de servicios (evitar duplicados)
    servicios_unicos = []
    for c in contraseñas:
        if c['servicio'] not in servicios_unicos:
            servicios_unicos.append(c['servicio'])
    
    # Mostrar servicios
    for i, servicio in enumerate(servicios_unicos, 1):
        print(f"  {i}. {servicio}")
    
    # Seleccionar servicio
    try:
        seleccion = int(input("\nSelecciona el número del servicio: ")) - 1
        
        if seleccion < 0 or seleccion >= len(servicios_unicos):
            print("Número no válido")
            return
        
        servicio_seleccionado = servicios_unicos[seleccion]
        
        # Encontrar TODAS las cuentas de ese servicio
        cuentas_del_servicio = []
        for c in contraseñas:
            if c['servicio'] == servicio_seleccionado:
                cuentas_del_servicio.append(c)
        
        # Si hay más de una cuenta para el mismo servicio
        if len(cuentas_del_servicio) > 1:
            print(f"\nHay {len(cuentas_del_servicio)} cuentas para '{servicio_seleccionado}':")
            for i, cuenta in enumerate(cuentas_del_servicio, 1):
                print(f"  {i}. Usuario: {cuenta['usuario']}")
            
            # Seleccionar qué cuenta editar
            cuenta_seleccion = int(input("\nSelecciona el número de cuenta: ")) - 1
            
            if cuenta_seleccion < 0 or cuenta_seleccion >= len(cuentas_del_servicio):
                print("Número no válido")
                return
            
            cuenta_a_editar = cuentas_del_servicio[cuenta_seleccion]
            indice_original = contraseñas.index(cuenta_a_editar)
        
        else:
            # Solo hay una cuenta
            cuenta_a_editar = cuentas_del_servicio[0]
            indice_original = contraseñas.index(cuenta_a_editar)
            print(f"\nEditando cuenta única para '{servicio_seleccionado}'")
            print(f"Usuario actual: {cuenta_a_editar['usuario']}")
        
        # MENÚ DE EDICIÓN
        print("\n¿Qué quieres editar?")
        print("1. Solo cambiar usuario")
        print("2. Cambiar contraseña")
        print("3. Cambiar usuario y contraseña")
        print("4. Cancelar")
        
        opcion_edicion = input("\nOpción: ").strip()
        
        if opcion_edicion == "4":
            print("Edición cancelada")
            return
        
        # CAMBIAR USUARIO (opciones 1 y 3)
        if opcion_edicion in ["1", "3"]:
            nuevo_usuario = input(f"Nuevo usuario (actual: {cuenta_a_editar['usuario']}): ").strip()
            if nuevo_usuario:
                contraseñas[indice_original]['usuario'] = nuevo_usuario
                print("Usuario actualizado")
        
        # CAMBIAR CONTRASEÑA (opciones 2 y 3)
        if opcion_edicion in ["2", "3"]:
            nueva_contraseña = input("Nueva contraseña: ").strip()
            
            if nueva_contraseña:
                # Confirmar contraseña
                confirmar = input("Confirmar contraseña: ").strip()
                
                if nueva_contraseña != confirmar:
                    print("Las contraseñas no coinciden. No se cambió la contraseña.")
                else:
                    # Analizar fortaleza
                    fuerza, puntaje, _ = analizar_fuerza(nueva_contraseña)
                    print(f"Fortaleza nueva: {fuerza}")
                    
                    # Preguntar método de cifrado
                    print(f"\nMétodo actual: {'César' if cuenta_a_editar['metodo_cifrado'] == 1 else 'Recursivo'}")
                    cambiar_metodo = input("¿Cambiar método? (s/n): ").lower().strip()
                    
                    if cambiar_metodo == 's':
                        print("1. César")
                        print("2. Recursivo")
                        try:
                            metodo_opcion = input("Opción (1/2): ").strip()
                            contraseñas[indice_original]['metodo_cifrado'] = 2 if metodo_opcion == "2" else 1
                        except:
                            print("Manteniendo método actual")
                    
                    # Cifrar nueva contraseña
                    metodo = contraseñas[indice_original]['metodo_cifrado']
                    if metodo == 1:
                        contraseñas[indice_original]['contraseña_cifrada'] = cifrar_cesar(nueva_contraseña)
                    else:
                        contraseñas[indice_original]['contraseña_cifrada'] = cifrar_recursivo(nueva_contraseña)
                    
                    # Actualizar fortaleza
                    contraseñas[indice_original]['fuerza'] = fuerza
                    contraseñas[indice_original]['puntaje_fuerza'] = puntaje
                    print("Contraseña actualizada")
        
        # Actualizar fecha
        contraseñas[indice_original]['fecha_registro'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Guardar cambios
        if guardar_contraseñas(contraseñas):
            print(f"\n✓ '{servicio_seleccionado}' actualizado correctamente")
            registrar_accion(f"Contraseña editada para '{servicio_seleccionado}'")
        else:
            print("Error al guardar cambios")
            
    except ValueError:
        print("Ingresa un número válido")
    except Exception as e:
        print(f"Error: {e}")
def eliminar_contraseña():
    """Elimina una contraseña - Primero servicio, luego cuenta"""
    contraseñas = cargar_contraseñas()
    
    if not contraseñas:
        print("No hay contraseñas guardadas")
        return
    
    print("\n" + "="*40)
    print("       ELIMINAR CUENTA")
    print("="*40)
    
    # 1. OBTENER LISTA ÚNICA DE SERVICIOS
    servicios_unicos = []
    for c in contraseñas:
        if c['servicio'] not in servicios_unicos:
            servicios_unicos.append(c['servicio'])
    
    # 2. MOSTRAR SERVICIOS
    print("\nSelecciona un servicio:")
    for i, servicio in enumerate(servicios_unicos, 1):
        cantidad = sum(1 for c in contraseñas if c['servicio'] == servicio)
        print(f"  {i:2}. {servicio} ({cantidad} cuenta{'s' if cantidad > 1 else ''})")
    
    try:
        # 3. SELECCIONAR SERVICIO
        servicio_opcion = int(input("\nNúmero del servicio: ")) - 1
        
        if servicio_opcion < 0 or servicio_opcion >= len(servicios_unicos):
            print("Número no válido")
            return
        
        servicio_seleccionado = servicios_unicos[servicio_opcion]
        
        # 4. OBTENER CUENTAS DE ESE SERVICIO
        cuentas_del_servicio = []
        for c in contraseñas:
            if c['servicio'] == servicio_seleccionado:
                cuentas_del_servicio.append(c)
        
        # 5. MOSTRAR CUENTAS PARA ESE SERVICIO
        print(f"\n" + "-"*40)
        print(f"SERVICIO: {servicio_seleccionado}")
        print("-"*40)
        
        if len(cuentas_del_servicio) == 1:
            # Solo una cuenta
            cuenta = cuentas_del_servicio[0]
            print(f"\nCuenta única encontrada:")
            print(f"  Usuario: {cuenta['usuario']}")
            print(f"  Fortaleza: {cuenta['fuerza']}")
            print(f"  Fecha: {cuenta['fecha_registro']}")
            
            # CONFIRMAR ELIMINACIÓN
            confirmar = input(f"\n¿Estás SEGURO de eliminar '{servicio_seleccionado}' - '{cuenta['usuario']}'? (s/n): ").lower()
            
            if confirmar == 's':
                contraseñas.remove(cuenta)
                if guardar_contraseñas(contraseñas):
                    print(f"\n✓ Cuenta eliminada: '{servicio_seleccionado}' - '{cuenta['usuario']}'")
                    registrar_accion(f"Contraseña eliminada para '{servicio_seleccionado}'")
                else:
                    print("Error al guardar cambios")
            else:
                print("Eliminación cancelada")
                
        else:
            # Múltiples cuentas
            print(f"Hay {len(cuentas_del_servicio)} cuentas:")
            for i, cuenta in enumerate(cuentas_del_servicio, 1):
                print(f"\n{i}. USUARIO: {cuenta['usuario']}")
                print(f"   Fortaleza: {cuenta['fuerza']}")
                print(f"   Fecha: {cuenta['fecha_registro']}")
            
            # 6. SELECCIONAR QUÉ CUENTA ELIMINAR
            cuenta_opcion = int(input(f"\nSelecciona el número de cuenta a eliminar (1-{len(cuentas_del_servicio)}): "))
            
            if 1 <= cuenta_opcion <= len(cuentas_del_servicio):
                cuenta_a_eliminar = cuentas_del_servicio[cuenta_opcion - 1]
                
                # 7. CONFIRMAR ELIMINACIÓN (DOBLE CONFIRMACIÓN)
                print(f"\n" + "!"*50)
                print(f"  ¡ATENCIÓN! Vas a eliminar:")
                print(f"  Servicio: {servicio_seleccionado}")
                print(f"  Usuario: {cuenta_a_eliminar['usuario']}")
                print(f"  Fecha de registro: {cuenta_a_eliminar['fecha_registro']}")
                print("!"*50)
                
                confirmar1 = input(f"\n¿Estás SEGURO de eliminar esta cuenta? (s/n): ").lower()
                
                if confirmar1 == 's':
                    # SEGUNDA CONFIRMACIÓN
                    confirmar2 = input("¿REALMENTE estás seguro? Esta acción NO se puede deshacer. (s/n): ").lower()
                    
                    if confirmar2 == 's':
                        contraseñas.remove(cuenta_a_eliminar)
                        if guardar_contraseñas(contraseñas):
                            print(f"\n✓✓ Cuenta ELIMINADA permanentemente: '{servicio_seleccionado}' - '{cuenta_a_eliminar['usuario']}'")
                            registrar_accion(f"Contraseña eliminada para '{servicio_seleccionado}'")
                        else:
                            print("Error al guardar cambios")
                    else:
                        print("Eliminación cancelada (segunda confirmación)")
                else:
                    print("Eliminación cancelada")
            else:
                print("Número de cuenta no válido")
                
    except ValueError:
        print("Ingresa un número válido")
    except Exception as e:
        print(f"Error: {e}")
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