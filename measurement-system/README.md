# Sistema de medición de temperatura
A continuación, se describe de forma resumida las caracteristicas del sistema de medición de temperatura dos dimensional para caracterizar las condiciones de secado de celdas solares flexibles fabricadas con un sistema Roll to Roll (R2R) (Más detalles pueden encontrarse en [terminos de servicio](https://github.com/GICM-UdeA/Horno-CS/tree/main/measurement-system/docs/documento_terminos_de_servicio.pdf)).

## Hardware
Consiste en un DAQ (data acquisition system) basado en Arduino y Python. El Hardware, se encarga de monitorear las temperaturas medidas por el conjunto de 5 termocuplas tipo K, y reporta los registros al usuario a través de una interfaz gráfica de usuario (ver Figura del sistema). En esta última, se pueden ver en tiempo real los datos tomados de forma gráfica, con posibilidad de extraerlos en un archivo Excel para su posterior análisis.

<img src ="../img/Imagen_CS_TC.png" width=800 align="center">

Los detalles sobre el diseño del circuito y la programación del Hardware pueden consultarse en la carpeta del [`hardware`](https://github.com/GICM-UdeA/Horno-CS/tree/main/measurement-system/hardware).

> [!NOTE]
> La conexión entre el Hardware y Software se tratará de implementar via bluethooth.

## Software
Desde la interfaz gráfica se podrá visualizar, en el “panel de visualización” (Ver Figura de la Interfaz), la información registrada por el Arduino a través de dos gráficas. Desde el “panel de conexión” se asegura que la comunicación entre el Hardware y Software se establezca exitosamente. Desde el panel de “Parámetros del experimento” se registran los datos relevantes del experimento que se esté realizando para su posterior identificación. Finalmente, desde el “panel de archivo” se establece la ruta donde se deben exportar los datos una vez finalizado el experimento.

<img src ="../img/Imagen_CS_TC_interface.png" width=800 align="center">

Los detalles sobre la programación del software pueden consultarse en la carpeta del [`software`](https://github.com/GICM-UdeA/Horno-CS/tree/main/measurement-system/software).