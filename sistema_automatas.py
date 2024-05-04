import tkinter as tk

class TablaInterfaz:
    def __init__(self, master):
        self.master = master
        self.master.title("Modificar Tamaño de la Tabla")

        self.frame_instrucciones = tk.Frame(self.master)
        self.frame_instrucciones.pack(padx=20, pady=5)

        self.label_instrucciones = tk.Label(self.frame_instrucciones,
                                            text="Instrucciones:\n"
                                                 "- Escribir el estado inicial con '->'\n"
                                                 "- Si una entrada de transición va a más de 1 estado, escribir los estados separados por espacios\n"
                                                 "- Los estados aceptados deben ser escritos con '*'\n"
                                                 "- Si una entrada no tiene estado de transición, escribir con '-'")
        self.label_instrucciones.pack()

        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=20, pady=20)

        self.label_filas = tk.Label(self.frame, text="Filas:")
        self.label_filas.grid(row=0, column=0, padx=5, pady=5)

        self.entry_filas = tk.Entry(self.frame)
        self.entry_filas.grid(row=0, column=1, padx=5, pady=5)

        self.label_columnas = tk.Label(self.frame, text="Columnas:")
        self.label_columnas.grid(row=1, column=0, padx=5, pady=5)

        self.entry_columnas = tk.Entry(self.frame)
        self.entry_columnas.grid(row=1, column=1, padx=5, pady=5)

        self.boton_modificar = tk.Button(self.frame, text="Modificar Tabla", command=self.modificar_tabla)
        self.boton_modificar.grid(row=2, columnspan=2, padx=5, pady=5)

        self.tabla_frame = tk.Frame(self.master)
        self.tabla_frame.pack(padx=20, pady=20)

        self.tabla = None

    def modificar_tabla(self):
        filas = int(self.entry_filas.get())
        columnas = int(self.entry_columnas.get())

        if self.tabla:
            self.tabla.destroy()

        self.tabla = tk.Frame(self.tabla_frame)
        self.tabla.pack()

        self.celdas = []

        for i in range(filas):
            fila = []
            for j in range(columnas):
                entry = tk.Entry(self.tabla, width=10)
                entry.grid(row=i, column=j)
                fila.append(entry)
            self.celdas.append(fila)


def main():
    root = tk.Tk()
    app = TablaInterfaz(root)
    root.mainloop()


if __name__ == "__main__":
    main()
