from customtkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog, ttk,messagebox
from pytube import YouTube, Playlist
import urllib.request
from io import BytesIO

set_appearance_mode("dark")
set_default_color_theme("dark-blue")

class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("Ace")
        self.geometry(f"{900}x{650}")
        self.resizable(False, False)

        self.imagen = Image.open(r"C:\Users\nad__\Documents\Proyectos Personales\Ace Downloader\imagenes\logo-youtube.png")
        self.imagen = self.imagen.resize((self.imagen.width // 2, self.imagen.height // 2))
        self.imagen_tk = ImageTk.PhotoImage(self.imagen)

        self.label = CTkLabel(self, image=self.imagen_tk, text=None)
        self.label.place(x=50, y=20)

        self.titulo = CTkLabel(self, text="Ace Downloader")
        font_title = ("Arial", 40)
        self.titulo.configure(font=font_title)
        self.titulo.place(x=400, y=100)

        # Boton y entrada de ubicacion
        font_sub = ("Arial", 16)
        self.lb_ubi = CTkLabel(self, text="Ubicacion:")
        self.lb_ubi.configure(font=font_sub)
        self.lb_ubi.place(x=220, y=240)

        self.et_ubi = CTkEntry(self, placeholder_text="Ubicacion donde se guardaran los archivos", width=400)
        self.et_ubi.place(x=300, y=240)

        # Corrección: abrir_ubicacion debe estar en el nivel de la clase
        self.btnUbicacion = CTkButton(self, text="Ubicacion", height=50, command=self.abrir_ubicacion)
        self.btnUbicacion.place(x=50, y=230)

        # boton y entrada de url
        self.lb_url = CTkLabel(self, text="URL:")
        self.lb_url.configure(font=font_sub)
        self.lb_url.place(x=255, y=310)

        self.et_url = CTkEntry(self, placeholder_text="Ingresa aqui la url del video", width=400)
        self.et_url.place(x=300, y=310)

        self.btnDescargar = CTkButton(self, text="Descargar", height=50,command=self.descargar)
        self.btnDescargar.place(x=50, y=300)
        
        self.btnPlaylist = CTkButton(self, text="Descargar\nPlaylist", height=50, command=self.descargar_playlist)
        self.btnPlaylist.place(x=730, y=300)
        
        # Combobox para elegir formato y calidad
        self.cbox_calidad_var = StringVar(value="Buena calidad")
        self.cbox_calidad = CTkComboBox(self, height=20, values=["Maxima calidad", "Alta calidad", "Buena calidad", "Baja calidad", "Solo audio", "Solo Video"], command=self.calidad_elegida, variable=self.cbox_calidad_var)
        self.cbox_calidad.set("Buena calidad")
        self.cbox_calidad.place(x=730, y=250)
        
                
        # Estilo de la tabla de operaciones
        self.style_tabla = ttk.Style()
        self.style_tabla.configure("Custom.Treeview", background="#1a1a1a", foreground="white", rowheigth=10)
        
        # Tabla de operaciones
        self.tabla = ttk.Treeview(self, style="Custom.Treeview")
        self.tabla["columns"] = ("Nombre","url","estado")
        self.tabla.heading("#0",text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("url", text="url")
        self.tabla.heading("estado", text="estado")
            # Ajuste del tamaño de la tabla
        self.tabla.column("#0",width=35)
        self.tabla.column("Nombre",width=275)
        self.tabla.column("url",width=420)
        self.tabla.column("estado",width=100)
        self.tabla.place(x=50,y=380)
        
        self.calidad = 0
        self.cont = 1
        
    # FUNCIONES
    
    def calidad_elegida(self,choice):
        print(self.cbox_calidad_var.get())
    
    def abrir_ubicacion(self):
        ubicacion = filedialog.askdirectory()
        self.et_ubi.delete(0, "end")
        self.et_ubi.insert(0, ubicacion)
    
    def descargar(self):
        try:
            link = self.et_url.get()
            yt = YouTube(link)
            video = yt.streams.get_by_itag(22)
            salida = self.et_ubi.get()
            video.download(output_path=salida)
            self.tabla.insert("", "end",text=self.cont, values=(yt.title, link,"terminado"))
            self.cont += 1
        except:
            messagebox.showerror("Error","Link Invalido")
        
    def descargar_playlist(self):
        try:
            link = self.et_url.get()
            pl = Playlist(link)
            for video in pl.videos:
                self.tabla.insert("", "end",text=self.cont, values=(video.title, video.watch_url, "terminado"))
                self.cont += 1
        except: 
            messagebox.showerror("Error","Link Invalido")
        

if __name__ == "__main__":
    app = App()
    app.mainloop()
