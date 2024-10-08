import customtkinter
import random
import time
import threading
from queue import Queue

# Configuraciones iniciales de la apariencia de la GUI
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("Hades.json")

# Clase PCB (Process Control Block) que representa un proceso en el sistema
class PCB:
    def __init__(self, pid, memoria_requerida, tiempo_limite):
        self.pid = pid  # Identificador único del proceso
        self.estado = "Nuevo"  # Estado inicial del proceso
        self.memoria_requerida = memoria_requerida  # Cantidad de memoria requerida por el proceso
        self.contador_programa = 0  # Contador de instrucciones ejecutadas
        self.tiempo_inicio = time.time()  # Tiempo de inicio del proceso
        self.tiempo_limite = tiempo_limite  # Tiempo máximo de ejecución
        self.tiempo_ejecucion = 0 # El tiempo que el proceso lleva en ejecución 

# Clase Memoria que maneja la asignación y liberación de la memoria principal
class Memoria:
    def __init__(self, limite):
        self.limite = limite  # Límite máximo de memoria disponible
        self.usada = 0  # Memoria actualmente en uso

    # Método para asignar memoria a un proceso
    def asignar_memoria(self, pcb):
        if self.usada + pcb.memoria_requerida <= self.limite:
            pcb.estado = "Listo" # Actualizar el estado del proceso
            self.usada += pcb.memoria_requerida  # Se asigna la memoria requerida
            return True
        return False

    # Método para liberar la memoria cuando un proceso termina
    def liberar_memoria(self, pcb):
        if pcb.estado == "Terminado":
            return
        
        self.usada -= pcb.memoria_requerida  # Se libera la memoria usada por el proceso

# Clase Planificador que maneja la planificación de procesos según el algoritmo seleccionado
class Planificador:
    def __init__(self, algoritmo="FCFS", quantum=2):
        self.listos = list()  # Lista de procesos listos
        self.enEspera = list()  # Lista de procesos nuevos o en espera
        self.algoritmo = algoritmo  # Algoritmo de planificación seleccionado
        self.quantum = quantum  # Quantum para el algoritmo Round Robin (en segundos)
        self.enEjecucion = None # Proceso en ejecución

    # Método para agregar un proceso a la cola de listos
    def agregar_proceso(self, pcb, memoria_asignada):
        if memoria_asignada == False:
            self.enEspera.append(pcb)
        else:
            self.listos.append(pcb)

    # Método para obtener el siguiente proceso según el algoritmo de planificación
    def obtener_proceso(self):
        global app
        if self.algoritmo == "RR":
            if self.enEjecucion != None:
                if self.enEjecucion.tiempo_ejecucion < self.quantum: # Si el proceso no termina su ejecución dentro del quantum, se realiza un cambio de contexto
                    return self.enEjecucion
                if self.enEjecucion.tiempo_ejecucion > self.enEjecucion.tiempo_limite:
                    app.memoria.liberar_memoria(self.enEjecucion)
                    self.enEjecucion.estado = "Terminado"
                else:
                    self.enEjecucion.estado = "Listo" # Actualizamos el estado del antiguo proceso a ejecutar
                    self.listos.append(self.enEjecucion) # Ponemos el proceso en la lista de procesos listos para ejecutarse
        elif self.enEjecucion != None: # Si el proceso todavia no termino de ejecutarse, devolvemos el valor
            if self.enEjecucion.tiempo_ejecucion < self.enEjecucion.tiempo_limite:
                return self.enEjecucion

        # Elegimos un nuevo proceso a ejecutar
        if self.algoritmo == "FCFS":
            self.enEjecucion = self.listos.pop(0) if not len(self.listos) == 0 else None
        elif self.algoritmo == "SJN":
            self.enEjecucion = self.obtener_sjn() # Obtener el proceso más corto
        elif self.algoritmo == "RR":
            self.enEjecucion = self.listos.pop(0) if not len(self.listos) == 0 else None
        
        if self.enEjecucion != None:
            self.enEjecucion.estado = "En ejecución"
        return self.enEjecucion

    # Método específico para el algoritmo SJN (Shortest Job Next)
    def obtener_sjn(self):
        if len(self.listos) != 0:
            proceso_mas_corto = min(self.listos, key=lambda p: p.tiempo_limite)
            self.listos.remove(proceso_mas_corto)
            return proceso_mas_corto
        return None

    # # Método para ejecutar un proceso usando Round Robin
    # def ejecutar_rr(self, pcb):
    #     time.sleep(self.quantum)
    #     pcb.contador_programa += 1
    #     self.listos.put(pcb)

