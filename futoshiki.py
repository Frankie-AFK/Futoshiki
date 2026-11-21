import random #Permite seleccionar partidas aleatorias
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
dificultad_actual = tk.StringVar(value="Fácil") #Guarda la dificultad elegida
tipo_reloj = tk.StringVar(value="Cronómetro") #Guarda el tipo de reloj seleccionado
posicion_panel = tk.StringVar(value="Derecha") #Guarda la posición del panel de números
tiempo_timer = [0, 0, 0] #Guarda horas, minutos y segundos del Timer
try: #Intenta recuperar la configuración anterior
    with open("futoshiki2026configuración.dat", "r", encoding="utf-8") as archivo:
        configuracion = json.load(archivo) #Lee las preferencias guardadas
    dificultad_actual.set(configuracion["nivel"]) #Recupera la dificultad
    tipo_reloj.set(configuracion["reloj"]) #Recupera el tipo de reloj
    posicion_panel.set(configuracion["panel"]) #Recupera la posición del panel
    tiempo_timer[0] = configuracion.get("horas", 0) #Recupera las horas
    tiempo_timer[1] = configuracion.get("minutos", 0) #Recupera los minutos
    tiempo_timer[2] = configuracion.get("segundos", 0) #Recupera los segundos
except (FileNotFoundError, json.JSONDecodeError, KeyError): #Si no existe o está incompleta
    configuracion = {} #Mantiene las opciones predeterminadas



