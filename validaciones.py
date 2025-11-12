def validar_dinero(nuevo_texto: str) -> bool:
    if nuevo_texto == "":
        return True

    try:
        float(nuevo_texto) 
        
        if "." in nuevo_texto:
            parte_decimal = nuevo_texto.split(".", 1)[1]
            if len(parte_decimal) > 2:
                return False

        return True

    except ValueError:
        return False