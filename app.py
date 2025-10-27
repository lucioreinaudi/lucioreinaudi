import alumnos
al = alumnos.alumno
insFut = []
insVol = []
insTejo = []
tejo = 'tejo'


# Funcion asignar deporta
def asignarDeporte(actividad,lista):
    for alumno in al:      
        actividad_actual = alumno['actividad']
        nombre_alumno = alumno['nombre']
        if actividad_actual == actividad:
            lista.append(alumno)


asignarDeporte('futbol',insFut)
asignarDeporte('volley',insVol)
asignarDeporte('tejo',insTejo)

def divisor_por_genero_y_actividad(lista, actividad):
    for i in lista:
        if i['genero'] == 'M' and i['actividad'] == actividad:
            print(f"Los varones inscriptos en futbol son {i['nombre']}")

        if i['genero'] == 'F' and i['actividad'] == actividad:
            print(f"Las mujeres inscriptas en futbol son {i['nombre']}")

divisor_por_genero_y_actividad(insFut,'futbol')

def asignarEquipo(listaM, listaF, cuporPorEquipo):
    num_hombres = len(listaM)
    num_mujeres = len(listaF)
