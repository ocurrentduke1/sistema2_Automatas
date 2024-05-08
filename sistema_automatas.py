import tkinter as tk
from tkinter import simpledialog

def crear_matriz(filas, columnas):
    # Inicializar la matriz con espacios en blanco
    matriz = [[' ' for _ in range(columnas + 1)] for _ in range(filas + 1)]
    return matriz

def ingresar_estados(matriz, estados_input):
    # Colocar los estados en la primer columna de la matriz
    estados = estados_input.split()
    for i, estado in enumerate(estados):
        matriz[i+1][0] = estado

def ingresar_alfabeto(matriz, elementos_input):
    # Colocar los elementos del alfabeto en la primer fila de la matriz
    elementos = elementos_input.split()
    for j, elemento in enumerate(elementos):
        matriz[0][j+1] = elemento

def ingresar_transiciones(matriz):
    for i in range(1, len(matriz)):
        for j in range(1, len(matriz[0])):
            estado = matriz[i][0]
            elemento = matriz[0][j]
            transicion = simpledialog.askstring("Transición", f"Ingrese la transición para el estado {estado} y el elemento {elemento}:")
            matriz[i][j] = transicion if transicion else ' '

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

    # Construir una cadena de texto para representar la tabla
    resultado = "Estados del AFD:\n"
    for estado in estados_afd:
        resultado += str(estado) + "\n"

    resultado += "\nTransiciones del AFD:\n"
    for transicion, destino in transiciones_afd.items():
        resultado += f"{transicion} -> {destino}\n"

    return resultado

def main():
    root = tk.Tk()
    root.title("Convertidor AFND a AFD")

    # Variables para almacenar la entrada del usuario
    filas_var = tk.StringVar()
    columnas_var = tk.StringVar()
    estados_var = tk.StringVar()
    alfabeto_var = tk.StringVar()

    # Función para ejecutar la conversión
    def convertir():
        # Obtener las entradas del usuario
        filas = int(filas_var.get())
        columnas = int(columnas_var.get())
        estados_input = estados_var.get()
        elementos_input = alfabeto_var.get()

        # Crear la matriz
        matriz = crear_matriz(filas, columnas)

        # Ingresar los estados en la matriz
        ingresar_estados(matriz, estados_input)

        # Ingresar los elementos del alfabeto en la matriz
        ingresar_alfabeto(matriz, elementos_input)

        # Ingresar las transiciones en la matriz
        ingresar_transiciones(matriz)

        # Verificar y modificar la matriz según las condiciones
        verificar_transiciones(matriz)

        # Convertir el AFND a AFD y obtener la tabla resultante
        tabla_resultante = convertir_afnd_a_afd(matriz)

        # Limpiar el widget tk.Text y agregar la tabla resultante
        resultado_text.delete(1.0, tk.END)
        resultado_text.insert(tk.END, tabla_resultante)

    # Crear widgets de entrada
    tk.Label(root, text="Número de estados:").pack()
    tk.Entry(root, textvariable=filas_var).pack()
    tk.Label(root, text="Tamaño del alfabeto:").pack()
    tk.Entry(root, textvariable=columnas_var).pack()
    tk.Label(root, text="Estados (separados por espacios):").pack()
    tk.Entry(root, textvariable=estados_var).pack()
    tk.Label(root, text="Elementos del alfabeto (separados por espacios):").pack()
    tk.Entry(root, textvariable=alfabeto_var).pack()

    # Botón para convertir
    tk.Button(root, text="Convertir", command=convertir).pack()

    # Widget tk.Text para mostrar el resultado
    resultado_text = tk.Text(root, height=10, width=40)
    resultado_text.pack()

    root.mainloop()

main()
