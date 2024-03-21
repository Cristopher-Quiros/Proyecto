def validar(numero):
    while True:
        if numero.isdigit():
            return int(numero)
        else:
            numero = input("Ingrese un numero valido: ")
import csv

def consultar_datos_jugador(nombre_archivo, nombre_jugador):
    with open(nombre_archivo, 'r') as archivo:
        lector_csv = csv.DictReader(archivo)
        for fila in lector_csv:
            if fila['Ejemplo'] == nombre_jugador:
                return fila
        return None

def imprimir_informacion_jugador(informacion_jugador):
    if informacion_jugador is not None:
        print("Información del jugador:")
        for clave, valor in informacion_jugador.items():
            print(f"{clave}: {valor}")
    else:
        print("Jugador no encontrado.")

def consultar_informacion_jugador(nombres_archivos, nombre_jugador):
    for nombre_archivo in nombres_archivos:
        informacion_jugador = consultar_datos_jugador(nombre_archivo, nombre_jugador)
        print(f"Información del jugador {nombre_jugador} en {nombre_archivo}:")
        imprimir_informacion_jugador(informacion_jugador)
        print("\n")  # Imprime una línea en blanco entre resultados

nombres_archivos = ['Testeo.csv']  # Cambia por el nombre de tu archivo CSV
nombre_jugador = 'Messi'  # Cambia por el nombre del jugador que quieres consultar

consultar_informacion_jugador(nombres_archivos, nombre_jugador)

# consultar_datos_jugadores(nombres_archivos, nombre_jugador)



# consultar_datos_csvs(nombres_archivos, filas, columnas) # Imrpime las tablas

# Leer información de un jugador.

print("Que desea hacer?")
print("1. Agregar un nuevo jugador ")
print("2. Consultar sobre un jugador")
print("3. Eliminar un jugador")

while True:

    opciones = validar(input("Cual opcion quiere elegir?: "))

    if opciones == 2:
        consultar_datos_jugador(nombres_archivos, nombre_jugador)

