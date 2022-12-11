import numpy as np
from PIL import ImageTk, Image
import librosa
import os
#imports para la gui
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
window = tk.Tk()

from loadModel import load_model

#Pantalla principal
def pantalla_principal():
    global pantalla
    pantalla = tk.Tk()
    pantalla.geometry("300x250")
    pantalla.title("APP MUSICAL")
    Label(text="APP MUSICAL", bg="green",width="300",height="2",font=("Verdana",13)).pack()

    Label(text="").pack()
    Button(text="Iniciar sesion",height="2",width="30",command=login).pack()
    Label(text="").pack()
    Button(text="Registro",height="2",width="30",command=Registro).pack()
    pantalla.mainloop()
def login():
    global pantalla2
    global verificacion_usuario
    global verificacion_contra
    global usuario_entrada2 
    



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