import random

def generar_matriz_bingo():
    """
    Genera un diccionario con los números de un cartón de bingo 75.
    Reglas: B(1-15), I(16-30), N(31-45), G(46-60), O(61-75).
    Sin duplicados y ordenados de menor a mayor.
    """
    carton = {
        'B': sorted(random.sample(range(1, 16), 5)),
        'I': sorted(random.sample(range(16, 31), 5)),
        'N': sorted(random.sample(range(31, 46), 5)),
        'G': sorted(random.sample(range(46, 61), 5)),
        'O': sorted(random.sample(range(61, 76), 5))
    }

    carton['N'][2] = "FREE"

    return carton