def abrir_juego():
    juego = tk.Toplevel(ventana)#Abre otra ventana
    juego.title("Partida de Futoshiki")
    juego.geometry("700x600")#Aumenta el espacio para el panel de dígitos
    iniciado = [False]#Indica si la partida ha comenzado
    terminado = [False]#Indica si la partida ya terminó
    segundos = [0]#Guarda los segundos transcurridos
    reloj_pendiente = [None] #Guarda el identificador del contador
    modo_reloj = [tipo_reloj.get()] #Guarda el modo de reloj de esta partida
    tiempo_limite = [tiempo_timer[0] * 3600 + tiempo_timer[1] * 60 + tiempo_timer[2]] #Guarda el límite del Timer
    desplazamiento = 2 if posicion_panel.get() == "Izquierda" else 0 #Deja espacio para el panel izquierdo
    columna_panel = 0 if posicion_panel.get() == "Izquierda" else 11 #Define dónde aparecen los números
    titulo = tk.Label(juego, text="FUTOSHIKI", font=("Arial", 24, "bold"))#Título del juego
    titulo.grid(row=0, column=0, columnspan=10, pady=10)#Coloca el título arriba
    nivel = tk.Label(juego, text="NIVEL " + dificultad_actual.get().upper(), font=("Arial", 14)) #Muestra la dificultad seleccionada
    nivel.grid(row=1, column=0, columnspan=10)#Coloca el nivel debajo del título
    texto_nombre = tk.Label(juego, text="Nombre del jugador:")#Texto para pedir el nombre
    texto_nombre.grid(row=2, column=0, columnspan=3)#Coloca el texto
    entrada_nombre = tk.Entry(juego, width=25)#Espacio para escribir el nombre
    entrada_nombre.grid(row=2, column=3, columnspan=5)#Coloca la entrada
    reloj = tk.Label(juego, text="00:00:00", font=("Arial", 16))#Muestra el tiempo de la partida
    reloj.grid(row=15, column=0, columnspan=3, pady=10)#Coloca el reloj debajo de los botones
    if tipo_reloj.get() == "No usar reloj": #Comprueba si el reloj está desactivado
        reloj.grid_remove() #Oculta el reloj

    
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
        for dato in partida[0]["desigualdades_horizontales"]:#Recorre las desigualdades
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
        for dato in partida[0]["desigualdades_verticales"]:#Recorre las desigualdades
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






    
    def mostrar_error(casilla, mensaje, anterior): #Muestra un error de jugada
        color_anterior = casilla.cget("bg") #Guarda el color original
        casilla.config(bg="red") #Pinta la casilla incorrecta
        aviso = tk.Toplevel(juego) #Crea la ventana de error
        aviso.title("Jugada no válida") #Coloca el título
        aviso.geometry("460x150") #Define el tamaño
        aviso.transient(juego) #Relaciona el aviso con el juego
        aviso.grab_set() #Bloquea la ventana del juego

        tk.Label(aviso, text=mensaje, wraplength=420).pack(pady=20) #Muestra el mensaje

        def continuar(evento=None): #Continúa después del error
            casilla.delete(0, tk.END) #Elimina el número incorrecto
            casilla.insert(0, anterior) #Recupera el número anterior
            casilla.config(bg=color_anterior) #Restaura el color
            aviso.destroy() #Cierra el aviso

        tk.Button(aviso, text="CONTINUAR", command=continuar).pack() #Crea el botón
        aviso.bind("<Return>", continuar) #Permite continuar con Enter
        aviso.protocol("WM_DELETE_WINDOW", continuar) #Permite cerrar el aviso
        aviso.focus_set() #Activa el teclado





    
    def colocar_numero(fila, columna):#Recibe la posición de la casilla
        if iniciado[0] == False: #Comprueba si el juego no ha iniciado
            print("Primero debe iniciar el juego")#Muestra un aviso
            return#Impide colocar números
        numero = seleccionado[0]#Obtiene el número seleccionado
        if numero != 0:#Comprueba que se seleccionó un número
            casilla = casillas[fila][columna]#Busca la casilla seleccionada
            if casilla["state"] == "normal":#Comprueba que no sea un número fijo
                anterior = casilla.get() #Guarda el valor anterior
                casilla.delete(0, tk.END) #Borra el número anterior antes de colocar el nuevo
                casilla.insert(0, str(numero))#Coloca el número seleccionado
                if validar_fila(fila, numero) == False:#Llama a la función que revisa la fila
                    mostrar_error(casilla, "JUGADA NO ES VÁLIDA PORQUE EL ELEMENTO YA ESTÁ EN LA FILA", anterior)
                    return#Termina la función
                if validar_columna(columna, numero) == False:#Llama a la función que revisa la columna
                    mostrar_error(casilla, "JUGADA NO ES VÁLIDA PORQUE EL ELEMENTO YA ESTÁ EN LA COLUMNA", anterior)
                    return#Termina la función
                if validar_horizontal() == False:#Llama a la función que revisa las desigualdades
                    mostrar_error(casilla, "JUGADA NO ES VÁLIDA PORQUE NO CUMPLE CON UNA DESIGUALDAD HORIZONTAL", anterior)
                    return#Termina la función
                if validar_vertical() == False:#Llama a la función que revisa las desigualdades verticales
                    mostrar_error(casilla, "JUGADA NO ES VÁLIDA PORQUE NO CUMPLE CON UNA DESIGUALDAD VERTICAL", anterior)
                    return#Termina la función
                historial.append((fila, columna, anterior))#Guarda la jugada válida para poder deshacerla
                if tablero_completo() and tablero_correcto(): #Comprueba si el jugador ganó
                    victoria() #Finaliza la partida automáticamente al ganar
        return "break" #Evita que el clic modifique la casilla



    historial = deque()#Crea una pila para guardar las jugadas realizadas                  
    casillas = []#Guarda las casillas del tablero
    for fila in range(5):#Recorre las 5 filas
        fila_casillas = []#Guarda las casillas de una fila
        for columna in range(5):#Recorre las 5 columnas
            casilla = tk.Entry(juego, width=4, font=("Arial", 20), justify="center")
            casilla.grid(row=fila*2+4, column=columna*2+desplazamiento, padx=5, pady=5) #Coloca las casillas según el panel
            casilla.bind("<Button-1>", lambda evento, f=fila, c=columna: colocar_numero(f, c))#Detecta el clic izquierdo
            casilla.bind("<Key>", lambda evento: "break") #Impide escribir directamente con el teclado
            fila_casillas.append(casilla)#Guarda la casilla en su fila
        casillas.append(fila_casillas)#Guarda la fila completa
    nivel_seleccionado = dificultad_actual.get() #Obtiene la dificultad seleccionada
    partidas_nivel = partidas[nivel_seleccionado] #Busca las partidas de esa dificultad
    if len(partidas_nivel) == 0: #Comprueba si hay partidas disponibles
        messagebox.showwarning("Sin partidas", "Todavía no hay partidas para esta dificultad", parent=juego)
        juego.destroy() #Cierra la ventana del juego
        return
    partida = [random.choice(partidas_nivel)] #Permite recuperar el tablero original
    etiquetas_desigualdad = [] #Guarda los símbolos del tablero
    for dato in partida[0]["dígitos_predeterminados"]:#Recorre los números fijos
        fila = dato["fila"] 
        columna = dato["columna"]#Obtiene la columna
        numero = dato["dígito"]#Obtiene el número
        casillas[fila][columna].insert(0, str(numero))#Coloca el número en la casilla
        casillas[fila][columna].config(state="disabled")#Impide modificarlo
    for dato in partida[0]["desigualdades_horizontales"]:#Recorre las desigualdades
        fila = dato["fila"]#Obtiene la fila
        columna = dato["columna"]#Obtiene la columna
        signo = dato["restricción"]#Obtiene el símbolo < o >
        simbolo = tk.Label(juego, text=signo, font=("Arial", 16))#Crea el símbolo
        simbolo.grid(row=fila*2+4, column=columna*2+1+desplazamiento) #Coloca los símbolos horizontales
        etiquetas_desigualdad.append(simbolo) #Guarda el símbolo para restaurarlo
    for dato in partida[0]["desigualdades_verticales"]:#Recorre las desigualdades verticales
        fila = dato["fila"]#Obtiene la fila
        columna = dato["columna"]#Obtiene la columna
        signo = dato["restricción"]#Obtiene el símbolo vertical
        simbolo = tk.Label(juego, text=signo, font=("Arial", 16))#Crea el símbolo
        simbolo.grid(row=fila*2+5, column=columna*2+desplazamiento) #Coloca los símbolos verticales
        etiquetas_desigualdad.append(simbolo) #Guarda el símbolo para restaurarlo
    botones = []#Guarda los botones de los números
    seleccionado = [0]#Guarda el número seleccionado



    def actualizar_reloj(): #Actualiza el reloj según el modo seleccionado
        if iniciado[0] == False: #Comprueba si la partida está detenida
            reloj_pendiente[0] = None #Limpia el contador pendiente
            return
        segundos[0] += 1 #Aumenta el tiempo transcurrido
        if modo_reloj[0] == "Timer": #Comprueba si está usando cuenta regresiva
            tiempo_mostrar = max(0, tiempo_limite[0] - segundos[0]) #Calcula el tiempo restante
        else:
            tiempo_mostrar = segundos[0] #Muestra el tiempo transcurrido
        horas = tiempo_mostrar // 3600 #Calcula las horas
        minutos = (tiempo_mostrar % 3600) // 60 #Calcula los minutos
        seg = tiempo_mostrar % 60 #Calcula los segundos
        reloj.config(text=f"{horas:02}:{minutos:02}:{seg:02}") #Actualiza la pantalla
        if modo_reloj[0] == "Timer" and segundos[0] >= tiempo_limite[0]: #Comprueba si terminó el Timer
            respuesta = messagebox.askyesno(
                "Tiempo expirado",
                "TIEMPO EXPIRADO. ¿Desea continuar el mismo juego?",
                parent=juego
            ) #Pregunta si desea continuar
            if respuesta == True: #Si desea continuar
                modo_reloj[0] = "Cronómetro" #Cambia a cronómetro
                segundos[0] = 0 #Reinicia el cronómetro
                reloj.config(text="00:00:00") #Actualiza el reloj
            else:
                iniciado[0] = False #Detiene la partida
                terminado[0] = True #Marca el juego como terminado
                reloj_pendiente[0] = None #Limpia el contador
                juego.destroy() #Regresa al menú principal
                return
        reloj_pendiente[0] = juego.after(1000, actualizar_reloj) #Programa el siguiente segundo



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
        if modo_reloj[0] == "Timer": #Comprueba si usa cuenta regresiva
            horas = tiempo_limite[0] // 3600 #Calcula las horas iniciales
            minutos = (tiempo_limite[0] % 3600) // 60 #Calcula los minutos iniciales
            seg = tiempo_limite[0] % 60 #Calcula los segundos iniciales
            reloj.config(text=f"{horas:02}:{minutos:02}:{seg:02}") #Muestra el tiempo inicial
        if modo_reloj[0] != "No usar reloj": #Comprueba si debe iniciar el reloj
            reloj_pendiente[0] = juego.after(1000, actualizar_reloj) #Inicia el contador
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



    def victoria():#Finaliza la partida cuando el jugador gana
        iniciado[0] = False#Detiene la partida
        terminado[0] = True#Marca la partida como terminada
        if reloj_pendiente[0] != None:#Comprueba si hay un reloj activo
            juego.after_cancel(reloj_pendiente[0])#Cancela la actualización del reloj
            reloj_pendiente[0] = None#Limpia el reloj pendiente
        guardar_resultado()#Guarda el resultado del ganador
        messagebox.showinfo("¡Victoria!", "¡Felicidades! Completaste el Futoshiki correctamente.", parent=juego)#Muestra el mensaje de victoria



    def terminar_juego():#Termina la partida actual
        if iniciado[0] == False:#Comprueba si el juego no ha comenzado
            print("Primero debe iniciar el juego")#Muestra un aviso
            return#Termina la función
        respuesta = messagebox.askyesno("Terminar juego", "¿Seguro que desea terminar la partida?", parent=juego)#Pregunta si desea terminar
        if respuesta == False:#Comprueba si seleccionó No
            return#Cancela la acción
        iniciado[0] = False #Indica que la partida ya no está activa
        terminado[0] = True #Marca la partida como terminada
        if reloj_pendiente[0] != None: #Comprueba si el reloj está activo
            juego.after_cancel(reloj_pendiente[0]) #Cancela el reloj
            reloj_pendiente[0] = None #Limpia el reloj pendiente
        print("Juego terminado") #Confirma que terminó la partida


        
    
    def guardar_resultado(): #Guarda los mejores tiempos por dificultad
        resultado = { #Crea el resultado del ganador
            "nombre": entrada_nombre.get().strip(), #Guarda el nombre
            "nivel": nivel_seleccionado, #Guarda la dificultad
            "tiempo": segundos[0] #Guarda el tiempo utilizado
        }

        try: #Intenta recuperar los resultados anteriores
            with open("top10.json", "r", encoding="utf-8") as archivo:
                resultados = json.load(archivo) #Lee los resultados
        except (FileNotFoundError, json.JSONDecodeError):
            resultados = [] #Crea una lista vacía si no existe

        resultados.append(resultado) #Agrega el nuevo resultado

        mejores = [] #Guarda los 10 mejores de cada dificultad
        for dificultad in ["Fácil", "Intermedio", "Difícil"]:
            jugadores = [] #Crea la lista de esta dificultad
            for jugador in resultados:
                if jugador["nivel"] == dificultad:
                    jugadores.append(jugador)

            jugadores.sort(key=lambda jugador: jugador["tiempo"]) #Ordena por menor tiempo
            mejores.extend(jugadores[:10]) #Conserva los 10 mejores del nivel

        with open("top10.json", "w", encoding="utf-8") as archivo:
            json.dump(mejores, archivo, ensure_ascii=False, indent=4) #Guarda la clasificación

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


    
    def guardar_partida(): #Guarda el progreso completo
        if not iniciado[0]: #Comprueba que la partida esté activa
            messagebox.showwarning("Aviso", "Primero debe iniciar el juego", parent=juego)
            return

        tablero = [] #Guarda los números del jugador
        for fila in range(5):
            fila_actual = []
            for columna in range(5):
                fila_actual.append(casillas[fila][columna].get())
            tablero.append(fila_actual)

        datos = { #Reúne todos los datos necesarios
            "nombre": entrada_nombre.get().strip(),
            "nivel": nivel_seleccionado,
            "tiempo": segundos[0],
            "tablero": tablero,
            "original": partida[0],
            "modo_reloj": modo_reloj[0],
            "tiempo_limite": tiempo_limite[0] #Guarda el límite del Timer
        }

        with open("partidas_guardadas.json", "a", encoding="utf-8") as archivo:
            archivo.write(json.dumps(datos, ensure_ascii=False) + "\n")

        messagebox.showinfo("Guardar", "Partida guardada correctamente", parent=juego)

    boton_guardar = tk.Button(juego, text="GUARDAR PARTIDA", command=guardar_partida)#Crea el botón para guardar
    boton_guardar.grid(row=16, column=0, columnspan=3, pady=10)#Coloca el botón debajo del reloj






    def restaurar_tablero(datos): #Recupera pistas, números y desigualdades
        nonlocal nivel_seleccionado

        if "original" not in datos: #Detecta partidas del formato anterior
            messagebox.showwarning(
                "Partida antigua",
                "Esta partida no tiene las pistas originales. Guarde una nueva partida.",
                parent=juego
            )
            return False

        partida[0] = datos["original"] #Recupera el problema original
        nivel_seleccionado = datos["nivel"] #Recupera la dificultad
        nivel.config(text="NIVEL " + nivel_seleccionado.upper())

        for fila in range(5): #Limpia todas las casillas
            for columna in range(5):
                casilla = casillas[fila][columna]
                casilla.config(state="normal")
                casilla.delete(0, tk.END)
                casilla.insert(0, datos["tablero"][fila][columna])

        for dato in partida[0]["dígitos_predeterminados"]:
            casillas[dato["fila"]][dato["columna"]].config(state="disabled")

        for etiqueta in etiquetas_desigualdad: #Elimina las pistas anteriores
            etiqueta.destroy()
        etiquetas_desigualdad.clear()

        for dato in partida[0]["desigualdades_horizontales"]:
            etiqueta = tk.Label(juego, text=dato["restricción"], font=("Arial", 16))
            etiqueta.grid(row=dato["fila"]*2+4,
                          column=dato["columna"]*2+1+desplazamiento)
            etiquetas_desigualdad.append(etiqueta)

        for dato in partida[0]["desigualdades_verticales"]:
            etiqueta = tk.Label(juego, text=dato["restricción"], font=("Arial", 16))
            etiqueta.grid(row=dato["fila"]*2+5,
                          column=dato["columna"]*2+desplazamiento)
            etiquetas_desigualdad.append(etiqueta)

        return True







    def cargar_partida():#Recupera una partida guardada
        try:#Intenta abrir el archivo
            with open("partidas_guardadas.json", "r", encoding="utf-8") as archivo: #Abre las partidas guardadas
                partidas = [json.loads(linea) for linea in archivo if linea.strip()] #Lee cada partida del archivo
                if len(partidas) == 0: #Comprueba si no hay partidas guardadas
                    messagebox.showwarning("Sin partidas", "No hay partidas guardadas", parent=juego)
                    return
                opciones = [] #Guarda las opciones para seleccionar
                for i in range(len(partidas)): #Recorre las partidas guardadas
                    partida = partidas[i]
                    opciones.append(str(i + 1) + ". " + partida["nombre"] + " - " + partida["nivel"])
                ventana_partidas = tk.Toplevel(juego) #Crea una ventana para seleccionar partidas
                ventana_partidas.title("Partidas guardadas") #Coloca el título
                ventana_partidas.geometry("400x300") #Establece el tamaño
                tk.Label(ventana_partidas, text="SELECCIONAR PARTIDA").pack(pady=10) #Muestra el título
                lista_partidas = tk.Listbox(ventana_partidas, width=45, height=8) #Crea la lista
                lista_partidas.pack(pady=10) #Coloca la lista en la ventana
                for opcion in opciones: #Recorre las partidas disponibles
                    lista_partidas.insert(tk.END, opcion) #Agrega cada partida a la lista
                def cargar_seleccionada(): #Carga la partida elegida por el jugador
                    seleccion = lista_partidas.curselection() #Obtiene la posición seleccionada
                    if len(seleccion) == 0: #Comprueba si no seleccionó ninguna partida
                        messagebox.showwarning("Aviso", "Seleccione una partida", parent=ventana_partidas)
                        return #Evita continuar sin seleccionar
                    datos = partidas[seleccion[0]] #Obtiene los datos de la partida seleccionada
                    ventana_partidas.destroy() #Cierra la ventana de selección
                    if not restaurar_tablero(datos): #Recupera el tablero original
                        return
                    entrada_nombre.delete(0, tk.END) #Limpia el nombre anterior
                    entrada_nombre.insert(0, datos["nombre"]) #Recupera el jugador
                    segundos[0] = datos["tiempo"] #Recupera el tiempo transcurrido
                    modo_reloj[0] = datos.get("modo_reloj", "Cronómetro") #Recupera el tipo de reloj
                    tiempo_limite[0] = datos.get("tiempo_limite", tiempo_limite[0]) #Recupera el límite del Timer
                    if modo_reloj[0] == "Timer": #Calcula el tiempo restante
                        tiempo_mostrar = max(0, tiempo_limite[0] - segundos[0])
                    else:
                        tiempo_mostrar = segundos[0]
                    horas = tiempo_mostrar // 3600 #Calcula las horas
                    minutos = (tiempo_mostrar % 3600) // 60 #Calcula los minutos
                    seg = tiempo_mostrar % 60 #Calcula los segundos
                    reloj.config(text=f"{horas:02}:{minutos:02}:{seg:02}") #Actualiza el reloj

                    if modo_reloj[0] == "No usar reloj":
                        reloj.grid_remove() #Oculta el reloj
                    else:
                        reloj.grid() #Muestra el reloj

                    historial.clear() #Limpia el historial
                    terminado[0] = False #Permite continuar la partida
                    iniciado[0] = True #Activa el juego

                    if reloj_pendiente[0] is not None: #Evita duplicar el reloj
                        juego.after_cancel(reloj_pendiente[0])
                        reloj_pendiente[0] = None

                    if modo_reloj[0] != "No usar reloj":
                        reloj_pendiente[0] = juego.after(1000, actualizar_reloj)

                    print("Partida cargada correctamente")

                boton_seleccionar = tk.Button(ventana_partidas, text="CARGAR SELECCIONADA", command=cargar_seleccionada) #Crea el botón para cargar
                boton_seleccionar.pack(pady=10) #Coloca el botón debajo de la lista
        except FileNotFoundError:#Detecta si el archivo no existe
            print("No hay ninguna partida guardada")#Muestra un aviso
            return#Termina la función
    boton_cargar = tk.Button(juego, text="CARGAR PARTIDA", command=cargar_partida)#Crea el botón para cargar
    boton_cargar.grid(row=16, column=6, columnspan=3, pady=10)#Coloca el botón junto a guardar


    
    def seleccionar_numero(numero):
        seleccionado[0] = numero#Actualiza el número seleccionado
        for boton in botones:
            boton.config(bg="SystemButtonFace")#Quita el color anterior
        botones[numero-1].config(bg="lightgreen")#Pinta el seleccionado
    for numero in range(1, 6):#Recorre los números del 1 al 5
        boton = tk.Button(juego, text=str(numero), width=5, height=2, command=lambda n=numero: seleccionar_numero(n))#Crea el botón
        boton.grid(row=(numero-1)*2+4, column=columna_panel, padx=10) #Coloca los números según la configuración
        botones.append(boton)#Guarda el botón en la lista



