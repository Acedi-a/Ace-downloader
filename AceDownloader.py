from customtkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog, ttk,messagebox
from pytube import YouTube, Playlist
import os
import threading

set_appearance_mode("dark")
set_default_color_theme("dark-blue")

class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("Ace Downloader v1.2")
        self.geometry(f"{900}x{650}")
        self.resizable(False, False)
        self.iconbitmap(r"C:\Users\nad__\Documents\Proyectos Personales\Ace Downloader\imagenes\icono_logo.ico")

        self.imagen = Image.open(r"C:\Users\nad__\Documents\Proyectos Personales\Ace Downloader\imagenes\logo-youtube.png")
        self.imagen = self.imagen.resize((self.imagen.width // 3, self.imagen.height // 3))
        self.imagen_tk = ImageTk.PhotoImage(self.imagen)

        self.label = CTkLabel(self, image=self.imagen_tk, text=None)
        self.label.place(x=50, y=20)

        self.titulo = CTkLabel(self, text="Ace Downloader")
        font_title = ("Arial", 40)
        self.titulo.configure(font=font_title)
        self.titulo.place(x=400, y=70)

        # Boton y entrada de ubicacion
        font_sub = ("Arial", 16)
        self.lb_ubi = CTkLabel(self, text="Ubicacion:")
        self.lb_ubi.configure(font=font_sub)
        self.lb_ubi.place(x=220, y=170)

        self.et_ubi = CTkEntry(self, placeholder_text="Ubicacion donde se guardaran los archivos", width=400)
        self.et_ubi.place(x=300, y=170)

        # Boton de ubicacion de descarga
        self.btnUbicacion = CTkButton(self, text="Ubicacion", height=50, command=self.abrir_ubicacion)
        self.btnUbicacion.place(x=50, y=160)

        # boton y entrada de url
        self.lb_url = CTkLabel(self, text="URL:")
        self.lb_url.configure(font=font_sub)
        self.lb_url.place(x=255, y=240)

        self.et_url_var = StringVar()
        self.et_url = CTkEntry(self, placeholder_text="Ingresa aqui la url del video", width=400)
        self.et_url.bind("<KeyRelease>", self.verificar_palabra) 
        self.et_url.place(x=300, y=240)

        self.btnDescargar = CTkButton(self, text="Descargar", height=50,command=self.descargar)
        self.btnDescargar.place(x=50, y=230)
        
        self.btnPlaylist = CTkButton(self, text="Descargar\nPlaylist", height=50, command=self.descargar_playlist)
        self.btnPlaylist.place(x=730, y=230)
        
        # Combobox para elegir formato y calidad
        self.cbox_calidad_var = StringVar(value="Buena calidad")
        self.cbox_calidad = CTkComboBox(self, height=20, values=["Maxima calidad", "Alta calidad", "Buena calidad", "Baja calidad", "Solo audio", "Solo Video"], command=self.calidades, variable=self.cbox_calidad_var)
        self.cbox_calidad.set("Buena calidad")
        self.cbox_calidad.place(x=730, y=180)
        
        # Entrada para nombre
        self.et_nombre = CTkEntry(self, width=400, placeholder_text="Nombre del video, dejar en blanco si no se modifica")
        self.et_nombre.place(x=300,y=310)
        
        self.lb_nombre = CTkLabel(self, text="Nombre:")
        self.lb_nombre.configure(font=font_sub)
        self.lb_nombre.place(x=230, y=310)
        
        # Label para tamaño del video
        self.lb_peso = CTkLabel(self, text="")
        self.lb_peso.configure(font=font_sub)
        self.lb_peso.place(x=70,y=310)
        
        # Estilo de la tabla de operaciones
        self.style_tabla = ttk.Style()
        self.style_tabla.configure("Custom.Treeview", background="#1a1a1a", foreground="white", rowheigth=10)
        
        # Tabla de operaciones
        self.tabla = ttk.Treeview(self, style="Custom.Treeview")
        self.tabla["columns"] = ("Nombre","URL","Tamaño")
        self.tabla.heading("#0",text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("URL", text="URL")
        self.tabla.heading("Tamaño", text="Tamaño")
            # Ajuste del tamaño de la tabla
        self.tabla.column("#0",width=35)
        self.tabla.column("Nombre",width=275)
        self.tabla.column("URL",width=420)
        self.tabla.column("Tamaño",width=70)
        self.tabla.place(x=50,y=380)
        
        self.calidad = 0
        self.cont = 1
        self.c = 1
        self.tamsize = ""
        
        self.info_videos = {
            1:0,
            137:0,
            22:0,
            18:0,
            5:0,
            6:0,
        }
        
        
    # FUNCIONES -----------------------------------------------------------------------------
    def verificar_palabra(self, evento):
        print("Prueba")
        video_url = self.et_url.get()
        palabra_clave = "https://www.youtube.com/"

        if video_url.startswith(palabra_clave) and len(video_url) > 17:
            # Iniciar un nuevo hilo para realizar la operación en segundo plano
            threading.Thread(target=self.procesar_video, args=(video_url,)).start()
        elif video_url.startswith("https://www.youtube.com/playlist"): print("playlist")
        else : print("Palabra invallida")
            
    
    def procesar_video(self, link):
        try:
            yt = YouTube(link)
            video = yt.streams.get_highest_resolution()
            self.info_videos[1] = self.peso_video(video)
            video = yt.streams.get_by_itag(137)
            self.info_videos[137] = self.peso_video(video)
            video = yt.streams.get_by_itag(22)
            self.info_videos[22] = self.peso_video(video)
            video = yt.streams.get_by_itag(18)
            self.info_videos[18] = self.peso_video(video)
            video = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
            self.info_videos[5] = self.peso_video(video)
            video = yt.streams.filter(only_video=True).first()
            self.info_videos[6] = self.peso_video(video)
        except Exception as e:
            print(f"Error: {e}")
        print(self.info_videos)
        

    def peso_video(self,video):
        try:
            t = video
            tam = t.filesize / (1024 * 1024)
            #self.lb_peso.configure(text=f"Peso: {tam:.2f} MB")
            self.tamsize = f"{tam:.2f}"
            return self.tamsize
        except: 
            #self.lb_peso.configure(text=f"Peso: -- MB")
            self.tamsize = "--"
            return self.tamsize
    
    
    def calidades(self,choice):
        threading.Thread(target=self.calidad_elegida, args=(choice,)).start()

    def calidad_elegida(self,choice):
        cal = self.cbox_calidad_var.get()
        if(cal == "Maxima calidad"): self.calidad = 1
        elif (cal == "Alta calidad"): self.calidad = 137
        elif (cal == "Buena calidad"): self.calidad = 22
        elif (cal == "Baja calidad"): self.calidad = 18
        elif (cal == "Solo audio"): self.calidad = 5
        else : self.calidad = 6
        
        link = self.et_url.get()
        yt = YouTube(link)
        if(self.calidad == 1): video = yt.streams.get_highest_resolution()
        elif(self.calidad in [137, 22, 18]): video = yt.streams.get_by_itag(self.calidad)
        elif(self.calidad == 5): video = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        else: video = yt.streams.filter(only_video=True).first()
        print(f"Calidad: {self.calidad} - Peso: {self.info_videos[self.calidad]}")
        self.lb_peso.configure(text=f"{self.info_videos[self.calidad]} Mb")

    
    def abrir_ubicacion(self):
        ubicacion = filedialog.askdirectory()
        self.et_ubi.delete(0, "end")
        self.et_ubi.insert(0, ubicacion)
    
    def descargar(self):
        threading.Thread(target=self.descargar_video).start()

    def descargar_video(self):
        try:
            key = True
            salida = self.et_ubi.get()
            link = self.et_url.get()
            yt = YouTube(link)
            if self.et_nombre.get() != "":
                yt.title = self.et_nombre.get()

            """
            if os.path.exists(os.path.join(salida, self.et_nombre.get())):
                yt.title += f"({self.c})"
                self.c += 1
            """


            if self.calidad == 1:
                video = yt.streams.get_highest_resolution()
            elif self.calidad in [137, 22, 18]:
                video = yt.streams.get_by_itag(self.calidad)
            elif self.calidad == 5:
                video = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
                key = False
            else:
                video = yt.streams.filter(only_video=True).first()
            
            
            if key:
                video.download(output_path=salida)
            else:
                video.download(filename=f"{yt.title}.mp3", output_path=salida)
            
            sizetam = self.info_videos[self.calidad] + " Mb"

            self.tabla.insert("", "end", text=self.cont, values=(yt.title, link, sizetam))
            self.cont += 1
        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Link Invalido")

    def descargar_playlist(self):
        threading.Thread(target=self.descargar_playlist_thread).start()

    def descargar_playlist_thread(self):
        try:
            link = self.et_url.get()
            salida = self.et_ubi.get()
            pl = Playlist(link)
            key = True
            for video in pl.videos:
                try:
                    if self.calidad == 1:
                        vid = video.streams.get_highest_resolution()
                    elif self.calidad in [137, 22, 18]:
                        vid = video.streams.get_by_itag(self.calidad)
                    elif self.calidad == 5:
                        vid = video.streams.filter(only_audio=True).order_by('abr').desc().first()
                        key = False
                    else:
                        vid = video.streams.filter(only_video=True).first()
                    
                    if key: video.download(output_path=salida)
                    else: video.download(filename=f"{video.title}.mp3", output_path=salida)
            
                    vid.download(output_path=self.et_ubi.get())
                    t = vid
                    tam = t.filesize / (1024 * 1024)
                    peso = f"{tam:.2f}"
                    self.tabla.insert("", "end", text=self.cont, values=(video.title, video.watch_url, peso))
                    self.cont += 1
                except Exception as e: 
                    print(f"Error: {e}")
                    self.tabla.insert("", "end", text=self.cont, values=(e, video.watch_url, "Error"))
                    self.cont += 1
        except:
            messagebox.showerror("Error", "Link Invalido")


if __name__ == "__main__":
    app = App()
    app.mainloop()