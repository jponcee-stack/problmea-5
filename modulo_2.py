'''
Problema 5 - Modulo 2 - Indices en memoria - Chalan Maycol

Sección declarativa:

(c) Implementar construir_indices(ruta) que recorra una sola vez el archivo binario y
devuelva dos diccionarios: indice_por_dni (clave: DNI, valor: posición k del registro en el
archivo) e indice_por_apellido (clave: apellido, valor: lista de posiciones, porque puede
haber apellidos repetidos).

(d) Implementar buscar_por_dni(archivo, indice_por_dni, dni) que resuelva la
búsqueda en O(1) promedio consultando el diccionario y leyendo un único registro. Comparar
conceptualmente, en la docstring, con el costo de una búsqueda secuencial O(n) sobre el
archivo sin índice.
'''

import os
from modulo_1 import TAM_REGISTRO, leer_paciente

def construir_indices(ruta):
    """
    Recorre el archivo binario una sola vez y construye dos indices en memoria.
    Precondicion:
    - ruta apunta a un archivo valido creado por crear_archivo_pacientes.
    Postcondicion:
    - devuelve (indice_por_dni, indice_por_apellido) donde:
        indice_por_dni : dict { dni (int) -> k (int) }
        indice_por_apellido : dict { apellido (str) -> [k, ...] }
    """
    indice_por_dni = {}
    indice_por_apellido = {}

    total = os.path.getsize(ruta) // TAM_REGISTRO

    with open(ruta, 'rb') as f:
        for k in range(total):
            dni, apellido, nombre, telefono, prioridad = leer_paciente(f, k)
            indice_por_dni[dni] = k
            if apellido not in indice_por_apellido:
                indice_por_apellido[apellido] = []
            indice_por_apellido[apellido].append(k)

    return indice_por_dni, indice_por_apellido


def buscar_por_dni(archivo, indice_por_dni, dni):
    """
    Busca un paciente por DNI en O(1) promedio usando el indice en memoria.
    Precondicion:
    - archivo es un objeto de archivo abierto en modo binario ('rb').
    - indice_por_dni fue construido por construir_indices sobre ese archivo.
    - dni es un int.
    Postcondicion:
    - devuelve la tupla (dni, apellido, nombre, telefono, prioridad) si el
      DNI existe, o None si no fue encontrado.

    Comparacion de costos:
    - Con indice (este metodo): O(1) promedio. El diccionario resuelve la
      posicion k en tiempo constante; luego se hace una sola lectura con seek.
    - Sin indice (busqueda secuencial): O(n). Habria que leer registro por
      registro desde el inicio hasta encontrar el DNI buscado, recorriendo
      en el peor caso la totalidad del archivo.
    """
    if dni not in indice_por_dni:
        return None
    k = indice_por_dni[dni]
    return leer_paciente(archivo, k)


#Casos de prueba del modulo

if __name__ == '__main__':
    from modulo_1 import crear_archivo_pacientes

    ruta = 'pacientes_test2.dat'

    pacientes = [
        (12345678, 'Garcia', 'Juan', '1122334455', 1),
        (87654321, 'Lopez', 'Maria', '9988776655', 2),
        (11111111, 'Martinez', 'Carlos', '5544332211', 3),
        (22222222, 'Lopez', 'Ana', '6677889900', 1),
    ]
    crear_archivo_pacientes(ruta, pacientes)

    idx_dni, idx_apellido = construir_indices(ruta)

    print('Indice por DNI')
    for dni, pos in idx_dni.items():
        print(f'  DNI {dni} -> posicion {pos}')

    print()
    print('Indice por apellido')
    for apellido, posiciones in idx_apellido.items():
        print(f'  {apellido} -> posiciones {posiciones}')

    print()
    print('Busquedas por DNI')
    with open(ruta, 'rb') as f:
        encontrado = buscar_por_dni(f, idx_dni, 87654321)
        print(f'  DNI 87654321 -> {encontrado}')

        no_encontrado = buscar_por_dni(f, idx_dni, 99999999)
        print(f'  DNI 99999999 -> {no_encontrado}')

        # Verificar que todos los DNIs devuelven el registro correcto
        todos_ok = True
        for p in pacientes:
            resultado = buscar_por_dni(f, idx_dni, p[0])
            if resultado is None or resultado[0] != p[0]:
                todos_ok = False
        print(f'  Todas las busquedas correctas: {todos_ok}')