def mostrar_top10():#Abre la ventana de clasificación
    ventana_top = tk.Toplevel(ventana)#Crea una ventana nueva
    ventana_top.title("TOP 10")#Coloca el título
    ventana_top.geometry("400x400")#Establece el tamaño
    titulo = tk.Label(ventana_top, text="MEJORES 10 JUGADORES", font=("Arial", 16, "bold"))#Crea el título
    titulo.pack(pady=15)#Coloca el título en la ventana
    resultados = []#Crea una lista para los mejores jugadores
    try:#Intenta abrir el archivo de clasificación
        with open("top10.json", "r", encoding="utf-8") as archivo:
            resultados = json.load(archivo)#Lee los resultados guardados
    except FileNotFoundError:#Si todavía no existe el archivo
        resultados = []#Deja la lista vacía
    print(resultados)#Muestra los resultados para comprobarlos
    nivel_top = dificultad_actual.get() #Obtiene la dificultad actual
    resultados = [jugador for jugador in resultados if jugador["nivel"] == nivel_top] #Filtra por dificultad
    resultados.sort(key=lambda jugador: jugador["tiempo"]) #Ordena de menor a mayor tiempo
    resultados = resultados[:10] #Muestra solamente los 10 mejores
    tk.Label(ventana_top, text="DIFICULTAD: " + nivel_top.upper(), font=("Arial", 12, "bold")).pack(pady=5) #Muestra el nivel
    if len(resultados) == 0:#Comprueba si no hay jugadores
        texto = tk.Label(ventana_top, text="Todavía no hay resultados")#Crea el mensaje
        texto.pack(pady=10)#Muestra el mensaje
    else:#Si existen resultados
        for i in range(len(resultados)):#Recorre los jugadores
            jugador = resultados[i] #Obtiene los datos del jugador
            texto = str(i + 1) + ". " + jugador["nombre"] + " - " + jugador["nivel"] + " - " + str(jugador["tiempo"]) + " segundos" #Muestra nombre, dificultad y tiempo
            etiqueta = tk.Label(ventana_top, text=texto, font=("Arial", 12))#Crea la etiqueta
            etiqueta.pack(pady=5)#Muestra el jugador



