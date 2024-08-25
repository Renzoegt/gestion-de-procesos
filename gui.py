import customtkinter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("Hades.json") 

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configuramos la ventana
        self.title("Tp Sistemas: Gestión de Procesos")
        self.geometry(f"{900}x{580}")

        # configuramos el layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # creamos un frame lateral para widgets
        self.frameLateral = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.frameLateral.grid(row=0, column=0, rowspan=6, sticky="nsew")
        self.frameLateral.grid_rowconfigure(4, weight=1)
        
        #Creamos un texto que le de titulo al frame lateral
        self.logo = customtkinter.CTkLabel(self.frameLateral, text="Gestión de Memoria", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        #Creamos un botón para iniciar el proceso
        self.botonProceso = customtkinter.CTkButton(self.frameLateral, text="Ejecutar un proceso", command=self.EjecutarProceso)
        self.botonProceso.grid(row=1, column=0, padx=20, pady=10)
        
        #Creamos un boton que permita interacción con el usuario para poder ingresar un cambio en la memoria predefinida
        self.cambiarMemoria = customtkinter.CTkButton(self.frameLateral, text="Cambiar Cantidad de Memoria", command=self.ingresoPorPantalla)
        self.cambiarMemoria.grid(row=2, column=0, padx=20, pady=10)
        #Creamos un botón para parar la simulación
        self.pararSimulacion = customtkinter.CTkButton(self.frameLateral, text="Parar Simulación", command=self.pararSimulacion)
        self.pararSimulacion.grid(row=3, column=0, padx=20, pady=10)
        
        #creamos un título y un menú para cambiar la apariencia de la pestaña
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
    
        # creamos espacios para texto
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(2, 0), pady=(2, 0), sticky="nsew")
        self.textbox.insert("0.0", "CTkTextbox\n" )
        self.textbox.insert("2.0", "CTkTextbox\n" )
        self.textbox.insert("4.0", "CTkTextbox\n" )
    
    
    #función para el ingreso por pantalla de la app
    def ingresoPorPantalla(self):
        dialog = customtkinter.CTkInputDialog(text="Ingrese un número:", title="Nueva Memoria")
        print("Ingreso:", dialog.get_input())

    def cambiarApariencia(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def cambiarMood(self, nuevaApariencia: str):
        customtkinter.set_default_color_theme(nuevaApariencia)
    
    def cambiarEscala(self, nuevaEscala: str):
        Nuevo = int(nuevaEscala.replace("%", "")) / 100
        customtkinter.set_widget_scaling(Nuevo)

    #Aca están las funciones a las que llaman los botones
    def EjecutarProceso(self):
        print("apretaste un boton")
    
    def pararSimulacion(self):
        print("prueba botón")

        

    

if __name__ == "__main__":
    app = App()
    app.mainloop()