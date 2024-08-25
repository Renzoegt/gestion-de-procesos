import customtkinter
import threading
import time

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("Hades.json")

class PCB():
    def __init__(self, pid, prioridad, memoria, tiempoLimite):
        self.pid = pid
        self.estado = 0  # 0: Listo, 1: En ejecución, 2: Bloqueado, 3: Terminado
        self.prioridad = prioridad
        self.memoria = memoria
        self.tiempoLimite = tiempoLimite
        self.tiempoEjecucion = 0  # Tiempo en segundos

class GestorMemoria():
    def __init__(self, memoria_total=500000):
        self.memoriaTotal = memoria_total
        self.memoriaDisponible = self.memoriaTotal

    def asignarMemoria(self, pcb:PCB):
        if pcb.memoria > self.memoriaDisponible:
            return False
        self.memoriaDisponible -= pcb.memoria
        return True
    
    def liberarMemoria(self, pcb:PCB):
        self.memoriaDisponible += pcb.memoria

class GestorProcesos():
    def __init__(self):
        self.espera = []  # Procesos en espera
        self.ejecucion = []  # Procesos en ejecución

    def ponerEnEspera(self, pcb:PCB):
        pcb.estado = 0
        if pcb in self.ejecucion:
            self.ejecucion.remove(pcb)
        self.espera.append(pcb)

    def ponerEnEjecucion(self, pcb:PCB):
        pcb.estado = 1
        if pcb in self.espera:
            self.espera.remove(pcb)
        self.ejecucion.append(pcb)

    def detenerProceso(self, pcb:PCB):
        pcb.estado = 3
        self.ejecucion.remove(pcb)

    def ejecutarCiclo(self, memoria:GestorMemoria):
        i = 0
        while i < len(self.espera):  # Agregar procesos a ejecución si hay suficiente memoria
            pcb = self.espera[i]
            if memoria.asignarMemoria(pcb):
                self.ponerEnEjecucion(pcb)
            else:
                i += 1

        i = 0
        while i < len(self.ejecucion):  # Simulamos la ejecución
            pcb = self.ejecucion[i]
            pcb.tiempoEjecucion += 1
            if pcb.tiempoEjecucion >= pcb.tiempoLimite:
                self.detenerProceso(pcb)
                memoria.liberarMemoria(pcb)
            else:
                i += 1

class SistemaOperativo():
    def __init__(self):
        self.procesos = GestorProcesos()
        self.memoria = GestorMemoria()
        self.proximoPid = 1  # PID único para cada proceso

    def ejecutarCiclo(self):
        self.procesos.ejecutarCiclo(self.memoria)

    def crearProceso(self, prioridad, memoria, tiempoLimite):
        pcb = PCB(self.proximoPid, prioridad, memoria, tiempoLimite)
        self.proximoPid += 1
        self.procesos.ponerEnEspera(pcb)

    def detenerProceso(self, pid):
        for pcb in self.procesos.ejecucion:
            if pcb.pid == pid:
                self.procesos.detenerProceso(pcb)
                return

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Tp Sistemas: Gestión de Procesos")
        self.geometry(f"{900}x{580}")

        self.sistema = SistemaOperativo()

        # Configuración del layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Frame lateral para widgets
        self.frameLateral = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.frameLateral.grid(row=0, column=0, rowspan=6, sticky="nsew")
        self.frameLateral.grid_rowconfigure(4, weight=1)
        
        self.logo = customtkinter.CTkLabel(self.frameLateral, text="Gestión de Memoria", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.botonProceso = customtkinter.CTkButton(self.frameLateral, text="Ejecutar un proceso", command=self.crear_proceso)
        self.botonProceso.grid(row=1, column=0, padx=20, pady=10)
        
        self.cambiarMemoria = customtkinter.CTkButton(self.frameLateral, text="Cambiar Cantidad de Memoria", command=self.ingreso_por_pantalla)
        self.cambiarMemoria.grid(row=2, column=0, padx=20, pady=10)

        self.pararSimulacion = customtkinter.CTkButton(self.frameLateral, text="Parar Simulación", command=self.parar_simulacion)
        self.pararSimulacion.grid(row=3, column=0, padx=20, pady=10)
        
        self.nombreApariencia = customtkinter.CTkLabel(self.frameLateral, text="Apariencia:", anchor="w")
        self.nombreApariencia.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.menuDeApariencia = customtkinter.CTkOptionMenu(self.frameLateral, values=["Light", "Dark"],
                                                            command=self.cambiarApariencia)
        self.menuDeApariencia.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        self.etiquetaDeEscala = customtkinter.CTkLabel(self.frameLateral, text="Escala de la Interfaz:", anchor="w")
        self.etiquetaDeEscala.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.menuDeescala = customtkinter.CTkOptionMenu(self.frameLateral, values=["80%", "90%", "100%", "110%", "120%"],
                                                        command=self.cambiarEscala)
        self.menuDeescala.grid(row=9, column=0, padx=20, pady=(10, 20))

        self.frameDeBarraDeProgreso = customtkinter.CTkFrame(self, fg_color="transparent")
        self.frameDeBarraDeProgreso.grid(row=6, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.frameDeBarraDeProgreso.grid_columnconfigure(0, weight=1)
        self.frameDeBarraDeProgreso.grid_rowconfigure(4, weight=1)
        self.barraProgreso = customtkinter.CTkProgressBar(self.frameDeBarraDeProgreso)
        self.barraProgreso.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
    
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(2, 0), pady=(2, 0), sticky="nsew")

        # Hilo para ejecutar ciclos del sistema operativo
        self.ciclo_activo = False
        self.hilo_ciclo = threading.Thread(target=self.ejecutar_ciclo_sistema)
    
    def crear_proceso(self):
        # Ejemplo: Crear un proceso con prioridad 1, memoria de 2000 y tiempo límite de 10 segundos
        self.sistema.crearProceso(prioridad=1, memoria=2000, tiempoLimite=10)
        self.textbox.insert("end", "Proceso creado\n")
    
    def ingreso_por_pantalla(self):
        dialog = customtkinter.CTkInputDialog(text="Ingrese la memoria total:", title="Configurar Memoria")
        memoria_nueva = int(dialog.get_input())
        self.sistema.memoria = GestorMemoria(memoria_nueva)
        self.textbox.insert("end", f"Memoria total configurada a {memoria_nueva}\n")

    def cambiarApariencia(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def cambiarEscala(self, nuevaEscala: str):
        Nuevo = int(nuevaEscala.replace("%", "")) / 100
        customtkinter.set_widget_scaling(Nuevo)

    def ejecutar_ciclo_sistema(self):
        self.ciclo_activo = True
        while self.ciclo_activo:
            self.sistema.ejecutarCiclo()
            time.sleep(1)  # Espera de 1 segundo por ciclo

    def parar_simulacion(self):
        self.ciclo_activo = False
        self.textbox.insert("end", "Simulación detenida\n")

if __name__ == "__main__":
    app = App()
    app.hilo_ciclo.start()
    app.mainloop()
