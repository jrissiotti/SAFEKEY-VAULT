from utilidades.archivos import cargar_json

ARCHIVO_CONTRASEÑAS = 'data/contraseñas.json'

def buscar_contraseñas():
    """Menú de búsqueda de contraseñas"""
    while True:
        print("\n=== BUSCAR CONTRASEÑAS ===")
        print("1. Buscar por servicio (recursiva)")
        print("2. Buscar por usuario (recursiva)")
        print("3. Búsqueda parcial (recursiva)")
        print("0. Volver")
        
        try:
            opcion = int(input("\nOpción: "))
        except ValueError:
            print("Ingresa un número")
            continue
        
        if opcion == 0:
            break
        elif opcion == 1:
            buscar_por_servicio()
        elif opcion == 2:
            buscar_por_usuario()
        elif opcion == 3:
            buscar_parcial()
        else:
            print("Opción no válida")

def buscar_por_servicio():
    """Busca por servicio usando recursividad"""
    termino = input("\nServicio a buscar: ").strip().lower()
    
    if not termino:
        print("Ingresa un término")
        return
    
    contraseñas = cargar_json(ARCHIVO_CONTRASEÑAS)
    resultados = buscar_recursiva_general(contraseñas, 'servicio', termino, 0)
    
    mostrar_resultados(resultados, f"Servicio: '{termino}'")

def buscar_por_usuario():
    """Busca por usuario usando recursividad"""
    termino = input("\nUsuario a buscar: ").strip().lower()
    
    if not termino:
        print("Ingresa un término")
        return
    
    contraseñas = cargar_json(ARCHIVO_CONTRASEÑAS)
    resultados = buscar_recursiva_general(contraseñas, 'usuario', termino, 0, exacto=False)
    
    mostrar_resultados(resultados, f"Usuario: '{termino}'")

def buscar_parcial():
    """Búsqueda parcial usando recursividad"""
    termino = input("\nTexto a buscar: ").strip().lower()
    
    if not termino:
        print("Ingresa un término")
        return
    
    contraseñas = cargar_json(ARCHIVO_CONTRASEÑAS)
    resultados = buscar_recursiva_parcial(contraseñas, termino, 0)
    
    mostrar_resultados(resultados, f"Texto: '{termino}'")

def buscar_recursiva_general(lista, campo, valor, indice=0, resultados=None, exacto=True):
    """
    Búsqueda recursiva general
    exacto=True: coincide exactamente
    exacto=False: contiene el valor
    """
    if resultados is None:
        resultados = []
    
    # Caso base
    if indice >= len(lista):
        return resultados
    
    item = lista[indice]
    
    if campo in item:
        campo_valor = item[campo].lower()
        
        if exacto:
            if campo_valor == valor:
                resultados.append(item)
        else:
            if valor in campo_valor:
                resultados.append(item)
    
    # Llamada recursiva
    return buscar_recursiva_general(lista, campo, valor, indice + 1, resultados, exacto)

def buscar_recursiva_parcial(lista, termino, indice=0, resultados=None):
    """Búsqueda parcial recursiva en servicio y usuario"""
    if resultados is None:
        resultados = []
    
    # Caso base
    if indice >= len(lista):
        return resultados
    
    item = lista[indice]
    servicio = item['servicio'].lower()
    usuario = item['usuario'].lower()
    
    if termino in servicio or termino in usuario:
        resultados.append(item)
    
    # Llamada recursiva
    return buscar_recursiva_parcial(lista, termino, indice + 1, resultados)

def mostrar_resultados(resultados, criterio):
    """Muestra resultados de búsqueda"""
    if not resultados:
        print(f"\nNo hay resultados para: {criterio}")
        return
    
    print(f"\n=== RESULTADOS ({len(resultados)}) ===")
    print(f"Criterio: {criterio}")
    
    for i, r in enumerate(resultados, 1):
        print(f"\n{i}. {r['servicio']}")
        print(f"   Usuario: {r['usuario']}")
        print(f"   Fortaleza: {r['fuerza']}")
        
        cifrada = r['contraseña_cifrada']
        if len(cifrada) > 20:
            mostrar = cifrada[:10] + "..." + cifrada[-10:]
        else:
            mostrar = cifrada
        
        print(f"   Contraseña (cifrada): {mostrar}")