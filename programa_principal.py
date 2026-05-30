"""
Problema 5 - Main - Gestión de turnos médicos - Chalan Maycol

Programa principal que articula los cuatro módulos en un flujo completo.
No contiene lógica propia: sólo coordina las funciones de cada módulo.
"""

import os
from modulo_1 import crear_archivo_pacientes
from modulo_2 import construir_indices, buscar_por_dni
from Modulo_3 import listar_pacientes_ordenados
from modulo_4 import asignar_agenda

# ===================================
#           CONSTANTES
# ===================================

RUTA = 'pacientes.dat'

FRANJAS_DEL_DIA = [
    "08:00", "08:30", "09:00", "09:30",
    "10:00", "10:30", "11:00", "11:30"
]

# ===================================
#        DATOS INICIALES
# ===================================

PACIENTES_INICIALES = [
    (12345678, 'Garcia',    'Juan',   '1122334455', 1),
    (87654321, 'Lopez',     'Maria',  '9988776655', 2),
    (11111111, 'Martinez',  'Carlos', '5544332211', 3),
    (22222222, 'Rodriguez', 'Ana',    '6677889900', 1),
    (33333333, 'Lopez',     'Pedro',  '1133557799', 2),
]

# Pacientes del día y su disponibilidad horaria (para la agenda)
PACIENTES_DEL_DIA = ['Garcia', 'Lopez', 'Martinez']

DISPONIBILIDAD = {
    'Garcia':   ['08:00', '09:00'],
    'Lopez':    ['08:00', '08:30'],
    'Martinez': ['09:00', '09:30', '10:00'],
}

# ===================================
#        FUNCIONES DE DISPLAY
# ===================================

def _mostrar_paciente(tupla):
    """Imprime una tupla de paciente en formato legible."""
    dni, apellido, nombre, telefono, prioridad = tupla
    print(f'DNI: {dni} | {apellido}, {nombre} | Tel: {telefono} | Prioridad: {prioridad}')


def _mostrar_lista(lista):
    """Imprime una lista de tuplas de pacientes."""
    for tupla in lista:
        _mostrar_paciente(tupla)


def _mostrar_menu():
    """interfaz desde la terminal que imprime las opciones del menú"""
    print()
    print('====== SISTEMA DE TURNOS MÉDICOS ======')
    print('  1. Buscar paciente por DNI')
    print('  2. Listar pacientes por apellido')
    print('  3. Listar pacientes por prioridad')
    print('  4. Resolver agenda del día')
    print('  5. Salir')
    print('=======================================')

# ===================================
#        PROGRAMA PRINCIPAL
# ===================================

def main():
    """Flujo principal del sistema de turnos médicos."""

    # --- crear archivo binario con los pacientes iniciales ---
    crear_archivo_pacientes(RUTA, PACIENTES_INICIALES)
    print(f'Archivo creado: {RUTA}')

    # --- construir índices en memoria ------------------------
    indice_dni, indice_apellido = construir_indices(RUTA)
    print(f'Índices construidos: {len(indice_dni)} registros.')

    # --- Paso 3: menú de consulta ------------------------------------
    continuar = True
    while continuar:
        _mostrar_menu()
        opcion = input('Ingrese una opción: ')

        if opcion == '1':
            dni = int(input('Ingrese DNI:'))
            with open(RUTA, 'rb') as f:
                resultado = buscar_por_dni(f, indice_dni, dni)
            if resultado:
                print('Paciente encontrado:')
                _mostrar_paciente(resultado)
            else:
                print('DNI no encontrado.')

        elif opcion == '2':
            print('Pacientes ordenados por apellido:')
            _mostrar_lista(listar_pacientes_ordenados(RUTA, 'apellido'))

        elif opcion == '3':
            print('Pacientes ordenados por prioridad (y apellido en caso de empate):')
            _mostrar_lista(listar_pacientes_ordenados(RUTA, 'prioridad'))

        elif opcion == '4':
            resultado = asignar_agenda(PACIENTES_DEL_DIA, FRANJAS_DEL_DIA, DISPONIBILIDAD)
            if resultado:
                print('Agenda del día asignada:')
                for paciente, franja in resultado.items():
                    print(f'    {paciente}: {franja}')
            else:
                print('No fue posible asignar la agenda con la disponibilidad indicada')

        elif opcion == '5':
            continuar = False
            print('Saliendo del sistema')

        else:
            print('Opción inválida. Ingrese un número del 1 al 5')


if __name__ == '__main__':
    main()