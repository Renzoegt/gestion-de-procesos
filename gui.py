class PCB():
    def __init__(self, pid, prioridad, memoria, tiempoLimite):
        self.pid = pid
        self.estado = 0 # 0: Listo, 1: En ejecución, 2: Bloqueado, 3: Terminado
        self.prioridad = prioridad
        self.memoria = memoria
        self.tiempoLimite = tiempoLimite
        self.tiempoEjecucion = 0 # Tiempo en segundos

class Nodo():
    def __init__(self, dato:PCB):
        self.siguiente = None
        self.dato = dato

class Cola():
    def __init__(self):
        self.primerNodo = None
        self.ultimoNodo = None
        self.cantNodos = 0

    def encolar(self, nodo:Nodo):
        nodo.siguiente = None # Nos aseguramos de que el puntero al siguiente sea None porque será el ultimo nodo

        if self.primerNodo is None:
            self.primerNodo = nodo # Establecemos el primer nodo
        if self.ultimoNodo is not None:
            self.ultimoNodo.siguiente = nodo # El siguiente del último nodo será el nuevo nodo

        self.ultimoNodo = nodo # Establecemos el último nodo agregado a la cola
        self.cantNodos += 1

    def desencolar(self):
        if self.primerNodo == None:
            return None
        
        nodoEliminado = self.primerNodo
        self.primerNodo = self.primerNodo.siguiente
        self.cantNodos -= 1

        if self.cantNodos == 0:
            self.ultimoNodo = None

        nodoEliminado.siguiente = None # Reseteamos el puntero al siguiente nodo
        return nodoEliminado
    
    def encontrarNodoEnCaja(self, id:int): # Buscamos en los nodos de la caja y si el id del carrito coincide con el parámetro retornamos el nodo
        if self.primerNodo == None:
            return None

        actual = self.primerNodo
        while actual != None:
            if actual.dato.id == id:
                return actual

            actual = actual.siguiente

        return None

class GestorMemoria():
    def __init__(self):
        self.memoriaTotal = 500000
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
        self.contexto = None
        self.espera = list() # Procesos recien creados y esperando que se libere memoria
        self.ejecucion = list() # Procesos ejecutandose concurrentemente

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
        self.ejecucion.remove(pcb) # Removemos de la lista actual

    def ejecutarCiclo(self, memoria:GestorMemoria):
        if self.contexto == None:
            return
        
        i = 0
        while i < self.espera.count: # Agregar los procesos a ejecución si hay suficiente memoria
            pcb:PCB = self.ejecucion[i]
            
            if memoria.asignarMemoria(pcb) == True:
                self.ponerEnEjecucion(pcb)
            else: # Incrementamos el índice sólo si no se removieron elementos de la lista
                i += 1

        i = 0
        while i < self.ejecucion.count: # Simulamos la ejecución de todos los procesos en ejecución y terminamos los procesos según su tiempo límite
            pcb:PCB = self.ejecucion[i]
            pcb.tiempoEjecucion += 1
            
            if pcb.tiempoEjecucion >= pcb.tiempoLimite: # Liberamos la memoria y detenemos el proceso
                self.detenerProceso(pcb)
                memoria.liberarMemoria(pcb)
            else:
                i += 1
    
    def detenerProceso(self, idProceso):
        for pcb in self.ejecucion:
            if pcb.pid == idProceso:
                self.detenerProceso(pcb)
                return
            
        print("El PID solicitado no se encuentra en ejecución.")


class SistemaOperativo():
    def __init__(self):
        self.procesos = GestorProcesos()
        self.memoria = GestorMemoria()
    
    def ejecutarCiclo(self): # Llamar esta función cada segundo. Aca se ejecutan los procesos.
        self.procesos.ejecutarCiclo(self.memoria)
        return

    def ejecutarProceso(self):
        return 0
    
    def detenerProceso(self, idProceso):
        self.procesos.detenerProceso(idProceso)

# El Sistem Operativo debería iniciar cuando un usuario presione un boton de encendido
# Esa acción iniciaría el loop infinito que representa la ejecución del proceso principal del sistema

cerrar = False
while (cerrar == False): # (Temporal) El usuario debería presionar un botón de cerrar o cerrar la ventana para que termine de ejecutarse el programa
    print("...")
    
    if input() != None: # (Temporal) Cerrar programa
        break