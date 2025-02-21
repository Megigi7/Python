import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import json
import os

# Clase que representa una celda del tablero
class Celda:
    def __init__(self, x, y, boton):
        self.x = x  # Coordenada x de la celda
        self.y = y  # Coordenada y de la celda
        self.boton = boton  # Botón asociado a la celda en la interfaz
        self.tiene_mina = False  # Indica si la celda tiene una mina
        self.revelada = False  # Indica si la celda ha sido revelada
        self.marcada = False  # Indica si la celda ha sido marcada con una bandera
        self.numero_adyacente = 0  # Número de minas adyacentes a la celda

# Clase que representa el juego de Buscaminas
class Buscaminas:
    def __init__(self, filas=16, columnas=16, minas=40):
        self.filas = filas  # Número de filas del tablero
        self.columnas = columnas  # Número de columnas del tablero
        self.minas = minas  # Número de minas en el tablero
        self.celdas = []  # Lista de celdas del tablero
        self.minas_restantes = minas  # Minas restantes por marcar
        self.tiempo_inicio = None  # Tiempo de inicio del juego
        self.temporizador_activo = False  # Estado del temporizador
        self.records = {"Principiante": [], "Intermedio": [], "Experto": []}  # Lista de récords
        self.cargar_records()  # Cargar los récords desde el archivo
        self.crear_interfaz()  # Crear la interfaz gráfica
        self.iniciar_juego()  # Iniciar el juego

    # Método para crear la interfaz gráfica
    def crear_interfaz(self):
        self.ventana = tk.Tk()  # Crear la ventana principal
        self.ventana.title("Buscaminas")  # Título de la ventana
        self.ventana.geometry("600x400")  # Tamaño de la ventana
        self.ventana.iconbitmap("img/icono.ico")  # Icono de la ventana
        self.ventana.minsize(600, 400)  # Tamaño mínimo de la ventana
        self.ventana.maxsize(600, 400)  # Tamaño máximo de la ventana

        # Crear el encabezado
        self.encabezado = tk.Frame(self.ventana, relief=tk.RAISED, borderwidth=2)
        self.encabezado.pack(side=tk.TOP, fill=tk.X)

        # Título del juego
        self.titulo = tk.Label(self.encabezado, text="BUSCAMINAS", font=("Arial", 16), fg="darkgreen")
        self.titulo.pack(side=tk.LEFT, padx=10)

        # Selector de dificultad
        self.dificultad_label = tk.Label(self.encabezado, text="Dificultad", font=("Arial", 10))
        self.dificultad_label.pack(side=tk.LEFT, padx=10)

        self.dificultad_selector = ttk.Combobox(self.encabezado, values=["Principiante", "Intermedio", "Experto"], state="readonly")
        self.dificultad_selector.set("Intermedio")
        self.dificultad_selector.pack(side=tk.LEFT)
        self.dificultad_selector.bind("<<ComboboxSelected>>", lambda event: self.cambiar_dificultad())

        # Frame para mostrar las minas restantes
        self.minas_frame = tk.Frame(self.encabezado)
        self.minas_frame.pack(side=tk.LEFT, padx=20)

        self.bandera_icono = tk.Label(self.minas_frame, text="\u2691", font=("Arial", 16), fg="red")
        self.bandera_icono.pack(side=tk.LEFT)

        self.minas_restantes_label = tk.Label(self.minas_frame, text=str(self.minas_restantes), font=("Arial", 14))
        self.minas_restantes_label.pack(side=tk.LEFT, padx=5)

        # Temporizador
        self.temporizador = tk.Label(self.encabezado, text="00:00", font=("Arial", 14), relief=tk.SUNKEN, width=6)
        self.temporizador.pack(side=tk.RIGHT, padx=20)

        # Puntajes
        self.puntajes_frame = tk.Frame(self.ventana, relief=tk.SUNKEN, borderwidth=2)
        self.puntajes_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=10)

        self.record_label = tk.Label(self.puntajes_frame, text="RECORDS:", font=("Arial", 12))
        self.record_label.pack(pady=5)

        self.record_puntos = tk.Label(self.puntajes_frame, text="", font=("Arial", 12), relief=tk.SUNKEN, width=8)
        self.record_puntos.pack(pady=5)

        # Frame del tablero
        self.frame_tablero = tk.Frame(self.ventana, relief=tk.SUNKEN, borderwidth=2)
        self.frame_tablero.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Método para iniciar el juego
    def iniciar_juego(self):
        self.celdas = []  # Reiniciar la lista de celdas
        self.minas_restantes = self.minas  # Reiniciar las minas restantes
        self.minas_restantes_label.config(text=str(self.minas_restantes))  # Actualizar el label de minas restantes
        self.tiempo_inicio = None  # Reiniciar el tiempo de inicio
        self.temporizador_activo = False  # Desactivar el temporizador
        self.temporizador.config(text="00:00")  # Reiniciar el temporizador
        self.crear_tablero()  # Crear el tablero
        self.colocar_minas()  # Colocar las minas en el tablero
        self.calcular_numeros_adyacentes()  # Calcular los números adyacentes a cada celda

    # Método para crear el tablero
    def crear_tablero(self):
        for widget in self.frame_tablero.winfo_children():
            widget.destroy()  # Eliminar los widgets existentes en el frame del tablero

        # Configurar el grid para que se expanda
        for i in range(self.filas):
            self.frame_tablero.grid_rowconfigure(i, weight=1)
        for j in range(self.columnas):
            self.frame_tablero.grid_columnconfigure(j, weight=1)

        # Crear los botones del tablero
        for x in range(self.filas):
            fila = []
            for y in range(self.columnas):
                boton = tk.Button(self.frame_tablero, width=3, height=1, command=lambda x=x, y=y: self.revelar_celda(x, y))
                boton.bind("<Button-3>", lambda e, x=x, y=y: self.marcar_celda(x, y))
                boton.grid(row=x, column=y, sticky="nsew")  # Botones expandidos
                boton.config(bg="#b8ea96")

                # Ajuste adicional para la dificultad Principiante
                if self.dificultad_selector.get() == "Principiante":
                    boton.config(width=5, height=2)  # Ajuste del tamaño de las casillas

                fila.append(Celda(x, y, boton))
            self.celdas.append(fila)

    # Método para colocar las minas en el tablero
    def colocar_minas(self):
        posiciones = random.sample([(x, y) for x in range(self.filas) for y in range(self.columnas)], self.minas)
        for x, y in posiciones:
            self.celdas[x][y].tiene_mina = True

    # Método para calcular los números adyacentes a cada celda
    def calcular_numeros_adyacentes(self):
        for x in range(self.filas):
            for y in range(self.columnas):
                if not self.celdas[x][y].tiene_mina:
                    self.celdas[x][y].numero_adyacente = self.contar_minas_adyacentes(x, y)

    # Método para contar las minas adyacentes a una celda
    def contar_minas_adyacentes(self, x, y):
        direcciones = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        minas = 0
        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.filas and 0 <= ny < self.columnas and self.celdas[nx][ny].tiene_mina:
                minas += 1
        return minas

    # Método para revelar una celda
    def revelar_celda(self, x, y):
        if not self.temporizador_activo:
            self.tiempo_inicio = time.time()
            self.temporizador_activo = True
            self.actualizar_temporizador()

        celda = self.celdas[x][y]
        if celda.revelada or celda.marcada:
            return

        celda.revelada = True
        if celda.tiene_mina:
            self.game_over(perdio=True)
            return

        celda.boton.config(text=str(celda.numero_adyacente) if celda.numero_adyacente > 0 else "", bg="#a6ca8f", state="disabled")

        if celda.numero_adyacente == 0:
            self.revelar_en_cascada(x, y)

        self.verificar_victoria()

    # Método para revelar celdas en cascada
    def revelar_en_cascada(self, x, y):
        direcciones = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.filas and 0 <= ny < self.columnas:
                self.revelar_celda(nx, ny)

    # Método para marcar una celda con una bandera
    def marcar_celda(self, x, y):
        celda = self.celdas[x][y]
        if celda.revelada:
            return

        if celda.marcada:
            celda.boton.config(text="", bg="#b8ea96")
            self.minas_restantes += 1
            celda.marcada = not celda.marcada
        else:
            if self.minas_restantes > 0:
                celda.boton.config(text="\u2691", bg="lightblue")
                self.minas_restantes -= 1
                celda.marcada = not celda.marcada

        self.minas_restantes_label.config(text=str(self.minas_restantes))

    # Método para verificar si se ha ganado el juego
    def verificar_victoria(self):
        for fila in self.celdas:
            for celda in fila:
                if not celda.tiene_mina and not celda.revelada:
                    return
        self.game_over(perdio=False)

    # Método para manejar el fin del juego
    def game_over(self, perdio):
        for fila in self.celdas:
            for celda in fila:
                if celda.tiene_mina:
                    if celda.marcada:
                        celda.boton.config(text="💣", state="disabled", bg="lightblue")
                    else:
                        celda.boton.config(text="💣", state="disabled", bg="#d1b29c")
                else:
                    if celda.marcada:
                        celda.boton.config(bg="#b8ea96")
                celda.boton.config(state="disabled")

        self.temporizador_activo = False

        if not perdio:
            tiempo_transcurrido = int(time.time() - self.tiempo_inicio)
            dificultad = self.dificultad_selector.get()
            self.records[dificultad].append(tiempo_transcurrido)
            self.records[dificultad].sort()  # Ordenar los récords de menor a mayor
            self.actualizar_records()
            self.guardar_records()  # Guardar los récords en el archivo

        mensaje = "Has perdido" if perdio else "Has ganado"
        respuesta = messagebox.askyesno("Fin del juego", f"{mensaje}. ¿Quieres jugar de nuevo?")
        if respuesta:
            self.cambiar_dificultad()
        else:
            self.ventana.destroy()

    # Método para actualizar el temporizador
    def actualizar_temporizador(self):
        if self.temporizador_activo:
            tiempo_transcurrido = int(time.time() - self.tiempo_inicio)
            minutos = tiempo_transcurrido // 60
            segundos = tiempo_transcurrido % 60
            self.temporizador.config(text=f"{minutos:02}:{segundos:02}")
            self.ventana.after(1000, self.actualizar_temporizador)

    # Método para actualizar los récords en la interfaz
    def actualizar_records(self):
        dificultad = self.dificultad_selector.get()
        records_text = "\n".join([f"{i+1}. {t//60:02}:{t%60:02}" for i, t in enumerate(self.records[dificultad][:5])])  # Mostrar solo los 5 mejores
        self.record_puntos.config(text=records_text)

    # Método para cambiar la dificultad del juego   
    def cambiar_dificultad(self):
        dificultad = self.dificultad_selector.get()
        if dificultad == "Principiante":
            self.filas = 9; self.columnas = 9; self.minas = 10
        elif dificultad == "Intermedio":
            self.filas = 16; self.columnas = 16; self.minas = 40
        elif dificultad == "Experto":
            self.filas = 16; self.columnas = 30; self.minas = 99

        self.iniciar_juego()
        self.actualizar_records()

    # Método para guardar los récords en un archivo
    def guardar_records(self):
        with open("records.json", "w") as file:
            json.dump(self.records, file)

    # Método para cargar los récords desde un archivo
    def cargar_records(self):
        if os.path.exists("records.json"):
            try:
                with open("records.json", "r") as file:
                    self.records = json.load(file)
            except json.JSONDecodeError:
                self.records = {"Principiante": [], "Intermedio": [], "Experto": []}

if __name__ == "__main__":
    app = Buscaminas()  # Iniciar el juego directamente
    app.ventana.mainloop()