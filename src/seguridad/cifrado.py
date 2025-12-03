def cifrar_cesar(texto, desplazamiento=3):
    """Cifrado César: desplaza cada letra N posiciones"""
    resultado = ""
    
    for caracter in texto:
        if 'A' <= caracter <= 'Z':
            codigo = ord(caracter) - ord('A')
            codigo = (codigo + desplazamiento) % 26
            resultado += chr(codigo + ord('A'))
        
        elif 'a' <= caracter <= 'z':
            codigo = ord(caracter) - ord('a')
            codigo = (codigo + desplazamiento) % 26
            resultado += chr(codigo + ord('a'))
        
        elif '0' <= caracter <= '9':
            codigo = ord(caracter) - ord('0')
            codigo = (codigo + desplazamiento) % 10
            resultado += chr(codigo + ord('0'))
        
        else:
            resultado += caracter
    
    return resultado

def descifrar_cesar(texto_cifrado, desplazamiento=3):
    """Descifra texto cifrado con César"""
    resultado = ""
    
    for caracter in texto_cifrado:
        if 'A' <= caracter <= 'Z':
            codigo = ord(caracter) - ord('A')
            codigo = (codigo - desplazamiento) % 26
            resultado += chr(codigo + ord('A'))
        
        elif 'a' <= caracter <= 'z':
            codigo = ord(caracter) - ord('a')
            codigo = (codigo - desplazamiento) % 26
            resultado += chr(codigo + ord('a'))
        
        elif '0' <= caracter <= '9':
            codigo = ord(caracter) - ord('0')
            codigo = (codigo - desplazamiento) % 10
            resultado += chr(codigo + ord('0'))
        
        else:
            resultado += caracter
    
    return resultado

def invertir_recursivo(texto):
    """Invierte un texto usando recursividad"""
    if len(texto) <= 1:
        return texto
    
    return texto[-1] + invertir_recursivo(texto[:-1])

def cifrar_recursivo(contraseña):
    """Cifrado recursivo: invierte + César"""
    invertida = invertir_recursivo(contraseña)
    return cifrar_cesar(invertida)

def descifrar_recursivo(contraseña_cifrada):
    """Descifrado recursivo: César + invertir"""
    descifrada_cesar = descifrar_cesar(contraseña_cifrada)
    return invertir_recursivo(descifrada_cesar)