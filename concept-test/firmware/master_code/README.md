# Arduino principal - Master 
El Arduino que contiene este programa está encargado de mantener la comunicación con el usuario mediante protocolo serial y enviar los comandos necesarios a los dispositivos esclavos para el control de los subsistemas (Motor y fuente de calor). Además, es el encargado de hacer la medición de temperatura a lo largo del recorrido de la muestra cuando la toma de datos se desencadene.

### Medición de la temperatura
La temperatura se registra a través de un termopar formado a partir de dos conductores (Alumel-Cromel de 0.005 de diámetro). Esto con el fín de tener un sensor de respuesta rápida ante los cambios de temperatura. El termopar se conecta a un amplificador MAX6675, y su codificación se basa en lo expuesto en el siguiente [blog][electronoobs]. 

### Conexión
A continuación se deja un esquema de las conexiones del Arduino con el al amplificador MAX6675. 

<p align="center">
  <image src="../../../img/master_thermocouple.jpg" alt="Descripción de la imagen" width="500x" justify="center"/>
</p>

### Codificación
Los comandos para el control del motor son recibidos por serial y luego transmitidos por I2C al resto de dispositivo con la misma sintaxis (por ejemplo, "`S[vel. en rpm]`" para el control de velocidad y "`R`" para comenzar el movimiento de motor). Adicionalmente, la ejecución del comando "`R`" comienza la medición de temperatura hasta que reciba la señal del esclavo que controla el motor que indique que el recorrido termino. Esta señal se recibe como una interrupción por el pin `2`. 


[electronoobs]: https://electronoobs.com/eng_arduino_tut24.php

