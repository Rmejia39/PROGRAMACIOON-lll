from typing import self
from tkinter import  Tk, Button, Entry, Label, ttk, PhotoImage
from tkinter import  StringVar,END,HORIZONTAL,Frame,Toplevel
import time
import numpy as np
import conexion
import mysql.connector 
from PIL import ImageTk, Image
import librosa
import os
#imports para la gui
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename


from loadModel import load_model


class GUI:
    def app():
        window = tk.Tk()
        #Cargar el modelo
        model = load_model()


        #Propiedades de la Ventana
        
        window.title("APP MUSICAL")
        window.geometry('400x400')
        #window.iconbitmap("./clef.ico")
        window.maxsize(width=400,height=400)
        frame1 = tk.Frame(window, bg='#67B93E')

        frame1.pack(fill='both', expand='yes')
        #-------------------------#

        #
        #lbl1 = tk.Label(frame1, image=photo)
        #lbl1.photo = photo
        #lbl1.pack()
        bgframe="snow"
        frame2 = tk.Frame(frame1, bg=bgframe)
        frame2.place(relx=0.017, rely=0.022, relheight=0.95, relwidth=0.96)

        #Widgets
        #img = ImageTk.PhotoImage(file='UIS-logo2.png')
        #imagenUis = tk.Label(frame2, image=img)
        #imagenUis.place(x = 53, y = 5)

        lbl0 = tk.Label(frame1, text="Bienvenido",
                        bg=bgframe,
                        fg='Black',
                        font=("Century Gothic",40))
        lbl0.place(x=58,y=150)

        lbl1 = tk.Label(frame1, text=" 2022",
                        bg=bgframe,
                        fg='Black',
                        font=("Helvetica",8))
        lbl1.place(x=161,y=365)

        progressbar = ttk.Progressbar(frame1)
        progressbar.place(x=95, y=240, width=200)    
        def choose_file():
            filename = askopenfilename()
            return filename
            
        def identificar_genero():
            audiopath = choose_file()
            
            if(audiopath != ""):
                base=os.path.basename(audiopath)
                songname = os.path.splitext(base)[0]
                try:
                    #Se tiene el path del archivo, ahora se procede a realizar la regresión
                    progressbar.step(9.99)  
                    #Se empieza por cargar el achivo con librosa
                    y , sr = librosa.load(audiopath, mono=True, duration=50)
                    progressbar.step(9.99)  
                    #se procede a extraer las características
                    features = np.zeros(shape=(1,26))
                    features = np.ndarray.astype(features, float)
                    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
                    features[0][0] = np.mean(chroma_stft)
                    rmse = librosa.feature.rms(y=y)
                    features[0][1] = np.mean(rmse)
                    progressbar.step(9.99)  
                    spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
                    features[0][2] = np.mean(spec_cent)
                    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
                    features[0][3] = np.mean(spec_bw)
                    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
                    progressbar.step(9.99)  
                    features[0][4] = np.mean(rolloff)
                    zcr = librosa.feature.zero_crossing_rate(y)
                    features[0][5] = np.mean(zcr)
                    mfcc = librosa.feature.mfcc(y=y, sr=sr)
                    i = 5
                    progressbar.step(9.99)  
                    for e in mfcc:
                        i += 1
                        features[0][i] = np.mean(e)
                    features = np.array(features)
                    progressbar.step(9.99)  
                    #se cargan las medias y desviaciones estándar
                    medias = np.load('data\medias.npy')
                    desvest = np.load('data\desvest.npy')
                    #Se procede a estandarizar las caraceterísticas con respecto a las medias y desviaciones estándar
                    progressbar.step(9.99)  
                    for idx in range(features.shape[1]):
                        features[0][idx] = (features[0][idx]-medias[idx])/desvest[idx]
                    progressbar.step(9.99)  
                    #Se procede a realizar la regresión con el modelo
                    progressbar.step(9.99)  
                    prediction = model.predict_classes(features)
                    progressbar.step(9.99)  
                    #ahora se procede a mostrar al usuario la predicción del genero musical del audio que ingresó
                    generos = []
                    generos.append("Blues")
                    generos.append("Clásica")
                    generos.append("Country")
                    generos.append("Disco")
                    generos.append("Hiphop")
                    generos.append("Jazz")
                    generos.append("Metal")
                    generos.append("Pop")
                    generos.append("Reggae")
                    generos.append("Rock")
                    genero = generos[prediction[0]]
                    text = "La canción:\n"  + songname + "\nEs del género: " + genero + "."
                    messagebox.showinfo("¡Éxito!", text)
                    progressbar.step(0.2)
                except:
                    messagebox.showinfo("Error", "El archivo seleccionado:\n" + base + "\nEs inválido o no ha podido ser leído")
                    progressbar.stop()
            else:
                messagebox.showinfo("Error", "Ningún archivo seleccionado")


        btn0 = tk.Button(frame1, text="Identificar Género Canción",
                        bg='ghost white',
                        fg='gray11',
                        font=("Helvetica",10),
                        command= identificar_genero)
        btn0.place(x=113,y=280)

        def click_credits():         
            tk.messagebox.showinfo("Créditos","Rigoberto: \n\nPROGRAMACIÓN III\n \t     -RIGOBERTO MEJÍA\n \t     -DANIELA ESPERANZA \n\n          Universidad Gerardo Barrios\n\t\t    2022")
            
            
        btn1 = tk.Button(frame1, text="Créditos",
                        bg='ghost white',
                        fg='gray11',
                        font=("Helvetica",10),
                        command=click_credits)
        btn1.place(x=161,y=330)


        window.mainloop()


