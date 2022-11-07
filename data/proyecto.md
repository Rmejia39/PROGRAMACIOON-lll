<p align="center"><img src="" width="1500" heigth="500"></p>


# Reproductor de Música 
**Integrantes**
-    KARLA DANIELA TORRES ESPERANZA
-    RIGOBERTO ALEXANDER MEJÍA SORTO




**UNIVERSIDAD GERARDO BARRIOS** </br>
**INGENIERÍA EN SISTEMAS Y REDES INFORMÁTICAS**</br>
**2021**</br>
<p align="center"><img src="" width="342" heigth="166"></p>


# Introduccion
El planteamiento del proyecto consiste en crear un reproductor de canciones, por medio de caracteristicas similares preprocesadas en los espectrogramas de las canciones.

Para esto se Utilizará como entrenamiento un Dataset de canciones 1000 canciones en formato au con su respectivo género, 10 en total.

Para entrenar un modelo, primero se necesita obtener de cada una de esas canciones sus caracteristicas más relevantes para el problema de clasificación, por lo que se utilizó la Librería *LIBROSE* para explorar los espectrogramas y sacar así las siguentes características:

<ul>
   <li> Coeficientes ceptrales en la frecuencia de mel (MFCC)(20)
   <li> Spectral Centroid,
   <li> Zero Crossing Rate
   <li> Chroma Frequencies
   <li> Spectral Roll-off.
</ul>




# Objetivo
-Clasificar canciones por su respectivo género músical.<br> 
-Aprender acerca de los Modelos de DeepLearning, más especificamente los que ofrece la Librería Keras usando TensorFlow como backend.

# Referencias
Los datos del dataset y otros datos fueron recolectados por usuarios que también tienen como propósito el entrenamiento de señales de audio.