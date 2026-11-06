import json#Permite trabajar con archivos JSON
import tkinter as tk#Importa la librería para crear ventanas
with open("futoshiki2026partidas.json", "r", encoding="utf-8") as archivo:#Abre el archivo JSON
    partidas = json.load(archivo)#Convierte los datos JSON en estructuras de Python
ventana = tk.Tk()#Crea la ventana principal
ventana.title("FUTOSHIKI")#Nombre de la ventana
ventana.geometry("600x500")#Tamaño de la ventana
def abrir_juego():
    juego = tk.Toplevel(ventana)#Abre otra ventana
    juego.title("Partida de Futoshiki")
    juego.geometry("700x600")#Aumenta el espacio para el panel de dígitos
    casillas = []#Guarda las casillas del tablero
    for fila in range(5):#Recorre las 5 filas
        fila_casillas = []#Guarda las casillas de una fila
        for columna in range(5):#Recorre las 5 columnas
            casilla = tk.Entry(juego, width=4, font=("Arial", 20), justify="center")
            casilla.grid(row=fila*2, column=columna*2, padx=5, pady=5)
            fila_casillas.append(casilla)#Guarda la casilla en su fila
        casillas.append(fila_casillas)#Guarda la fila completa
    partida = partidas["Fácil"][0]#Obtiene la primera partida del nivel Fácil
    for dato in partida["dígitos_predeterminados"]:#Recorre los números fijos
        fila = dato["fila"] 
        columna = dato["columna"]#Obtiene la columna
        numero = dato["dígito"]#Obtiene el número
        casillas[fila][columna].insert(0, str(numero))#Coloca el número en la casilla
        casillas[fila][columna].config(state="disabled")#Impide modificarlo
    for dato in partida["desigualdades_horizontales"]:#Recorre las desigualdades
        fila = dato["fila"]#Obtiene la fila
        columna = dato["columna"]#Obtiene la columna
        signo = dato["restricción"]#Obtiene el símbolo < o >
        simbolo = tk.Label(juego, text=signo, font=("Arial", 16))#Crea el símbolo
        simbolo.grid(row=fila*2, column=columna*2+1)#Lo coloca entre casillas
    for dato in partida["desigualdades_verticales"]:#Recorre las desigualdades verticales
        fila = dato["fila"]#Obtiene la fila
        columna = dato["columna"]#Obtiene la columna
        signo = dato["restricción"]#Obtiene el símbolo vertical
        simbolo = tk.Label(juego, text=signo, font=("Arial", 16))#Crea el símbolo
        simbolo.grid(row=fila*2+1, column=columna*2)#Lo coloca entre dos filas
    botones = []#Guarda los botones de los números
    seleccionado = [0]#Guarda el número seleccionado
    def seleccionar_numero(numero):
        seleccionado[0] = numero#Actualiza el número seleccionado
        for boton in botones:
            boton.config(bg="SystemButtonFace")#Quita el color anterior
        botones[numero-1].config(bg="lightgreen")#Pinta el seleccionado
    for numero in range(1, 6):#Recorre los números del 1 al 5
        boton = tk.Button(juego, text=str(numero), width=5, height=2, command=lambda n=numero: seleccionar_numero(n))#Selecciona el número
        boton.grid(row=(numero-1)*2, column=9, padx=20)#Coloca el botón a la derecha
        botones.append(boton)#Guarda el botón en la lista
barra_menu = tk.Menu(ventana)#Crea la barra de menú
ventana.config(menu=barra_menu)#Coloca la barra en la ventana
barra_menu.add_command(label="Jugar", command=abrir_juego)#Abre el juego
barra_menu.add_command(label="Configurar")#Configuración
barra_menu.add_command(label="Ayuda")#Manual de usuario
barra_menu.add_command(label="Acerca de")#Información del programa
ventana.mainloop()#Mantiene la ventana abierta




