"""
Franjas por dia --------> 8 franjas de 30 minutos
Pacientes con restricciones de disponibilidad -------> una lista por pacientes de las franjas que puede asistir
El problema es asignar cada paciente de una lista del día a una franja,
respetando que (1) cada franja recibe a lo sumo un paciente y (2) cada paciente queda en una
franja compatible con su disponibilidad.
"""


"""
LA FUNCION A CREAR ASINGAR_AGENDA (PACIENTES_DEL_DIA, FRANJAS, DISPONIBILIDAD)
"""

def asignar_agenda(pacientes_del_dia, franja, disponibilidad):
    """Genera todas las asignaciones a pacientes respetando su disponibilidad acomodandose a la franja.

    Precondición: pacientes es una lista; sus elementos son distinguibles.
    Postcondición: devuelve una lista con una posible asignacion.
    Complejidad: O(n · n!) tiempo, O(n · n!) espacio para el resultado.
    """
    # --- Prólogo: estructuras iniciales para el backtracking --------
    soluciones = {}
    franjas_usadas = set()
    # --- Resolución: delegar la exploración al algoritmo recursivo --
    exito = _explorar_asignaciones(pacientes_del_dia, franja, disponibilidad, soluciones,franjas_usadas)

    # --- Epílogo: devolver todas las soluciones encontradas ---------\
    if exito:
        return soluciones
    else:
        return None

def _explorar_asignaciones(pacientes, franjas, disponibilidad, soluciones,franjas_usadas):

    #--------- caso base --------
    if len(pacientes) == len(soluciones):
        return True
    #--------- Caso recursivo -----------
    paciente_actual = pacientes[len(soluciones)]
    for franja in franjas:
        if franja in disponibilidad[paciente_actual] and franja not in franjas_usadas: #poda, nahorra muchisimo trabajo al programa
            #Estado parcial
            soluciones[paciente_actual] = franja
            franjas_usadas.add(franja)
            #activamos recursividad y buscamos el siguiente nivel
            if _explorar_asignaciones(pacientes, franjas, disponibilidad, soluciones, franjas_usadas):
                return True
            #si no funciona, Back-track. Descartamos esa opcion
            del soluciones[paciente_actual]
            franjas_usadas.remove(franja)

    return False



# --- EJECUCIÓN (en forma de script, para molestar programa principal)---
if __name__ == "__main__":
     # Datos para probar.
     franjas_del_dia = [
         "08:00", "08:30", "09:00", "09:30",
         "10:00", "10:30", "11:00", "11:30"
     ]

     pacientes_test = ["Juan", "Ana", "Pedro", "Maria"]

     disponibilidad_test = {
         "Juan": ["08:00"],
         "Ana": ["08:00"],
         "Pedro": ["08:30", "09:30"],
         "Maria": ["11:00", "11:30"]
     }

     resultado = asignar_agenda(pacientes_test, franjas_del_dia, disponibilidad_test)

     if resultado:
                 print(" Asignación encontrada:")
                 for paciente, franja in resultado.items():
                    print(f"  - {paciente}: {franja}")
     else:
                print("No existe una asignación válida para estos pacientes.")

"""
Discusion:
Sabiendo que el back-track sirve para buscar posibles combinaciones, -como por ejemplo posibles uniones de conjuntos dado 3 conjuntos, posibles numeros consecutivos
dada una fila de elementos comparables- todo ese proceso tiene un costo de O(N!). 
Si este problema lo hariamos a la 'fuerza bruta', en un ejemplo donde hay 8 franjas y 4 pacientes el programa de todas formas buscaria las posibles soluciones aunque un paciente no pueda en tal franja.
En cambio al agregar la poda y hacer el Back-tracking si un paciente solo puede en 2 franjas de horarios, las otras 6 ni las analiza, descartando esa opcion, ahorrando el procesamiento de combinaciones invalidas
"""

