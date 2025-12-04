## 📌 **Descripción del Proyecto**
SAFEKEY VAULT+ es un **gestor de contraseñas seguro** desarrollado en Python como proyecto final de Programación I. Permite almacenar, cifrar, generar y gestionar contraseñas de forma segura con autenticación por contraseña maestra.

## 🚀 **Características Principales**
- ✅ **Autenticación segura** con contraseña maestra (3 intentos)
- ✅ **Cifrado de contraseñas** (2 métodos: César y Recursivo)
- ✅ **Generador de contraseñas** seguras personalizables
- ✅ **Análisis de fortaleza** de contraseñas
- ✅ **Búsqueda inteligente** con recursividad
- ✅ **Verificación de integridad** recursiva
- ✅ **Registro de actividades** (audit log)
- ✅ **Persistencia en archivos** JSON/TXT
- ✅ **Interfaz por consola** intuitiva

## 📁 **Estructura del Proyecto**
```
PROYECTO_FINAL/
├── src/
│   ├── busqueda/
│   │   ├── buscador.py          # Búsqueda con recursividad
│   │   └── verificador_integridad.py # Verificación recursiva
│   ├── core/
│   │   ├── autenticacion.py     # Contraseña maestra
│   │   └── gestor_contraseñas.py # CRUD completo
│   ├── seguridad/
│   │   ├── analizador_fuerza.py # Análisis de fortaleza
│   │   ├── cifrado.py           # 2 métodos de cifrado
│   │   └── generador_contraseñas.py # Generador seguro
│   └── utilidades/
│       ├── archivos.py          # Manejo de JSON/TXT
│       ├── helpers.py           # Funciones auxiliares
│       └── registro_actividades.py # Log de actividades
├── data/                        # Datos del sistema
│   ├── contraseñas.json         # Contraseñas cifradas
│   ├── maestra.txt              # Hash contraseña maestra
│   └── log_actividades.txt      # Registro de actividades
├── main.py                      # Programa principal
└── README.md                    # Este archivo
```

## 🔧 **Instalación y Ejecución**

### **Requisitos**
- Python 3.7 o superior
- No se requieren librerías externas

### **Pasos para ejecutar:**
1. **Clonar/descargar** el proyecto
2. **Navegar** a la carpeta del proyecto:
   ```bash
   cd ruta/al/proyecto
   ```
3. **Ejecutar** el programa principal:
   ```bash
   python main.py
   ```

## 🎮 **Instrucciones de Uso**

### **Primer uso:**
1. Al ejecutar por primera vez, se te pedirá **crear una contraseña maestra**
2. La contraseña debe tener al menos 6 caracteres
3. Se guarda cifrada con SHA-256

### **Menú Principal:**
```
1. Agregar cuenta           # Añadir nueva contraseña
2. Consultar cuenta         # Ver/consultar contraseñas
3. Editar cuenta            # Modificar contraseñas
4. Eliminar cuenta          # Eliminar contraseñas
5. Buscar contraseñas       # Búsqueda inteligente
6. Generar contraseña segura # Generador automático
7. Verificar integridad     # Revisión de datos
8. Cambiar contraseña maestra # Actualizar contraseña
0. Salir                    # Terminar programa
```

## 🔐 **Funcionalidades Detalladas**

### **1. Autenticación**
- Contraseña maestra con hash SHA-256
- Bloqueo tras 3 intentos fallidos
- Almacenamiento seguro en `data/maestra.txt`

### **2. Gestión de Contraseñas**
- **Agregar**: Servicio + usuario + contraseña (con confirmación)
- **Consultar**: Ver por servicio → seleccionar cuenta
- **Editar**: Modificar servicio, usuario o contraseña
- **Eliminar**: Con doble confirmación para seguridad

### **3. Cifrado (2 métodos)**
- **Método 1**: Cifrado César (desplazamiento de caracteres)
- **Método 2**: Cifrado Recursivo (inversión + César)
- Elección por cada contraseña

### **4. Generador de Contraseñas**
- Longitud personalizable (8-16 caracteres)
- Incluye: mayúsculas, minúsculas, números, símbolos
- Opción para guardar directamente en el gestor

### **5. Analizador de Fortaleza**
Evalúa 5 criterios:
- Longitud mínima (8+ caracteres)
- Presencia de mayúsculas
- Presencia de números
- Presencia de símbolos
- Detección de patrones débiles ("123", "password", etc.)

Clasificación: **Débil** | **Media** | **Fuerte** | **Muy fuerte**

### **6. Búsqueda Inteligente**
- Por servicio (exacta)
- Por usuario (parcial)
- Búsqueda general (parcial en ambos)
- **Implementación recursiva**

### **7. Verificación de Integridad**
**Función recursiva que verifica:**
- Registros vacíos o corruptos
- Campos incompletos o vacíos
- Contraseñas muy cortas
- Métodos de cifrado inválidos
- Opción de reparación automática

### **8. Registro de Actividades**
- Todas las acciones se registran con fecha/hora
- Archivo: `data/log_actividades.txt`
- Formato: `[YYYY-MM-DD HH:MM:SS] Acción realizada`

## 🧪 **Casos de Prueba**

### **Caso 1: Flujo Completo Normal**
```
1. Ejecutar: python main.py
2. Crear contraseña maestra: "Admin123"
3. Agregar contraseña:
   - Servicio: Gmail (del catálogo)
   - Usuario: prueba@gmail.com
   - Contraseña: MiPass123! (confirmar)
   - Método: César (1)
4. Consultar contraseña:
   - Servicio: Gmail
   - Seleccionar cuenta
   - Ver contraseña descifrada
5. Verificar que todo funciona
```