def abrir_configuracion(): #Abre la ventana de configuración
    ventana_config = tk.Toplevel(ventana) #Crea una ventana nueva
    ventana_config.title("Configuración") #Coloca el título
    ventana_config.geometry("400x650") #Amplía la ventana para el Timer
    titulo = tk.Label(ventana_config, text="CONFIGURACIÓN DEL JUEGO",font=("Arial", 16, "bold")) #Crea el título
    titulo.pack(pady=15) #Muestra el título
    texto_nivel = tk.Label(ventana_config, text="Seleccione la dificultad:") #Crea el texto de dificultad
    texto_nivel.pack(pady=10) #Muestra el texto
    dificultad = dificultad_actual #Utiliza la dificultad guardada del programa
    for opcion in ["Fácil", "Intermedio", "Difícil"]: #Recorre las dificultades
        boton = tk.Radiobutton(ventana_config, text=opcion, variable=dificultad, value=opcion) #Crea una opción
        boton.pack(pady=5) #Muestra la opción
    tk.Label(ventana_config, text="Tipo de reloj:").pack(pady=10) #Muestra el título del reloj
    for opcion in ["Cronómetro", "Timer", "No usar reloj"]: #Recorre los tipos de reloj
        tk.Radiobutton(ventana_config, text=opcion, variable=tipo_reloj, value=opcion).pack() #Permite seleccionar el reloj
    tk.Label(ventana_config, text="Posición del panel:").pack(pady=10) #Muestra el título del panel
    for opcion in ["Derecha", "Izquierda"]: #Recorre las posiciones
        tk.Radiobutton(ventana_config, text=opcion, variable=posicion_panel, value=opcion).pack() #Permite seleccionar la posición
    tk.Label(ventana_config, text="Tiempo del Timer (H / M / S):").pack(pady=5) #Muestra el tiempo
    horas_timer = tk.Entry(ventana_config, width=5) #Entrada de horas
    horas_timer.pack()
    horas_timer.insert(0, str(tiempo_timer[0])) #Muestra las horas guardadas
    minutos_timer = tk.Entry(ventana_config, width=5) #Entrada de minutos
    minutos_timer.pack()
    minutos_timer.insert(0, str(tiempo_timer[1])) #Muestra los minutos guardados
    segundos_timer = tk.Entry(ventana_config, width=5) #Entrada de segundos
    segundos_timer.pack()
    segundos_timer.insert(0, str(tiempo_timer[2])) #Muestra los segundos guardados
    def guardar_configuracion(): #Guarda las preferencias del jugador
        horas = horas_timer.get().strip() #Obtiene las horas
        minutos = minutos_timer.get().strip() #Obtiene los minutos
        segundos_t = segundos_timer.get().strip() #Obtiene los segundos
        if tipo_reloj.get() == "Timer": #Valida solamente si seleccionó Timer
            if not horas.isdigit() or not minutos.isdigit() or not segundos_t.isdigit(): #Comprueba que sean números
                messagebox.showerror("Error", "Ingrese solamente números", parent=ventana_config)
                return
            if int(horas) > 2 or int(minutos) > 59 or int(segundos_t) > 59: #Comprueba los límites
                messagebox.showerror("Error", "Tiempo fuera del rango permitido", parent=ventana_config)
                return
            if int(horas) == 0 and int(minutos) == 0 and int(segundos_t) == 0: #Evita un Timer vacío
                messagebox.showerror("Error", "El Timer debe ser mayor que cero", parent=ventana_config)
                return
        datos = { #Agrupa las opciones seleccionadas
            "nivel": dificultad_actual.get(),
            "reloj": tipo_reloj.get(),
            "panel": posicion_panel.get(),
            "horas": int(horas) if horas.isdigit() else 0, #Guarda las horas
            "minutos": int(minutos) if minutos.isdigit() else 0, #Guarda los minutos
            "segundos": int(segundos_t) if segundos_t.isdigit() else 0 #Guarda los segundos
        }
        with open("futoshiki2026configuración.dat", "w", encoding="utf-8") as archivo: #Abre el archivo
            json.dump(datos, archivo, ensure_ascii=False, indent=4) #Guarda la configuración
        tiempo_timer[0] = datos["horas"] #Actualiza las horas guardadas
        tiempo_timer[1] = datos["minutos"] #Actualiza los minutos guardados
        tiempo_timer[2] = datos["segundos"] #Actualiza los segundos guardados
        messagebox.showinfo("Configuración", "Configuración guardada correctamente", parent=ventana_config) #Confirma el guardado
        ventana_config.destroy() #Cierra la ventana

    tk.Button(ventana_config, text="GUARDAR CONFIGURACIÓN", command=guardar_configuracion).pack(pady=20) #Crea el botón