class Login(Frame):


        def __init__(self, master, *args):
        super().__init__( master,*args)
        self.user_marcar = "Ingrese su correo"
        self.contra_marcar = "Ingrese su contraseña"
        self.fila1  = ''
        self.fila2 = ''
        self.datos = conexion.Registro_datos()
        self.widgets()
def entry_out(self, event, event_text):
        if event['fg'] == 'black' and len(event.get()) ==0:
            event.delete(0, END)
            event['fg'] = 'grey'
            event.insert(0, event_text)
        if self.entry2.get() != 'Ingrese su contraseña':
            self.entry2['show'] =""
        if self.entry2.get() != 'Ingrese su correo':
            self.entry2['show'] ="*"
def entry_in(self, event):		
    if  event['fg'] == 'grey':
        event['fg'] = 'black'
    event.delate(0,END)
           	
if self.entry2.get() != 'Ingrese su contraseña':
   self.entry2['show'] = "*"

if self.entry2.get() == 'Ingrese su contraseña':
   self.entry2['show'] = ""

def salir(self):
        self.master.destroy()
        self.master.quit()

def acceder_ventana_dos(self):
        for i in  range(101):
            self.barra['value'] +=1
            self.master.update()
            time.sleep(0.02)

        self.master.withdraw()
        self.ventana_dos = Toplevel()
        self.ventana_dos.title('Segunda Ventana')
        self.ventana_dos.geometry('500x500+400+80')
        self.ventana_dos.protocol("WM_DELETE_WINDOW", self.salir)
        self.ventana_dos.config(bg= 'white')
        self.ventana_dos.state('zoomed')

        Label(self.ventana_dos, text='VENTANA DOS', font='Arial 40', bg= 'white').pack(expand=True)
        Button(self.ventana_dos, text='Salir', font='Arial 10', bg= 'red', command= self.salir).pack(expand=True)

