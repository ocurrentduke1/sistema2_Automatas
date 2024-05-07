def crear_matriz(filas, columnas):
    # Inicializar la matriz con espacios en blanco
    matriz = [[' ' for _ in range(columnas + 1)] for _ in range(filas + 1)]
    return matriz

def ingresar_estados(matriz):
    # Pedir al usuario que ingrese los estados
    print("\nIngresa los estados, separados por espacios:")
    estados = input().split()

    # Colocar los estados en la primer columna de la matriz
    for i, estado in enumerate(estados):
        matriz[i+1][0] = estado

def ingresar_alfabeto(matriz, columnas):
    # Pedir al usuario que ingrese los elementos del alfabeto
    print("\nIngresa los elementos del alfabeto, separados por espacios:")
    elementos = input().split()

    # Colocar los elementos del alfabeto en la primer fila de la matriz
    for j, elemento in enumerate(elementos):
        matriz[0][j+1] = elemento

def ingresar_transiciones(matriz):
    filas = len(matriz) - 1
    columnas = len(matriz[0]) - 1

    for i in range(filas):
        for j in range(columnas):
            estado = matriz[i+1][0]
            elemento = matriz[0][j+1]
            transicion = input(f"Ingrese la transición para el estado {estado} y el elemento {elemento}: ")
            matriz[i+1][j+1] = transicion

def verificar_transiciones(matriz):
    nuevas_filas = []
    for i in range(1, len(matriz)):
        for j in range(1, len(matriz[0])):
            if ' ' in matriz[i][j] and len(matriz[i][j].split()) >= 2:
                # Si encuentra más de un elemento en la casilla, crea una fila extra
                elementos_adicionales = matriz[i][j].split()
                nueva_fila = [' ' for _ in range(len(matriz[0]))]
                nueva_fila[0] = ' '.join(elementos_adicionales)  # Copiar todos los elementos en la nueva fila
                nuevas_filas.append((i+1, nueva_fila))
    # Insertar las nuevas filas en la matriz
    for index, (pos, fila) in enumerate(nuevas_filas):
        matriz.insert(pos + index, fila)


def imprimir_matriz(matriz):
    for fila in matriz:
        for elemento in fila:
            print(elemento, end='\t')
        print()


def convertir_afnd_a_afd(matriz):
    estados_afnd = [fila[0] for fila in matriz[1:]]
    alfabeto = matriz[0][1:]

    transiciones_afnd = {}
    for i in range(1, len(matriz)):
        estado = matriz[i][0]
        for j in range(1, len(matriz[0])):
            simbolo = matriz[0][j]
            transicion = matriz[i][j].split()
            if transicion:
                transiciones_afnd[(estado, simbolo)] = transicion

    estado_inicial = (matriz[1][0],)
    estados_finales = {fila[0] for fila in matriz[1:] if ' ' in fila[0]}

    # Crear un diccionario para las transiciones del AFD
    transiciones_afd = {}
    # Crear una lista para los estados del AFD
    estados_afd = []
    # Crear una cola para los estados pendientes de procesar
    cola_estados = [estado_inicial]
    # Mientras haya estados pendientes
    while cola_estados:
        estado_actual = cola_estados.pop(0)
        # Para cada símbolo del alfabeto
        for simbolo in alfabeto:
            # Obtener el conjunto de estados alcanzables desde el estado actual con el símbolo actual
            alcanzables = set()
            for estado in estado_actual:
                alcanzables.update(transiciones_afnd.get((estado, simbolo), []))
            # Convertir el conjunto a un estado del AFD (tupla ordenada)
            estado_afd = sorted(list(alcanzables))
            # Si el estado AFD no está en la lista de estados del AFD, agregarlo y encolarlo
            if estado_afd not in estados_afd:
                estados_afd.append(estado_afd)
                cola_estados.append(estado_afd)
            # Agregar la transición al diccionario de transiciones del AFD
            transiciones_afd[(tuple(estado_actual), simbolo)] = tuple(estado_afd)
    # Determinar los estados finales del AFD
    estados_finales_afd = [estado for estado in estados_afd if any(fin in estado for fin in estados_finales)]

    # Imprimir todos los estados del AFD
    print("\nEstados del AFD:")
    for estado in estados_afd:
        print(estado)

    return estados_afd, transiciones_afd, estados_finales_afd


# Ejemplo de uso:
def main():
    # Pedir al usuario las dimensiones de la matriz
    filas = int(input("Ingresa el número de estados: "))
    columnas = int(input("Ingresa el tamaño del alfabeto: "))

    # Crear la matriz
    matriz = crear_matriz(filas, columnas)

    # Ingresar los estados en la matriz
    ingresar_estados(matriz)

    # Ingresar los elementos del alfabeto en la matriz
    ingresar_alfabeto(matriz, columnas)

    # Ingresar las transiciones en la matriz
    ingresar_transiciones(matriz)

    # Verificar y modificar la matriz según las condiciones
    verificar_transiciones(matriz)

    # Convertir el AFND a AFD
    afd = convertir_afnd_a_afd(matriz)

    # Imprimir el resultado del AFD
    print("Transiciones del AFD:", afd[1])

main()