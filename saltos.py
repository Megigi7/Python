import random as rand
import pandas as pd

#--#--#--#--# PREPARACION DE DATOS #--#--#--#--#
grado_dificultad = [] #Grado de dificultad de los 3 saltos
for i in range (0,3):
    grado_dificultad.append(int(rand.random()*10)/10)

#Datos personales de saltadores
saltadores = [
    ["Raúl", "Capablanca", "Federación Cubana", 2780],
    ["José", "Martínez", "Federación Bética", 2638],
    ["Iván", "Gómez", "Federación Suiza", 2809],
    ["Pepe", "Pepito", "Federación Pepe", 2323],
    ["Ubuntu", "Proxmox", "Federación Torretas", 2080],
    ["Skibidi", "Sigma", "Federación Rizzler", 2679],
    ["Impac", "Tum", "Federación PC", 2180]]

#Lista de posibles notas
posibles_notas = []
for i in range(0,10):
    posibles_notas.append(i)
    posibles_notas.append(i+0.5)
    i-=0.5
posibles_notas.append(10)


#--#--#--#--# FUNCIONES #--#--#--#--#
#Todos los saltos de todos los saltadores
def calcular_todos_saltos(lista_saltadores, saltos):
    saltos_X_de_todos_saltadores = [ #ANTIGUO saltos_por_saltador !!!!!!!!!
    #Saltador 1 -> [salto_1, salto_2, salto_3],
    #Saltador 2 -> [salto_1, salto_2, salto_3], ....
    ]
    for i in lista_saltadores:
        saltos_X = [] #nota final de los X saltos
        for salto in range(saltos):
            puntuaciones_salto = [] #las 5 puntuaciones de 1 salto
            for juez in range(5):
                puntuaciones_salto.append(rand.choice(posibles_notas))
            puntuaciones_salto.sort()
            puntuacion_salto = 0 #suma de las puntuaciones
            for punt_valido in range(1, len(puntuaciones_salto)-1):
                puntuacion_salto += puntuaciones_salto[punt_valido]
            saltos_X.append(puntuacion_salto)
        saltos_X_de_todos_saltadores.append(saltos_X)
    return saltos_X_de_todos_saltadores

#Organizar nombres, apellidos y rankings para tabla
def datos_saltadores_para_tabla(lista_saltadores): # ← SALTADORES
    competi_nombre =[]; competi_apellido = []; competi_ranking = []
    for i in lista_saltadores:
        competi_nombre.append(i[0])
        competi_apellido.append(i[1])
        competi_ranking.append(i[3])
    datos = [competi_nombre, competi_apellido, competi_ranking]
    return datos

#Organizar saltos para tabla    # ↓ SALTOS POR SALTADOR
def datos_saltos_para_tabla(lista_saltos , n_saltos):
    todos_salto_1 = []; todos_salto_2 = [];todos_salto_3 = []; datos=[]
    if n_saltos==2:
        datos = [todos_salto_1, todos_salto_2]
    elif n_saltos==3:
        datos = [todos_salto_1, todos_salto_2, todos_salto_3]

    for n_jug in lista_saltos:
        salto_x = 0
        for salto in datos:
            salto.append(n_jug[salto_x])
            salto_x +=1
    return datos


#Puntuación total por jugador y numero de jugador
def total_por_saltador(lista_saltos):
    total_por_saltador = [
        #[TOTAL, SALTADOR],
        #[TOTAL, SALTADOR], ...
    ]; num_saltador=1
    for saltador in lista_saltos: #[SALTO 1, SALTO 2, SALTO 3] → Por cada saltador de la lista de todos los saltos de cada saltador
        total_y_saltador = [] #TOTAL, SALTADOR
        total = 0; grado = 0
        for salto in saltador: #SALTO X
            total += salto * grado_dificultad[grado]
            grado+=1
        total_y_saltador.append(int(total*10)/10)
        total_y_saltador.append(num_saltador) # = [TOTAL, N_SALT]
        num_saltador+=1
        total_por_saltador.append(total_y_saltador)
    return total_por_saltador

#Solo la puntuación
def sacar_totales_de_tps(total_por_saltador):
    totales = []
    for t in total_por_saltador:
        totales.append(t[0])
    return totales

#Ordenar por total
def ordenar_puesto(total_por_saltador):
    total_ordenado = sorted(total_por_saltador, reverse=True)
    ranking = []
    for i in total_ordenado:
        ranking.append(123)
    for i in range(0, len(ranking)):
        ranking[total_ordenado[i][1]-1] = i+1
    return ranking

#--#--#--#--# PREPARANDO DATOS PARA LA TABLA DE LA COMPETICION #--#--#--#--#
total_saltos_saltadores = calcular_todos_saltos(saltadores, 3) #saltos_por_saltador / #lista_saltos
ronda2_saltos_saltadores = calcular_todos_saltos(saltadores, 2) #saltos_por_saltador r2
datos_saltadores = datos_saltadores_para_tabla(saltadores) #n, a, r
datos_saltos = datos_saltos_para_tabla(total_saltos_saltadores, 3) #s1, s2, s3
total_y_saltador = total_por_saltador(total_saltos_saltadores) #[total, saltador], ...
total_y_saltador_r2 = total_por_saltador(ronda2_saltos_saltadores) # ↑ RONDA 2 (EJ 3)

# ----------- Nombre
competi_nombre = datos_saltadores[0]
# ----------- Apellido
competi_apellido = datos_saltadores[1]
# ----------- Ranking
competi_ranking = datos_saltadores[2]
# ----------- Salto 1
todos_salto_1 = datos_saltos[0]
# ----------- Salto 2
todos_salto_2 = datos_saltos[1]
# ----------- Salto 3
todos_salto_3 = datos_saltos[2]
# ----------- Total
totales_acti1 = sacar_totales_de_tps(total_y_saltador)
# ----------- Puesto
puesto_acti1 = ordenar_puesto(total_y_saltador)