def mostrar_ayuda(): #Abre el manual de usuario en PDF
    import os #Permite abrir archivos del sistema

    carpeta = os.path.dirname(os.path.abspath(__file__)) #Obtiene la carpeta del programa
    ruta = os.path.join(carpeta, "manual_de_usuario_futoshiki.pdf") #Busca el manual

    if os.path.exists(ruta): #Comprueba si existe el PDF
        os.startfile(ruta) #Abre el manual en Windows
    else:
        messagebox.showerror("Error", "No se encontró el manual de usuario PDF") #Muestra el error



def mostrar_acerca_de(): #Abre la información del programa
    acerca = tk.Toplevel(ventana) #Crea una ventana nueva
    acerca.title("Acerca de - Futoshiki") #Coloca el título
    acerca.geometry("450x350") #Define el tamaño

    tk.Label(acerca, text="FUTOSHIKI", font=("Arial", 22, "bold")).pack(pady=20) #Muestra el nombre
    tk.Label(acerca, text="Proyecto 2 - Introducción a la Programación", font=("Arial", 12)).pack(pady=10) #Muestra el proyecto
    tk.Label(acerca, text="Instituto Tecnológico de Costa Rica").pack(pady=5) #Muestra la institución
    tk.Label(acerca, text="Desarrollado por: Frankie Cheng Zheng").pack(pady=5) #Muestra el autor
    tk.Label(acerca, text="Año: 2026").pack(pady=5) #Muestra el año
    tk.Label(acerca, text="Juego de lógica Futoshiki 5x5").pack(pady=10) #Describe el programa

    tk.Button(acerca, text="CERRAR", command=acerca.destroy).pack(pady=15) #Cierra la ventana





        
barra_menu = tk.Menu(ventana)#Crea la barra de menú
ventana.config(menu=barra_menu)#Coloca la barra en la ventana
barra_menu.add_command(label="Jugar", command=abrir_juego)#Abre el juego
barra_menu.add_command(label="TOP 10", command=mostrar_top10) #Abre la clasificación
barra_menu.add_command(label="Configurar", command=abrir_configuracion) #Abre la configuración
barra_menu.add_command(label="Ayuda", command=mostrar_ayuda) #Abre las instrucciones del juego
barra_menu.add_command(label="Acerca de", command=mostrar_acerca_de) #Abre la información del programa
ventana.mainloop()#Mantiene la ventana abierta