# Clase principal de la aplicación, que maneja la interfaz gráfica y la simulación
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configuramos la ventana principal de la aplicación
        self.title("Tp Sistemas: Gestión de Procesos")
        self.geometry(f"{900}x{580}")

        # Configuración del layout principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Creamos un frame lateral para contener los widgets de control
        self.frameLateral = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.frameLateral.grid(row=0, column=0, rowspan=6, sticky="nsew")
        self.frameLateral.grid_rowconfigure(4, weight=1)
        
        # Título del frame lateral
        self.logo = customtkinter.CTkLabel(self.frameLateral, text="Gestión de Memoria", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        #Creamos una vision de pestañas
        self.vistaPestaña = customtkinter.CTkTabview(self, width=250)
        self.vistaPestaña.grid(row=5, column=0, pady=(20, 0), sticky="nsew")
        self.vistaPestaña.add("Ejecución")
        self.vistaPestaña.add("Apariencia")
        self.vistaPestaña.tab("Ejecución").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.vistaPestaña.tab("Apariencia").grid_columnconfigure(0, weight=1)
        
        # Botón para iniciar la ejecución de un proceso
        self.botonProceso = customtkinter.CTkButton(self.frameLateral, text="Iniciar simulación", command=self.EjecutarProceso)
        self.botonProceso.grid(row=1, column=0, padx=20, pady=10, sticky="ew") 
        
        # Botón para cambiar la cantidad de memoria disponible
        self.cambiarMemoria = customtkinter.CTkButton(self.frameLateral, text="Cambiar Cantidad de Memoria", command=self.ingresoPorPantalla)
        self.cambiarMemoria.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        # Botón para detener la simulación
        self.pararSimulacion = customtkinter.CTkButton(self.frameLateral, text="Parar Simulación", command=self.parar_simulacion)
        self.pararSimulacion.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        # Menú para seleccionar el algoritmo de planificación
        self.labelAlgoritmo = customtkinter.CTkLabel(self.vistaPestaña.tab("Ejecución"), text="Algoritmo de Planificación:", anchor="w")
        self.labelAlgoritmo.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.menuAlgoritmo = customtkinter.CTkOptionMenu(self.vistaPestaña.tab("Ejecución"), values=["FCFS", "SJN", "RR"], command=self.cambiarAlgoritmo)
        self.menuAlgoritmo.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        # Campo de entrada para definir la cantidad de hilos
        self.labelHilos = customtkinter.CTkLabel(self.vistaPestaña.tab("Ejecución"), text="Cantidad de Hilos:", anchor="w")
        self.labelHilos.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.entryHilos = customtkinter.CTkEntry(self.vistaPestaña.tab("Ejecución"))
        self.entryHilos.grid(row=8, column=0, padx=20, pady=(10, 10))
        self.entryHilos.insert(0, "1")  # Valor por defecto de 1 hilo

        #creamos un título y un menú para cambiar la apariencia de la pestaña
        self.etiquetaDeApariencia = customtkinter.CTkLabel(self.vistaPestaña.tab("Apariencia"), text="Modo:", anchor="w")
        self.etiquetaDeApariencia.grid(row=0, column=0, padx=20, pady=(10, 0))
        self.menuDeApariencia = customtkinter.CTkOptionMenu(self.vistaPestaña.tab("Apariencia"), 
                                                            values=["Light", "Dark"],
                                                            command=self.cambiarApariencia)
        self.menuDeApariencia.grid(row=0, column=0, padx=20, pady=(10, 10))
        self.menuDeApariencia.set("Dark")
        
        self.etiquetaDeEscala = customtkinter.CTkLabel(self.vistaPestaña.tab("Apariencia"), text="Escala de la Interfaz:", anchor="w")
        self.etiquetaDeEscala.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.menuDeescala = customtkinter.CTkOptionMenu(self.vistaPestaña.tab("Apariencia"), values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.cambiarEscala)
        self.menuDeescala.grid(row=9, column=0, padx=20, pady=(10, 20))
        self.menuDeescala.set("100%")
        
        # Frame para la barra de progreso de uso de memoria
        self.frameDeBarraDeProgreso = customtkinter.CTkFrame(self, fg_color="transparent")
        self.frameDeBarraDeProgreso.grid(row=5, column=1, padx=(20, 0), pady=(20, 0), sticky="ew")
        self.frameDeBarraDeProgreso.grid_columnconfigure(0, weight=1)
        self.frameDeBarraDeProgreso.grid_rowconfigure(4, weight=1)
        self.barraProgreso = customtkinter.CTkProgressBar(self.frameDeBarraDeProgreso)
        self.barraProgreso.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="nsew")
    
        # Espacio de texto para mostrar mensajes y el estado del sistema
        self.textbox = customtkinter.CTkTextbox(self, width=200, height=600)
        self.textbox.grid(row=0, column=1, padx=(2, 0), pady=(2, 0), sticky="nsew")

        # Inicialización de la simulación
        self.memoria = Memoria(1024)  # Inicialización de la memoria principal
        self.planificador = Planificador()  # Inicialización del planificador de procesos
        self.pcbs = []  # Lista para almacenar los PCBs de los procesos
        self.ejecutando = False  # Estado de la simulación (si está en ejecución o no)

    # Método para cambiar la cantidad de memoria disponible
    def ingresoPorPantalla(self):
        dialog = customtkinter.CTkInputDialog(text="Ingrese un número:", title="Nueva Memoria")
        nueva_memoria = dialog.get_input()
        if nueva_memoria.isdigit():
            self.memoria.limite = int(nueva_memoria)
            self.textbox.insert("end", f"Memoria ajustada a {nueva_memoria} unidades\n")
            self.actualizar_interfaz()

    #Definimos las funciones para cambiar la interfaz
    def cambiarEscala(self, nuevaEscala: str):
        Nuevo = int(nuevaEscala.replace("%", "")) / 100
        customtkinter.set_widget_scaling(Nuevo)
        
    def cambiarApariencia(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        
    # Método para cambiar el algoritmo de planificación
    def cambiarAlgoritmo(self, algoritmo):
        self.planificador.algoritmo = algoritmo
        self.textbox.insert("end", f"Algoritmo de planificación cambiado a {algoritmo}\n")

    # Método para iniciar la ejecución de procesos
    def EjecutarProceso(self):
        if not self.ejecutando:
            self.ejecutando = True
            try:
                cantidad_hilos = int(self.entryHilos.get())
                if cantidad_hilos < 1:
                    cantidad_hilos = 1
            except ValueError:
                cantidad_hilos = 1
            self.textbox.insert("end", f"Ejecutando con {cantidad_hilos} hilos\n")
            self.crear_procesos(10) # Creamos 10 procesos
            self.actualizar_interfaz()

            for _ in range(cantidad_hilos):
                threading.Thread(target=self.ejecutar_hilo, daemon=True).start()

    def crear_procesos(self, cantidad):
        global siguientePid
        for _ in range(cantidad):
            pcb = PCB(siguientePid, random.randint(10, 100), random.randint(1, 10))
            memoria_asignada = self.memoria.asignar_memoria(pcb)
            self.planificador.agregar_proceso(pcb, memoria_asignada)
            self.textbox.insert("end", f"Se creó el proceso {pcb.pid} con {pcb.memoria_requerida}. Estado: {pcb.estado}. Tiempo: {pcb.tiempo_limite}\n")
            siguientePid += 1

    def ejecutar_hilo(self): # Función ejecutada por cada hilo
        if self.ejecutando == False:
            return

        pcb = self.planificador.obtener_proceso()
        if pcb == None:
            self.ejecutando = False
            self.textbox.insert("end", "No se encuentran más procesos en la cola. Simulación detenida.\n")
            return
        
        self.textbox.insert("end", f"Ejecutando proceso {pcb.pid} ({pcb.estado})\n")

        self.ejecutar_proceso(pcb)
        self.actualizar_interfaz()

        self.ejecutar_hilo()

    def ejecutar_proceso(self, pcb):
        time.sleep(1)
        pcb.tiempo_ejecucion += 1

        if pcb.tiempo_ejecucion >= pcb.tiempo_limite: # Proceso terminado
            self.memoria.liberar_memoria(pcb)
            pcb.estado = "Terminado"

    # Método que simula la ejecución de procesos en base al algoritmo de planificación
    # def simulacion_procesos(self):
    #     pid = 0
    #     while self.ejecutando:
    #         memoria_requerida = random.randint(10, 100)
    #         pcb = PCB(pid, memoria_requerida)
    #         self.planificador.agregar_proceso(pcb)

    #         proceso_ejecutar = self.planificador.obtener_siguiente_proceso()
    #         if proceso_ejecutar and self.memoria.asignar_memoria(proceso_ejecutar):
    #             proceso_ejecutar.estado = "Ejecutando"
    #             self.textbox.insert("end", f"Proceso {proceso_ejecutar.pid} ejecutando con {proceso_ejecutar.memoria_requerida} unidades de memoria\n")
    #             self.actualizar_interfaz()  # Actualiza y muestra el estado de la memoria
    #             time.sleep(2)  # Simula el tiempo de ejecución
    #             proceso_ejecutar.contador_programa += 1
    #             proceso_ejecutar.estado = "Terminado"
    #             proceso_ejecutar.tiempo_termino = time.time()
    #             self.memoria.liberar_memoria(proceso_ejecutar)
    #             self.textbox.insert("end", f"Proceso {proceso_ejecutar.pid} terminado y memoria liberada\n")
    #             self.actualizar_interfaz()  # Actualiza y muestra el estado de la memoria
    #         else:
    #             proceso_ejecutar.estado = "Bloqueado"
    #             self.textbox.insert("end", f"Proceso {proceso_ejecutar.pid} bloqueado por falta de memoria\n")
    #             self.actualizar_interfaz()  # Actualiza y muestra el estado de la memoria

    #         pid += 1
    #         time.sleep(1)

    # Método para detener la simulación
    def parar_simulacion(self):
        self.ejecutando = False
        self.textbox.insert("end", "Simulación detenida\n")

    # Método para actualizar la interfaz gráfica con el estado actual de la memoria
    def actualizar_interfaz(self):
        self.barraProgreso.set(self.memoria.usada / self.memoria.limite)
        self.textbox.insert("end", f"Memoria usada: {self.memoria.usada}/{self.memoria.limite}\n")

siguientePid = 0 # Global
app = App()

# Punto de entrada de la aplicación
if __name__ == "__main__":
    app.mainloop()