# ----------- Ronda 2
# ----------- Total
totales_ronda2 = sacar_totales_de_tps(total_y_saltador_r2)
# ----------- Puesto
puesto_ronda2 = ordenar_puesto(total_y_saltador_r2)

#--#--#--#--# ACTIVIDADES #--#--#--#--#
## ACTIVIDAD 1
competicion_act1 = {
    'Nombre': competi_nombre,
    'Apellido': competi_apellido,
    'Ranking': competi_ranking,
    'Salto 1': todos_salto_1,
    'Salto 2': todos_salto_2,
    'Salto 3': todos_salto_3,
    'Total': totales_acti1,
    'Puesto': puesto_acti1,
}
tabla = pd.DataFrame(competicion_act1)
tabla_ordenada = tabla.sort_values(by=['Puesto'], ascending=True)
print("--------------------------------------------------------------------------")
print(tabla_ordenada)
print("--------------------------------------------------------------------------\n")

## ACTIVIDAD 2
for i in range(1,4):
    salto = 'Salto ' + str(i)
    tabla_salto = tabla.sort_values(by=[salto], ascending=False)
    saltador = tabla_salto[tabla_salto[salto] == tabla_salto[salto].max()]
    datos_salt = saltador.iloc[0]
    print("El saltador " + str(datos_salt['Nombre']) + " " + str(datos_salt['Apellido']) + " hizo el mejor salto "+ str(i)+" obteniendo: "+ str(datos_salt[salto]) +" puntos ")


## ACTIVIDAD 3
ronda_2 = {
    'Nombre': competi_nombre,
    'Apellido': competi_apellido,
    'Salto 1': todos_salto_1,
    'Salto 2': todos_salto_2,
    'Total': totales_ronda2,
    'Puesto': puesto_ronda2, 
}
tabla_ranking_prov = pd.DataFrame(ronda_2)
tabla_ranking_prov_ordenada = tabla_ranking_prov.sort_values(by=['Puesto'], ascending=True)
print("\n---------RANKING PROVISIONAL PARA LA SEGUNDA RONDA----------")
print(tabla_ranking_prov_ordenada)
print("------------------------------------------------------------")


## ACTIVIDAD 4
top_5_nombre = []; top_5_apellido = []; top_5_ranking = []; top_5_fede = []
for i in range(1,6):
    salt_puesto = tabla_ordenada[tabla_ordenada['Puesto'] == i]
    datos_salt = salt_puesto.iloc[0]
    top_5_nombre.append(str(datos_salt['Nombre']))
    top_5_apellido.append(str(datos_salt['Apellido']))
    top_5_ranking.append(int(datos_salt['Ranking']))
    for saltador in saltadores:
        if saltador[0] == top_5_nombre[i-1]:
            top_5_fede.append(saltador[2])

top_5 = {   
    'Puesto': [1,2,3,4,5], 
    'Nombre': top_5_nombre,
    'Apellido': top_5_apellido,
    'Ranking': top_5_ranking,
    'Federación': top_5_fede,
}
tabla_top_5 = pd.DataFrame(top_5)
print("----------------------------TOP 5---------------------------")
print(tabla_top_5)
print("------------------------------------------------------------")


## ACTIVIDAD 5
print("\n¡¡¡¡HA OCURRIDO UN IMPREVISTO!!!!\nRaúl Capablanca no pasa el control anti-doping, consumió por error una sustancia prohibida y resulta descalificado\nPresentamos el ranking actualizado")

# ------ DATOS ---------
#Eliminar raul
saltadores_act = saltadores.copy()
del saltadores_act[0] #eliminar raul

total_saltos_saltadores_act = total_saltos_saltadores.copy()
del total_saltos_saltadores_act[0] #eliminar raul

#Nuevos calculos
datos_saltadores_act = datos_saltadores_para_tabla(saltadores_act) #n, a, r
datos_saltos_act = datos_saltos_para_tabla(total_saltos_saltadores_act, 3) #s1, s2, s3
total_y_saltador_act = total_por_saltador(total_saltos_saltadores_act) #[total, saltador], ...

# ----------- Nombre
competi_nombre_act = datos_saltadores_act[0]
# ----------- Apellido
competi_apellido_act = datos_saltadores_act[1]
# ----------- Ranking
competi_ranking_act = datos_saltadores_act[2]
# ----------- Salto 1
todos_salto_1_act = datos_saltos_act[0]
# ----------- Salto 2
todos_salto_2_act = datos_saltos_act[1]
# ----------- Salto 3
todos_salto_3_act = datos_saltos_act[2]
# ----------- Total
totales_act = sacar_totales_de_tps(total_y_saltador_act)
# ----------- Puesto
puesto_act = ordenar_puesto(total_y_saltador_act)


datos_tabla_sin_raul = {
    'Nombre': competi_nombre_act,
    'Apellido': competi_apellido_act,
    'Ranking': competi_ranking_act,
    'Salto 1': todos_salto_1_act,
    'Salto 2': todos_salto_2_act,
    'Salto 3': todos_salto_3_act,
    'Total': totales_act,
    'Puesto': puesto_act, 
}

tabla_sin_raul = pd.DataFrame(datos_tabla_sin_raul)
tabla_sin_raul_ordenada = tabla_sin_raul.sort_values(by=['Puesto'], ascending=True)
print("-------------------------TABLA FINAL ACTUALIZADA------------------------")
print(tabla_sin_raul_ordenada)
print("------------------------------------------------------------------------")

