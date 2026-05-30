'''
Problema 5 - Modulo 1 - Persistencia binaria de pacientes - Chalan Maycol

Sección declarativa:

(a) Declarar FORMATO = '<i30s24s16sB' y TAM_REGISTRO = struct.calcsize(FORMATO)
como constantes globales (fuente única de verdad). Implementar empaquetar_paciente y
desempaquetar_paciente, con codificación UTF-8, truncado de cadenas largas y removido
del relleno de ceros al desempaquetar. El campo prioridad es un entero de 1 (alta) a 3
(baja).

(b) Implementar crear_archivo_pacientes(ruta, lista_pacientes) y
leer_paciente(archivo, k) con acceso directo por offset (seek(k * TAM_REGISTRO)). Usar
el context manager with en todo acceso a archivo.
'''
import struct
import os

FORMATO = '<i30s24s16sB'
TAM_REGISTRO = struct.calcsize(FORMATO)


def empaquetar_datos(dni, apellido, nombre, telefono, prioridad):
    """
    Convierte los datos de un paciente a bytes de longitud fija.
    Precondicion:
    - dni es un int.
    - apellido, nombre, telefono son str.
    - prioridad es un int entre 1 y 3.
    Postcondicion:
    - devuelve bytes de longitud TAM_REGISTRO listos para escribir en disco.
    """
    return struct.pack(
        FORMATO,
        dni,
        apellido.encode('utf-8')[:32].ljust(32, b'\x00'),
        nombre.encode('utf-8')[:24].ljust(24, b'\x00'),
        telefono.encode('utf-8')[:16].ljust(16, b'\x00'),
        prioridad,
    )


def decempaquetar_paciente(raw):
    """
    Convierte bytes leidos del archivo en una tupla de datos del paciente.
    Precondicion:
    - raw es un bytes de longitud TAM_REGISTRO.
    Postcondicion:
    - devuelve (dni, apellido, nombre, telefono, prioridad) con strings
      decodificados en UTF-8 y sin relleno de bytes nulos.
    """
    dni, apellido, nombre, telefono, prioridad = struct.unpack(FORMATO, raw)
    return (
        dni,
        apellido.rstrip(b'\x00').decode('utf-8'),
        nombre.rstrip(b'\x00').decode('utf-8'),
        telefono.rstrip(b'\x00').decode('utf-8'),
        prioridad,
    )


def crear_archivo_pacientes(ruta, lista_pacientes):
    """
    Crea (o sobreescribe) el archivo binario con todos los pacientes de la lista.
    Precondicion:
    - ruta es una ruta de archivo valida.
    - lista_pacientes es una lista de tuplas (dni, apellido, nombre, telefono, prioridad).
    Postcondicion:
    - el archivo ruta contiene len(lista_pacientes) registros de TAM_REGISTRO bytes cada uno.
    - os.path.getsize(ruta) == len(lista_pacientes) * TAM_REGISTRO.
    """
    with open(ruta, 'wb') as f:
        for paciente in lista_pacientes:
            f.write(empaquetar_datos(*paciente))


def leer_paciente(archivo, k):
    """
    Lee y devuelve el paciente en la posicion k usando acceso directo por offset.
    Precondicion:
    - archivo es un objeto de archivo abierto en modo binario.
    - 0 <= k < cantidad total de registros en el archivo.
    Postcondicion:
    - devuelve una tupla (dni, apellido, nombre, telefono, prioridad).
    """
    archivo.seek(k * TAM_REGISTRO)
    raw = archivo.read(TAM_REGISTRO)
    return decempaquetar_paciente(raw)


# Casos de prueba

if __name__ == '__main__':
    ruta = 'pacientes_test.dat'

    pacientes = [
        (12345678, 'Garcia', 'Juan', '1122334455', 1),
        (87654321, 'Lopez', 'Maria', '9988776655', 2),
        (11111111, 'Martinez', 'Carlos', '5544332211', 3),
        (22222222, 'Rodriguez', 'Ana', '6677889900', 1),
    ]

    crear_archivo_pacientes(ruta, pacientes)

    tamanio_esperado = len(pacientes) * TAM_REGISTRO
    tamanio_real = os.path.getsize(ruta)
    print(f'Tamaño esperado : {tamanio_esperado} bytes')
    print(f'Tamaño real: {tamanio_real} bytes')
    print(f'Coinciden : {tamanio_esperado == tamanio_real}')
    print()

    with open(ruta, 'rb') as f:
        for k in range(len(pacientes)):
            p = leer_paciente(f, k)
            print(f'Registro {k}: {p}')