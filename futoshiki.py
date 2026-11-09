import json#Permite trabajar con archivos JSON
import tkinter as tk#Importa la librería para crear ventanas
import time#Permite trabajar con el tiempo
with open("futoshiki2026partidas.json", "r", encoding="utf-8") as archivo:#Abre el archivo JSON
    partidas = json.load(archivo)#Convierte los datos JSON en estructuras de Python
ventana = tk.Tk()#Crea la ventana principal
ventana.title("FUTOSHIKI")#Nombre de la ventana
ventana.geometry("600x500")#Tamaño de la ventana



def abrir_juego():
    juego = tk.Toplevel(ventana)#Abre otra ventana
    juego.title("Partida de Futoshiki")
    juego.geometry("700x600")#Aumenta el espacio para el panel de dígitos
    iniciado = [False]#Indica si la partida ha comenzado
    terminado = [False]#Indica si la partida ya terminó
    segundos = [0]#Guarda los segundos transcurridos
    titulo = tk.Label(juego, text="FUTOSHIKI", font=("Arial", 24, "bold"))#Título del juego
    titulo.grid(row=0, column=0, columnspan=10, pady=10)#Coloca el título arriba
    nivel = tk.Label(juego, text="NIVEL FÁCIL", font=("Arial", 14))#Muestra el nivel
    nivel.grid(row=1, column=0, columnspan=10)#Coloca el nivel debajo del título
    texto_nombre = tk.Label(juego, text="Nombre del jugador:")#Texto para pedir el nombre
    texto_nombre.grid(row=2, column=0, columnspan=3)#Coloca el texto
    entrada_nombre = tk.Entry(juego, width=25)#Espacio para escribir el nombre
    entrada_nombre.grid(row=2, column=3, columnspan=5)#Coloca la entrada
    reloj = tk.Label(juego, text="00:00:00", font=("Arial", 16))#Muestra el tiempo de la partida
    reloj.grid(row=15, column=0, columnspan=3, pady=10)#Coloca el reloj debajo de los botones


    
    def validar_fila(fila, numero):#Comprueba si el número está repetido en una fila
        repetidos = 0#Inicia el contador
        for columna_actual in range(5):#Recorre las 5 columnas
            if casillas[fila][columna_actual].get() == str(numero):#Busca el número
                repetidos += 1#Aumenta el contador
        if repetidos > 1:#Comprueba si está repetido
            return False#El número está repetido
        return True#El número no está repetido


    
    def validar_columna(columna, numero):#Comprueba si el número está repetido en una columna
        repetidos = 0#Inicia el contador
        for fila_actual in range(5):#Recorre las 5 filas
            if casillas[fila_actual][columna].get() == str(numero):#Busca el número
                repetidos += 1#Aumenta el contador
        if repetidos > 1:#Comprueba si está repetido
            return False#El número está repetido
        return True#El número no está repetido


    
    def validar_horizontal():#Comprueba las desigualdades horizontales
        for dato in partida["desigualdades_horizontales"]:#Recorre las desigualdades
            fila_dato = dato["fila"]#Obtiene la fila
            columna_dato = dato["columna"]#Obtiene la columna
            signo = dato["restricción"]#Obtiene el signo
            izquierda = casillas[fila_dato][columna_dato].get()#Obtiene el número izquierdo
            derecha = casillas[fila_dato][columna_dato+1].get()#Obtiene el número derecho
            if izquierda != "" and derecha != "":#Comprueba que ambas casillas tengan números
                if signo == "<" and int(izquierda) >= int(derecha):#Comprueba si se incumple <
                    return False#La desigualdad es incorrecta
                if signo == ">" and int(izquierda) <= int(derecha):#Comprueba si se incumple >
                    return False#La desigualdad es incorrecta
        return True#Las desigualdades comprobadas son correctas



    def validar_vertical():#Comprueba las desigualdades verticales
        for dato in partida["desigualdades_verticales"]:#Recorre las desigualdades
            fila_dato = dato["fila"]#Obtiene la fila
            columna_dato = dato["columna"]#Obtiene la columna
            signo = dato["restricción"]#Obtiene el símbolo
            arriba = casillas[fila_dato][columna_dato].get()#Obtiene el número superior
            abajo = casillas[fila_dato+1][columna_dato].get()#Obtiene el número inferior
            if arriba != "" and abajo != "":#Comprueba que ambas casillas tengan números
                if signo == "v" and int(arriba) <= int(abajo):#Comprueba si se incumple v
                    return False#La desigualdad es incorrecta
                if signo == "^" and int(arriba) >= int(abajo):#Comprueba si se incumple ^
                    return False#La desigualdad es incorrecta
        return True#Las desigualdades comprobadas son correctas


    
    def colocar_numero(fila, columna):#Recibe la posición de la casilla
        if iniciado[0] == False: #Comprueba si el juego no ha iniciado
            print("Primero debe iniciar el juego")#Muestra un aviso
            return#Impide colocar números
        numero = seleccionado[0]#Obtiene el número seleccionado
        if numero != 0:#Comprueba que se seleccionó un número
            casilla = casillas[fila][columna]#Busca la casilla seleccionada
            if casilla["state"] == "normal":#Comprueba que no sea un número fijo
                anterior = casilla.get()#Guarda el número que tenía la casilla antes del cambio
                casilla.delete(0, tk.END)#Borra el contenido anterior
                casilla.insert(0, str(numero))#Coloca el número seleccionado
                if validar_fila(fila, numero) == False:#Llama a la función que revisa la fila
                    print("Número repetido en la fila")#Muestra el error
                    casilla.delete(0, tk.END)#Borra el número repetido
                    return#Termina la función
                if validar_columna(columna, numero) == False:#Llama a la función que revisa la columna
                    print("Número repetido en la columna")#Muestra el error
                    casilla.delete(0, tk.END)#Borra el número repetido
                    return#Termina la función
                if validar_horizontal() == False:#Llama a la función que revisa las desigualdades
                    print("Desigualdad horizontal incorrecta")#Muestra el error
                    casilla.delete(0, tk.END)#Borra el número incorrecto
                    return#Termina la función
                if validar_vertical() == False:#Llama a la función que revisa las desigualdades verticales
                    print("Desigualdad vertical incorrecta")#Muestra el error
                    casilla.delete(0, tk.END)#Borra el número incorrecto
                    return#Termina la función
                historial.append((fila, columna, anterior))#Guarda la jugada válida para poder deshacerla


    historial = []#Guarda las jugadas realizadas para poder deshacerlas                    
    casillas = []#Guarda las casillas del tablero
    for fila in range(5):#Recorre las 5 filas
        fila_casillas = []#Guarda las casillas de una fila
        for columna in range(5):#Recorre las 5 columnas
            casilla = tk.Entry(juego, width=4, font=("Arial", 20), justify="center")
            casilla.grid(row=fila*2+4, column=columna*2, padx=5, pady=5)#Coloca las casillas debajo del nombre
            casilla.bind("<Button-1>", lambda evento, f=fila, c=columna: colocar_numero(f, c))#Detecta el clic izquierdo
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
        simbolo.grid(row=fila*2+4, column=columna*2+1) #Coloca el símbolo entre casillas
    for dato in partida["desigualdades_verticales"]:#Recorre las desigualdades verticales
        fila = dato["fila"]#Obtiene la fila
        columna = dato["columna"]#Obtiene la columna
        signo = dato["restricción"]#Obtiene el símbolo vertical
        simbolo = tk.Label(juego, text=signo, font=("Arial", 16))#Crea el símbolo
        simbolo.grid(row=fila*2+5, column=columna*2) #Coloca el símbolo entre filas
    botones = []#Guarda los botones de los números
    seleccionado = [0]#Guarda el número seleccionado
    historial = []#Guarda las jugadas realizadas para poder deshacerlas



    def actualizar_reloj():#Actualiza el tiempo de la partida
        if iniciado[0] == True:#Comprueba si el juego está activo
            segundos[0] += 1#Aumenta un segundo
            horas = segundos[0] // 3600#Calcula las horas
            minutos = (segundos[0] % 3600) // 60#Calcula los minutos
            seg = segundos[0] % 60#Calcula los segundos
            reloj.config(text=f"{horas:02}:{minutos:02}:{seg:02}")#Muestra el tiempo
        if terminado[0] == False:#Comprueba si el juego no ha terminado
            juego.after(1000, actualizar_reloj)#Vuelve a ejecutar después de un segundo



    def iniciar_juego():#Función para iniciar la partida
        if terminado[0] == True:#Comprueba si la partida ya terminó
            print("La partida ya terminó")#Muestra un aviso
            return#Impide reiniciar la partida
        nombre = entrada_nombre.get().strip()#Obtiene el nombre del jugador
        if nombre == "":#Comprueba si está vacío
            print("Debe escribir el nombre del jugador")#Muestra un aviso
            return#No inicia el juego
        iniciado[0] = True#Permite jugar
        segundos[0] = 0#Reinicia el contador a cero
        actualizar_reloj()#Comienza a contar el tiempo
        print("Juego iniciado")#Confirma el inicio
    boton_iniciar = tk.Button(juego, text="INICIAR JUEGO", command=iniciar_juego)#Crea el botón
    boton_iniciar.grid(row=14, column=0, columnspan=3, pady=20)#Coloca el botón debajo del tablero

    

    def borrar_jugada():#Deshace la última jugada realizada
        if iniciado[0] == False:#Comprueba si el juego está detenido
            print("No puede borrar jugadas si el juego no está iniciado")#Muestra un aviso
            return#Impide borrar jugadas
        if len(historial) > 0:#Comprueba que existan jugadas
            fila, columna, anterior = historial.pop()#Obtiene y elimina la última jugada
            casilla = casillas[fila][columna]#Busca la casilla modificada
            casilla.delete(0, tk.END)#Borra el número actual
            casilla.insert(0, anterior)#Restaura el contenido anterior
        else:
            print("No hay jugadas para borrar")#Muestra un aviso
    boton_borrar = tk.Button(juego, text="BORRAR JUGADA", command=borrar_jugada)#Crea el botón
    boton_borrar.grid(row=14, column=3, columnspan=3, pady=20)#Coloca el botón debajo del tablero



    def terminar_juego():#Termina la partida actual
        if iniciado[0] == False:#Comprueba si el juego no ha comenzado
            print("Primero debe iniciar el juego")#Muestra un aviso
            return#Termina la función
        iniciado[0] = False#Impide seguir colocando números
        terminado[0] = True#Marca la partida como terminada
        print("Juego terminado")#Confirma que terminó la partida
    boton_terminar = tk.Button(juego, text="TERMINAR JUEGO", command=terminar_juego)#Crea el botón
    boton_terminar.grid(row=14, column=6, columnspan=3, pady=20)#Coloca el botón debajo del tablero



    def borrar_juego():#Borra los números colocados por el jugador
        if iniciado[0] == False:#Comprueba si la partida está activa
            print("Primero debe iniciar el juego")#Muestra un aviso
            return#Termina la función
        for fila in range(5):#Recorre las filas
            for columna in range(5):#Recorre las columnas
                casilla = casillas[fila][columna]#Obtiene la casilla
                if casilla["state"] == "normal":#Evita borrar los números fijos
                    casilla.delete(0, tk.END)#Borra el número
        historial.clear()#Elimina el historial de jugadas
        print("Juego borrado")#Confirma que se borró el tablero
    boton_borrar_juego = tk.Button(juego, text="BORRAR JUEGO", command=borrar_juego)#Crea el botón
    boton_borrar_juego.grid(row=14, column=9, columnspan=2, pady=20)#Coloca el botón


    
    def seleccionar_numero(numero):
        seleccionado[0] = numero#Actualiza el número seleccionado
        for boton in botones:
            boton.config(bg="SystemButtonFace")#Quita el color anterior
        botones[numero-1].config(bg="lightgreen")#Pinta el seleccionado
    for numero in range(1, 6):#Recorre los números del 1 al 5
        boton = tk.Button(juego, text=str(numero), width=5, height=2, command=lambda n=numero: seleccionar_numero(n))#Crea el botón
        boton.grid(row=(numero-1)*2+4, column=9, padx=20)#Coloca el botón
        botones.append(boton)#Guarda el botón en la lista
barra_menu = tk.Menu(ventana)#Crea la barra de menú
ventana.config(menu=barra_menu)#Coloca la barra en la ventana
barra_menu.add_command(label="Jugar", command=abrir_juego)#Abre el juego
barra_menu.add_command(label="Configurar")#Configuración
barra_menu.add_command(label="Ayuda")#Manual de usuario
barra_menu.add_command(label="Acerca de")#Información del programa
ventana.mainloop()#Mantiene la ventana abierta