### **Caso 2: Prueba de Seguridad**
```
1. Intentar acceso con contraseña incorrecta 3 veces
   ✓ Sistema debe bloquearse
2. Reiniciar programa
3. Acceder con contraseña correcta
4. Intentar cambiar contraseña maestra por la misma
   ✓ Debe rechazar "no puede ser igual"
```

### **Caso 3: Generador de Contraseñas**
```
1. Menú → 6. Generar contraseña segura
2. Opción 1: Generar contraseña segura
3. Longitud: 12
4. Guardar contraseña generada
5. Seleccionar servicio: Facebook
6. Usuario: test@fb.com
7. Confirmar uso de contraseña generada
```

### **Caso 4: Búsqueda Recursiva**
```
1. Agregar 3 cuentas:
   - Gmail: usuario1@gmail.com
   - Gmail: usuario2@gmail.com  
   - Facebook: user@fb.com
2. Menú → 5. Buscar contraseñas
3. Buscar por servicio: "mail"
   ✓ Debe encontrar las 2 cuentas de Gmail
4. Búsqueda parcial: "user"
   ✓ Debe encontrar Facebook
```

### **Caso 5: Verificación de Integridad**
```
1. Editar manualmente data/contraseñas.json
2. Añadir registros corruptos:
   - {}
   - {"servicio": "Test", "usuario": ""}
   - {"servicio": "Test2", "contraseña_cifrada": "abc"}
3. Ejecutar verificación de integridad
4. Reparar automáticamente
5. Verificar que los problemas se solucionaron
```

### **Caso 6: Prueba de Cifrado/Descifrado**
```
1. Agregar contraseña con método César: "Hello123!"
2. Consultar y ver que descifra correctamente
3. Agregar contraseña con método Recursivo: "Test456@"
4. Consultar y ver que descifra correctamente
5. Comparar contraseña cifrada vs descifrada
```

### **Caso 7: Análisis de Fortaleza**
Probar estas contraseñas:
```
1. "123"              → Débil (muy corta)
2. "password"         → Débil (patrón prohibido)
3. "Password"         → Media (sin números/símbolos)
4. "Password123"      → Fuerte (le faltan símbolos)
5. "Pass123!"         → Fuerte (cumple todo)
6. "MiClaveLarga123!@#" → Muy fuerte (12+ caracteres)
```

### **Caso 8: Manejo de Múltiples Cuentas**
```
1. Agregar 3 cuentas para Gmail:
   - personal@gmail.com
   - trabajo@gmail.com
   - universidad@gmail.com
2. Consultar Gmail → debe mostrar 3 cuentas
3. Editar la segunda cuenta
4. Eliminar la tercera cuenta
5. Verificar que quedan 2 cuentas
```

### **Caso 9: Registro de Actividades**
```
1. Realizar varias acciones:
   - Agregar contraseña
   - Consultar contraseña
   - Generar contraseña
   - Verificar integridad
2. Ver archivo data/log_actividades.txt
3. Verificar que todas las acciones están registradas
```

### **Caso 10: Recuperación ante Fallos**
```
1. Cerrar programa abruptamente (Ctrl+C)
2. Volver a abrir
3. Verificar que:
   - Las contraseñas siguen guardadas
   - Puedes autenticarte
   - Los datos están intactos
```

## 📊 **Requisitos Cumplidos**

| Requisito | Implementado | Archivo |
|-----------|-------------|---------|
| A. Acceso con contraseña maestra | ✅ | `autenticacion.py` |
| B. Gestión de contraseñas (CRUD) | ✅ | `gestor_contraseñas.py` |
| C. Cifrado (2 métodos) | ✅ | `cifrado.py` |
| D. Analizador de fuerza | ✅ | `analizador_fuerza.py` |
| E. Generador de contraseñas | ✅ | `generador_contraseñas.py` |
| F. Buscador con recursividad | ✅ | `buscador.py` |
| G. Registro de actividades | ✅ | `registro_actividades.py` |
| H. Verificación recursiva de integridad | ✅ | `verificador_integridad.py` |
| Persistencia en archivos | ✅ | `archivos.py` |
| Diseño modular | ✅ | Estructura de carpetas |

## 🐛 **Solución de Problemas Comunes**

### **Problema: "ModuleNotFoundError"**
**Solución:** Ejecutar desde la carpeta principal, no desde `src/`

### **Problema: Contraseña maestra incorrecta**
**Solución:** Borrar `data/maestra.txt` para reiniciar

### **Problema: Archivos JSON corruptos**
**Solución:** Usar "Verificar integridad" → Reparar automáticamente

### **Problema: Usuarios vacíos en consultas**
**Solución:** Ejecutar verificación de integridad y reparar

## 📝 **Notas Técnicas**

### **Recursividad Implementada en:**
1. **Cifrado recursivo** (`cifrado.py`) - `invertir_recursivo()`
2. **Búsqueda recursiva** (`buscador.py`) - `buscar_recursiva_*()`
3. **Verificación recursiva** (`verificador_integridad.py`) - `verificar_recursivo()`

### **Estructuras de Datos Usadas:**
- **Listas/Diccionarios**: Para almacenar contraseñas
- **Archivos JSON**: Para persistencia
- **Strings**: Para cifrado/manipulación de texto
- **Conjuntos de caracteres**: Para generación de contraseñas

### **Algoritmos Implementados:**
- Cifrado César (desplazamiento de caracteres)
- SHA-256 para hash de contraseña maestra
- Recursividad para recorrido y búsqueda
- Validación de patrones para análisis de fortaleza