def verificacion_users(self):
        self.indica1['text'] = ''
        self.indica2['text'] = ''		
        users_entry = self.entry1.get()
        password_entry = self.entry2.get()

        if users_entry!= self.user_marcar or self.contra_marcar != password_entry:
            users_entry = str("'" + users_entry + "'")
            password_entry = str("'" + password_entry + "'")

            dato1 = self.datos.busca_users(users_entry)
            dato2 = self.datos.busca_password(password_entry)

            self.fila1 = dato1
            self.fila2 = dato2 

            if self.fila1 == self.fila2:	
                if dato1 == [] and dato2 ==[]:
                    self.indica2['text'] = 'Contraseña incorrecta'
                    self.indica1['text'] = 'Usuario incorrecto'
                else:

                    if dato1 ==[]:
                        self.indica1['text'] = 'Usuario incorrecto'
                    else:
                        dato1 = dato1[0][1]

                    if dato2 ==[]:
                        self.indica2['text'] = 'Contraseña incorrecta'
                    else:
                        dato2 = dato2[0][2]

                    if dato1 != [] and dato2 != []:
                        self.mainGUI.app()
            else:
                self.indica1['text'] = 'Usuario incorrecto'
                self.indica2['text'] = 'Contraseña incorrecta'

def widgets(self):
        self.logo = PhotoImage(file ='logo.png')
        Label(self.master, image= self.logo, bg='DarkOrchid1',height=150, width=150).pack()
        Label(self.master, text= 'Usuario', bg='DarkOrchid1', fg= 'black', font= ('Lucida Sans', 16, 'bold')).pack(pady=5)
        self.entry1 = Entry(self.master, font=('Comic Sans MS', 12),justify = 'center', fg='grey',highlightbackground = "#E65561", 
			highlightcolor= "green2", highlightthickness=5)
        self.entry1.insert(0, self.user_marcar)
        self.entry1.bind("<FocusIn>", lambda args: self.entry_in(self.entry1))
        self.entry1.bind("<FocusOut>", lambda args: self.entry_out(self.entry1, self.user_marcar))
        self.entry1.pack(pady=4)   

        self.indica1 = Label(self.master, bg='DarkOrchid1', fg= 'black', font= ('Arial', 8, 'bold'))
        self.indica1.pack(pady=2)                             

		# contraseña y entry
        Label(self.master, text= 'Contraseña', bg='DarkOrchid1', fg= 'black', font= ('Lucida Sans', 16, 'bold')).pack(pady=5)
        self.entry2 = Entry(self.master,font=('Comic Sans MS', 12),justify = 'center',  fg='grey',highlightbackground = "#E65561", 
			highlightcolor= "green2", highlightthickness=5)
        self.entry2.insert(0, self.contra_marcar)
        self.entry2.bind("<FocusIn>", lambda args: self.entry_in(self.entry2))
        self.entry2.bind("<FocusOut>", lambda args: self.entry_out(self.entry2, self.contra_marcar))
        self.entry2.pack(pady=4)
        self.indica2 = Label(self.master, bg='DarkOrchid1', fg= 'black', font= ('Arial', 8, 'bold'))
        self.indica2.pack(pady=2)
        Button(self.master, text= 'Iniciar Sesion',  command = self.verificacion_users,activebackground='magenta', bg='#D64E40', font=('Arial', 12,'bold')).pack(pady=10)
        estilo = ttk.Style()
        estilo.theme_use('clam')
        estilo.configure("TProgressbar", foreground='red', background='black',troughcolor='DarkOrchid1',
																bordercolor='#970BD9',lightcolor='#970BD9', darkcolor='black')
        self.barra = ttk.Progressbar(self.master, orient= HORIZONTAL, length=200, mode='determinate', maximum=100, style="TProgressbar")
        self.barra.pack()
        Button(self.master, text= 'Salir', bg='DarkOrchid1',activebackground='DarkOrchid1', bd=0, fg = 'black', font=('Lucida Sans', 15,'italic'),command= self.salir).pack(pady=10)

if __name__ == "__main__":
	ventana = Tk()
	ventana.config(bg='DarkOrchid1')
	ventana.geometry('350x500+500+50')
	ventana.overrideredirect(1)
	ventana.resizable(0,0)
	app = Login(ventana)
	app.mainloop()

