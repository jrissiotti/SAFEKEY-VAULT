import sys
import os

# Esta línea hace que Python encuentre los módulos en src/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def mostrar_menu():
    """Muestra el menú principal"""
    print("\n" + "=" * 30)
    print("         MENU PRINCIPAL")
    print("=" * 30)
    print("1. Agregar cuenta")
    print("2. Consultar cuenta")
    print("3. Editar cuenta")
    print("4. Eliminar cuenta")
    print("5. Buscar contraseñas")
    print("6. Generar contraseña segura")
    print("7. Verificar integridad")
    print("8. Cambiar contraseña maestra")
    print("0. Salir")

def main():
    """Función principal del programa"""
    print("=" * 30)
    print("     SAFEKEY VAULT+")
    print("=" * 30)
    
    from core.autenticacion import autenticar_usuario
    if not autenticar_usuario():
        print("\nAcceso denegado.")
        return
    
    # 2. Menú principal
    while True:
        mostrar_menu()
        
        try:
            opcion = int(input("\nOpción: "))
        except ValueError:
            print("Ingresa un número válido")
            continue
        
        if opcion == 0:
            print("\nSaliendo del sistema...")
            break
        
        # Manejar cada opción (importamos solo cuando se necesita)
        if opcion == 1:
            from core.gestor_contraseñas import agregar_contraseña
            agregar_contraseña()
        
        elif opcion == 2:
            from core.gestor_contraseñas import consultar_contraseña
            consultar_contraseña()
        
        elif opcion == 3:
            from core.gestor_contraseñas import editar_contraseña
            editar_contraseña()
        
        elif opcion == 4:
            from core.gestor_contraseñas import eliminar_contraseña
            eliminar_contraseña()
        
        elif opcion == 5:
            from busqueda.buscador import buscar_contraseñas
            buscar_contraseñas()
        
        elif opcion == 6:
            from seguridad.generador_contraseñas import generar_contraseña
            generar_contraseña()
        
        elif opcion == 7:
            from busqueda.verificador_integridad import verificar_integridad
            verificar_integridad()
        
        elif opcion == 8:
            from core.autenticacion import cambiar_contraseña_maestra
            cambiar_contraseña_maestra()
        
        else:
            print("Opción no válida")

if __name__ == "__main__":
    main()