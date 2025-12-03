# src/busqueda/verificador_integridad.py
from utilidades.archivos import cargar_json, guardar_json
from utilidades.registro_actividades import registrar_accion
from seguridad.cifrado import cifrar_cesar

ARCHIVO_CONTRASEÑAS = 'data/contraseñas.json'

def verificar_integridad():
    """Verificación de integridad con recursividad"""
    print("\n" + "="*60)
    print("     VERIFICACIÓN DE INTEGRIDAD")
    print("="*60)
    
    contraseñas = cargar_json(ARCHIVO_CONTRASEÑAS)
    
    if not contraseñas:
        print("No hay contraseñas para verificar")
        return
    
    print(f"Analizando {len(contraseñas)} registros...")
    
    problemas = []
    verificar_recursivo(contraseñas, 0, problemas)
    
    if not problemas:
        print("\nTodos los registros están correctos")
        registrar_accion("Verificación de integridad: sin problemas")
    else:
        print(f"\nSe encontraron {len(problemas)} problemas")
        for i, p in enumerate(problemas, 1):
            print(f"  {i}. {p}")
        
        if input("\n¿Reparar automáticamente? (s/n): ").lower() == 's':
            reparar_problemas(contraseñas, problemas)

def verificar_recursivo(registros, indice, problemas):
    """
    FUNCIÓN RECURSIVA de verificación
    """
    if indice >= len(registros):
        return
    
    reg = registros[indice]
    
    if not reg or not isinstance(reg, dict):
        problemas.append(f"Registro {indice+1}: Vacío o corrupto")
    
    elif 'servicio' not in reg or 'usuario' not in reg or 'contraseña_cifrada' not in reg:
        serv = reg.get('servicio', 'Desconocido')
        problemas.append(f"Registro {indice+1} ({serv}): Faltan campos")
    
    elif not reg.get('servicio') or not reg.get('usuario') or not reg.get('contraseña_cifrada'):
        serv = reg.get('servicio', 'Desconocido')
        problemas.append(f"Registro {indice+1} ({serv}): Campos vacíos")
    
    elif reg.get('metodo_cifrado') not in [1, 2]:
        serv = reg.get('servicio', 'Desconocido')
        problemas.append(f"Registro {indice+1} ({serv}): Método inválido")
    
    elif len(reg.get('contraseña_cifrada', '')) < 4:
        serv = reg.get('servicio', 'Desconocido')
        problemas.append(f"Registro {indice+1} ({serv}): Contraseña muy corta")
    
    verificar_recursivo(registros, indice + 1, problemas)

def reparar_problemas(contraseñas, problemas):
    """Intenta reparar problemas"""
    print("\nReparando...")
    
    # Eliminar corruptos
    original = len(contraseñas)
    contraseñas = [r for r in contraseñas if r and isinstance(r, dict)]
    
    for i, reg in enumerate(contraseñas):
        if 'servicio' not in reg or not reg['servicio']:
            reg['servicio'] = f"Servicio_{i+1}"
        
        if 'usuario' not in reg or not reg['usuario']:
            reg['usuario'] = f"usuario{i+1}@ejemplo.com"
        
        if 'contraseña_cifrada' not in reg or not reg['contraseña_cifrada']:
            reg['contraseña_cifrada'] = cifrar_cesar("Temp123!")
            reg['metodo_cifrado'] = 1
        
        if reg.get('metodo_cifrado') not in [1, 2]:
            reg['metodo_cifrado'] = 1
    
    if guardar_json(ARCHIVO_CONTRASEÑAS, contraseñas):
        eliminados = original - len(contraseñas)
        print(f"\nReparado: {eliminados} eliminados, {len(contraseñas)} reparados")
        registrar_accion(f"Integridad reparada")
    else:
        print("\nError al guardar")