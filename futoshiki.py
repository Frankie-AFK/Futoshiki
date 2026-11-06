import json#Permite trabajar con archivos JSON
import tkinter as tk#Importa la librería para crear ventanas
with open("futoshiki2026partidas.json", "r", encoding="utf-8") as archivo:#Abre el archivo JSON
    partidas = json.load(archivo)#Convierte los datos JSON en estructuras de Python
print(partidas["Fácil"][0]["número_partida"])#Muestra el número de la primera partida fácil
ventana = tk.Tk()#Crea la ventana principal
ventana.title("Futoshiki")#Nombre de la ventana
ventana.geometry("600x500")#Tamaño de la ventana
def abrir_juego():
    juego = tk.Toplevel(ventana)#Abre otra ventana
    juego.title("Partida de Futoshiki")
    juego.geometry("500x500")
    casillas = []#Guarda las casillas del tablero
    for fila in range(5):#Recorre las 5 filas
        fila_casillas = []#Guarda las casillas de una fila
        for columna in range(5):#Recorre las 5 columnas
            casilla = tk.Entry(juego, width=4, font=("Arial", 20), justify="center")
            casilla.grid(row=fila*2, column=columna*2, padx=5, pady=5)
            fila_casillas.append(casilla)#Guarda la casilla en su fila
        casillas.append(fila_casillas)#Guarda la fila completa
    partida = partidas["Fácil"][0]#Obtiene la primera partida del nivel Fácil
    for dato in partida["dígitos_predeterminados"]:  # Recorre los números fijos
        fila = dato["fila"]  # Obtiene la fila
        columna = dato["columna"]  # Obtiene la columna
        numero = dato["dígito"]  # Obtiene el número
        casillas[fila][columna].insert(0, str(numero))  # Coloca el número en la casilla
        casillas[fila][columna].config(state="disabled")  # Impide modificarlo
    for dato in partida["desigualdades_horizontales"]:#Recorre las desigualdades
        fila = dato["fila"]#Obtiene la fila
        columna = dato["columna"]#Obtiene la columna
        signo = dato["restricción"]#Obtiene el símbolo < o >
        simbolo = tk.Label(juego, text=signo, font=("Arial", 16))# Crea el símbolo
        simbolo.grid(row=fila*2, column=columna*2+1)# Lo coloca entre casillas
    for dato in partida["desigualdades_verticales"]:#Recorre las desigualdades verticales
        fila = dato["fila"]#Obtiene la fila
        columna = dato["columna"]#Obtiene la columna
        signo = dato["restricción"]#Obtiene el símbolo vertical
        simbolo = tk.Label(juego, text=signo, font=("Arial", 16))#Crea el símbolo
        simbolo.grid(row=fila*2+1, column=columna*2)#Lo coloca entre dos filas
titulo = tk.Label(ventana, text="FUTOSHIKI", font=("Arial", 24))
titulo.pack(pady=30)
boton_jugar = tk.Button(ventana, text="Jugar", width=20, command=abrir_juego)
boton_jugar.pack(pady=10)
boton_config = tk.Button(ventana, text="Configuración", width=20)
boton_config.pack(pady=10)
boton_salir = tk.Button(ventana, text="Salir", width=20, command=ventana.destroy)
boton_salir.pack(pady=10)
ventana.mainloop()# Mantiene la ventana abierta




