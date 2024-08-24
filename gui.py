class Nodo():
    def __init__(self):
        self.siguiente = None

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