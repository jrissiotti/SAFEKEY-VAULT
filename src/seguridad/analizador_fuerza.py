def analizar_fuerza(contraseña):
    """Analiza fortaleza de contraseña y devuelve (categoria, puntaje)"""
    puntaje = 0
    
    # 1. Longitud (8+ caracteres)
    if len(contraseña) >= 8:
        puntaje += 1
    
    # 2. Mayúsculas
    if any(c.isupper() for c in contraseña):
        puntaje += 1
    
    # 3. Minúsculas  
    if any(c.islower() for c in contraseña):
        puntaje += 1
    
    # 4. Números
    if any(c.isdigit() for c in contraseña):
        puntaje += 1
    
    # 5. Símbolos
    simbolos = "!@#$%^&*()-_=+[]{}|;:,.<>?/~`"
    if any(c in simbolos for c in contraseña):
        puntaje += 1
    
    # Penalizar patrones débiles
    patrones_debiles = [
        "123", "abc", "password", "contraseña", "admin",
        "qwerty", "0000", "1111", "123456", "12345678"
    ]
    
    contra_min = contraseña.lower()
    for patron in patrones_debiles:
        if patron in contra_min and puntaje > 0:
            puntaje -= 1
    
    # Determinar categoría
    if len(contraseña) >= 12 and puntaje >= 4:
        categoria = "Muy fuerte"
    elif puntaje >= 4:
        categoria = "Fuerte"
    elif puntaje >= 3:
        categoria = "Media"
    else:
        categoria = "Débil"
    
    return categoria, puntaje, []


def verificar_longitud(contraseña):
    return len(contraseña) >= 8


def verificar_mayusculas(contraseña):
    return any(c.isupper() for c in contraseña)


def verificar_minusculas(contraseña):
    return any(c.islower() for c in contraseña)


def verificar_numeros(contraseña):
    return any(c.isdigit() for c in contraseña)


def verificar_simbolos(contraseña):
    simbolos = "!@#$%^&*()-_=+[]{}|;:,.<>?/~`"
    return any(c in simbolos for c in contraseña)