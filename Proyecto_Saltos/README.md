Este proyecto simula una competición ficticia de trampolín, donde varios saltadores realizan tres saltos evaluados por cinco jueces. La puntuación se ajusta según reglas oficiales, incluyendo un grado de dificultad único para todos los participantes.

### Reglas Principales
 - Saltos: Cada salto es evaluado eliminando la puntuación más alta y más baja, sumando las restantes.
 - Grado de Dificultad: Aleatorio entre 0 y 1, aplicado como multiplicador a las puntuaciones.
### Implementación
 - Datos generados y gestionados con pandas.
 - Cálculo automatizado de puntuaciones y totales.

Contamos con diferentes apartados:

### Actividad 1
Realizar un programa que produzca un listado de salida de las puntuaciones ordenado por puntuación total y con la siguiente cabecera:
  NOMBRE | APPELLIDO | RANKING | SALTO1 | SALTO2 | SALTO3 | TOTAL | PUESTO

### Actividad 2
Unas líneas más abajo de la primera salida, deberéis indicar la identidad del saltador que obtuvo el mejor salto en cada ronda de la competición

### Actividad 3
Más abajo, muestra un listado en el que aparezca la clasificación provisional del torneo en la segunda ronda de saltos. 
Emplea el mismo formato de salida de la primera tabla pero sin que aparezca el Ranking de cada saltador en la cabecera.

### Actividad 4
Elabora en otro listado de salida de la clasificación final en la que figuren los cinco primeros saltadores detallando la siguiente información:
  PUESTO | NOMBRE | APPELLIDO | RANKING | FEDERACION

### Actividad 5
Raúl Capablanca no pasa el control anti-doping, consumió por error una sustancia prohibida y resulta descalificado.
Vuelve a mostrar una visualización por pantalla de la clasificación general pero sin que aparezca dicho participante 


