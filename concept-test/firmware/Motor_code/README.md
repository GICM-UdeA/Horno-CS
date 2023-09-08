# Motor de paso
El motor paso a paso conocido también como motor de pasos es un dispositivo electromecánico que convierte una serie de impulsos eléctricos en desplazamientos angulares discretos [^1]. Para comprender a completitud el principio de funcionamiento de este puede referirse al video ["Mentalidad De Ingeniería/Motores paso a paso"][video]. 

El motor utilizado para el montaje de la prueba de concepto es el [NEMA 14][motor], y el controlador es el típico [A4988][driver]. En términos de programación podría optarse por usar la librería ["StepperDriver"][libreria], sin embargo, se ha optado por programar directamente el controlador para un mejor entendimiento del proceso de la configuración de velocidad, lo cual, se describe a continuación. 

### Control de velocidad con A4988
Este controlador, en su configuración de micro-steps "Full step", permite realizar 200 pasos de 1.8° para completar una revolución completa, y la ejecución de cada paso se controla enviando un pulso cuadrado al pin "STEP". La velocidad a la que el motor complete una vuelta va entonces a depender del tamaño del pulso que se le envía. 

Suponga que se requiere alcanzar una velocidad ($v$) en el motor de 1 rpm, es decir, una revolución en un minuto. Usando la siguiente relación es posible estimar cual debe ser el tamaño de pulso para lograrlo [^2]:

$$v = \frac{\Delta \theta}{360°} \times P_w \times 60, \quad(1)$$

donde, $\Delta \theta$ es el tamaño angular de paso del motor y $P_w$ es la velocidad del puso medida en Hz.

### Conexión
Las conexiones para el driver y el motor son las estándares, el único detalle es que por defecto se configura el driver el "Full step" poniendo todos los pines `MSX` a tierra. A continuación se deja un esquema de las conexiones del Arduino con el driver y el motor. 

<p align="center">
  <image src="../../../img/A4988_conection.jpg" alt="Descripción de la imagen" width="500x" justify="center"/>
</p>

### Codificación
El código para controlar el motor fue diseñado para configurar la velocidad de acuerdo a la ecuación (1) a través del comando 
"`S[vel. en rpm]`", internamente el microcontrolador hace la conversión de este dato a velocidad de pulso y con ello genera los pasos de para mover el motor. El movimiento del motor fue pensando para hacer el recorrido redondo en el riel, es decir, ir y volver a posición original. Para poner en marcha dicho movimiento se envía el comando "`R`". 

Para lograr que la rotación del motor cambie de sentido al llegar al extremo del camino del riel, se añade un interruptor que al ser presionado cambia el valor del pin `DIR`. Igualmente, hay otro interruptor que al ser presionado indica el final del recorrido y detiene el movimiento (ver figura).  

El Arduino fue configurado como un esclavo, y los comandos que debe recibir se capturan desde el [Arduino maestro][master].

<p align="center">
  <image src="../../../img/motor_rail.jpg" alt="Descripción de la imagen" height="150x" justify="center"/>
</p>

[^1]: https://es.wikipedia.org/wiki/Motor_paso_a_paso
[^2]: https://www.youtube.com/watch?v=VCv4PeEWfzQ

[video]: https://youtu.be/b_-PQCjyRRQ

[motor]: https://www.didacticaselectronicas.com/index.php/elementos-electromecanicos/motores-y-solenoides-1/motores-paso-a-paso/otros-paso-a-paso/OK35STH28-0504A-detail

[driver]: https://www.didacticaselectronicas.com/index.php/cnc-imp3d/controladores-cnc-y-3d/drivers/tar-a4988-detail

[libreria]: https://github.com/laurb9/StepperDriver

[master]: ../../firmware/master_code