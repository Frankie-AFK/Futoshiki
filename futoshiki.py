import json#Permite trabajar con archivos JSON
import tkinter as tk#Importa la librería para crear ventanas
import time#Permite trabajar con el tiempo
from collections import deque#Importa deque para manejar la pila de jugadas
from tkinter import messagebox#Permite mostrar ventanas de confirmación
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
    reloj_pendiente = [None] #Guarda el identificador del contador
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



    historial = deque()#Crea una pila para guardar las jugadas realizadas                  
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



    def actualizar_reloj():#Actualiza el tiempo de la partida
        if iniciado[0] == True:#Comprueba si el juego está activo
            segundos[0] += 1#Aumenta un segundo
            horas = segundos[0] // 3600#Calcula las horas
            minutos = (segundos[0] % 3600) // 60#Calcula los minutos
            seg = segundos[0] % 60#Calcula los segundos
            reloj.config(text=f"{horas:02}:{minutos:02}:{seg:02}")#Muestra el tiempo
        if iniciado[0] == True: #Comprueba si debe seguir contando
            reloj_pendiente[0] = juego.after(1000, actualizar_reloj)#Programa el siguiente segundo
        else:
            reloj_pendiente[0] = None#Indica que el contador se detuvo



    def iniciar_juego():#Función para iniciar la partida
        if iniciado[0] == True:#Evita iniciar dos veces la misma partida
            print("El juego ya está iniciado")#Muestra un aviso
            return#Termina la función
        if terminado[0] == True:#Comprueba si la partida ya terminó
            print("La partida ya terminó")#Muestra un aviso
            return#Impide reiniciar la partida
        nombre = entrada_nombre.get().strip()#Obtiene el nombre del jugador
        if nombre == "":#Comprueba si está vacío
            print("Debe escribir el nombre del jugador")#Muestra un aviso
            return#No inicia el juego
        iniciado[0] = True#Permite jugar
        segundos[0] = 0#Reinicia el contador a cero
        reloj_pendiente[0] = juego.after(1000, actualizar_reloj)#Inicia el reloj después de un segundo
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



    def tablero_completo():#Comprueba si todas las casillas tienen números
        for fila in range(5):#Recorre las 5 filas
            for columna in range(5):#Recorre las 5 columnas
                if casillas[fila][columna].get() == "":#Busca casillas vacías
                    return False#El tablero todavía está incompleto
        return True#Todas las casillas tienen números



    def tablero_correcto():#Comprueba si la solución cumple las reglas
        for fila in range(5):#Recorre las filas
            for columna in range(5):#Recorre las columnas
                numero = casillas[fila][columna].get()#Obtiene el número
                if validar_fila(fila, numero) == False:#Comprueba la fila
                    return False#Hay números repetidos
                if validar_columna(columna, numero) == False:#Comprueba la columna
                    return False#Hay números repetidos
        if validar_horizontal() == False:#Comprueba desigualdades horizontales
            return False#Hay una desigualdad incorrecta
        if validar_vertical() == False:#Comprueba desigualdades verticales
            return False#Hay una desigualdad incorrecta
        return True#La solución es correcta



    def terminar_juego():#Termina la partida actual
        if iniciado[0] == False:#Comprueba si el juego no ha comenzado
            print("Primero debe iniciar el juego")#Muestra un aviso
            return#Termina la función
        if tablero_completo() == False:#Comprueba si faltan números
            messagebox.showwarning("Tablero incompleto", "Todavía hay casillas vacías", parent=juego)#Muestra un aviso
            return#Impide terminar una partida incompleta
        if tablero_correcto() == False:#Comprueba si la solución es correcta
            messagebox.showwarning("Solución incorrecta", "El tablero no cumple las reglas", parent=juego)#Muestra un aviso
            return#Permite corregir el tablero
        respuesta = messagebox.askyesno("Terminar juego", "¿Seguro que desea terminar la partida?", parent=juego)#Pregunta si desea terminar
        if respuesta == False:#Comprueba si seleccionó No
            return#Cancela la acción
        iniciado[0] = False#Impide seguir colocando números
        terminado[0] = True#Marca la partida como terminada
        print("Juego terminado")#Confirma que terminó la partida
    boton_terminar = tk.Button(juego, text="TERMINAR JUEGO", command=terminar_juego)#Crea el botón
    boton_terminar.grid(row=14, column=6, columnspan=3, pady=20)#Coloca el botón debajo del tablero



    def borrar_juego():#Borra los números colocados por el jugador
        if iniciado[0] == False:#Comprueba si la partida está activa
            print("Primero debe iniciar el juego")#Muestra un aviso
            return#Termina la función
        respuesta = messagebox.askyesno("Borrar juego", "¿Seguro que desea borrar el tablero?", parent=juego)#Pregunta si desea borrar
        if respuesta == False:#Comprueba si seleccionó No
            return#Cancela la acción
        for fila in range(5):#Recorre las filas
            for columna in range(5):#Recorre las columnas
                casilla = casillas[fila][columna]#Obtiene la casilla
                if casilla["state"] == "normal":#Evita borrar los números fijos
                    casilla.delete(0, tk.END)#Borra el número
        historial.clear()#Elimina el historial de jugadas
        print("Juego borrado")#Confirma que se borró el tablero
    boton_borrar_juego = tk.Button(juego, text="BORRAR JUEGO", command=borrar_juego)#Crea el botón
    boton_borrar_juego.grid(row=14, column=9, columnspan=2, pady=20)#Coloca el botón



    def guardar_partida():#Guarda el progreso de la partida
        if iniciado[0] == False:#Comprueba si el juego está activo
            print("Primero debe iniciar el juego")
            return
        tablero = []#Lista para guardar los números del tablero
        for fila in range(5):#Recorre las 5 filas
            fila_actual = []#Guarda los números de una fila
            for columna in range(5):#Recorre las 5 columnas
                numero = casillas[fila][columna].get()#Obtiene el número de la casilla
                fila_actual.append(numero)#Agrega el número a la fila
            tablero.append(fila_actual)#Agrega la fila al tablero
            datos_guardados = {#Agrupa los datos de la partida
            "nombre": entrada_nombre.get().strip(),#Guarda el nombre del jugador
            "nivel": "Fácil",#Guarda la dificultad actual
            "tiempo": segundos[0],#Guarda los segundos transcurridos
            "tablero": tablero#Guarda los números del tablero
            }
        with open("partida_guardada.json", "w", encoding="utf-8") as archivo:#Abre el archivo para guardar
            json.dump(datos_guardados, archivo, indent=4, ensure_ascii=False)#Escribe los datos en JSON
        print("Partida guardada correctamente")#Confirma que se guardó
    boton_guardar = tk.Button(juego, text="GUARDAR PARTIDA", command=guardar_partida)#Crea el botón para guardar
    boton_guardar.grid(row=16, column=0, columnspan=3, pady=10)#Coloca el botón debajo del reloj



    def cargar_partida():#Recupera una partida guardada
        try:#Intenta abrir el archivo
            with open("partida_guardada.json", "r", encoding="utf-8") as archivo:#Abre la partida guardada
                datos = json.load(archivo)#Convierte el JSON en datos de Python
        except FileNotFoundError:#Detecta si el archivo no existe
            print("No hay ninguna partida guardada")#Muestra un aviso
            return#Termina la función
        entrada_nombre.delete(0, tk.END)#Borra el nombre anterior
        entrada_nombre.insert(0, datos["nombre"])#Recupera el nombre guardado
        segundos[0] = datos["tiempo"]#Recupera los segundos guardados
        horas = segundos[0] // 3600#Calcula las horas
        minutos = (segundos[0] % 3600) // 60#Calcula los minutos
        seg = segundos[0] % 60#Calcula los segundos
        reloj.config(text=f"{horas:02}:{minutos:02}:{seg:02}")#Muestra el tiempo recuperado
        tablero = datos["tablero"]#Obtiene el tablero guardado
        for fila in range(5):#Recorre las 5 filas
            for columna in range(5):#Recorre las 5 columnas
                casilla = casillas[fila][columna]#Obtiene la casilla actual
                if casilla["state"] == "normal":#Evita modificar números fijos
                    casilla.delete(0, tk.END)#Borra el número anterior
                    casilla.insert(0, tablero[fila][columna])#Coloca el número guardado
        historial.clear()#Limpia las jugadas de la partida anterior
        terminado[0] = False#Permite continuar la partida guardada
        iniciado[0] = True#Activa la partida recuperada
        if reloj_pendiente[0] != None:#Comprueba si existe un contador anterior
            juego.after_cancel(reloj_pendiente[0])#Cancela el contador anterior
            reloj_pendiente[0] = None#Limpia el identificador
        reloj_pendiente[0] = juego.after(1000, actualizar_reloj)#Continúa el reloj después de un segundo
        print("Partida cargada correctamente")#Confirma que se cargó
    boton_cargar = tk.Button(juego, text="CARGAR PARTIDA", command=cargar_partida)#Crea el botón para cargar
    boton_cargar.grid(row=16, column=6, columnspan=3, pady=10)#Coloca el botón junto a guardar


    
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
