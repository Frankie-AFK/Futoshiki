import tkinter as tk#Importa la librería para crear ventanas
ventana = tk.Tk()#Crea la ventana principal
ventana.title("Futoshiki")#Nombre de la ventana
ventana.geometry("600x500")#Tamaño de la ventana
def abrir_juego():
    juego = tk.Toplevel(ventana)#Abre otra ventana
    juego.title("Partida de Futoshiki")
    juego.geometry("500x500")
    for fila in range(5):#Recorre las 5 filas
        for columna in range(5):#Recorre las 5 columnas
            casilla = tk.Entry(juego, width=4, font=("Arial", 20), justify="center")
            casilla.grid(row=fila*2, column=columna*2, padx=5, pady=5)
            if columna < 4:
                simbolo = tk.Label(juego, text="<", font=("Arial", 16))
                simbolo.grid(row=fila*2, column=columna*2+1)
            if fila < 4:#Evita colocar símbolos debajo de la última fila
                vertical = tk.Label(juego, text="∨", font=("Arial", 16))
                vertical.grid(row=fila*2+1, column=columna*2)
titulo = tk.Label(ventana, text="FUTOSHIKI", font=("Arial", 24))
titulo.pack(pady=30)
boton_jugar = tk.Button(ventana, text="Jugar", width=20, command=abrir_juego)
boton_jugar.pack(pady=10)
boton_config = tk.Button(ventana, text="Configuración", width=20)
boton_config.pack(pady=10)
boton_salir = tk.Button(ventana, text="Salir", width=20, command=ventana.destroy)
boton_salir.pack(pady=10)
ventana.mainloop()# Mantiene la ventana abierta




