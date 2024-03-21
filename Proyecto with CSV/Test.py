import csv


def consultar_datos_jugador(nombre_archivo, nombre_jugador):
    with open(nombre_archivo, 'r') as archivo:
        lector_csv = csv.DictReader(archivo)
        for fila in lector_csv:
            if fila['Ejemplo'] == nombre_jugador:
                return fila
        return None

def imprimir_datos_jugador(jugador):
    if jugador is not None:
        print("Información del jugador:")
        for clave, valor in jugador.items():
            print(f"{clave}: {valor}")
    else:
        print("Jugador no encontrado.")

def consultar_datos_jugadores(nombres_archivos):
    nombre_jugador = input("Ingrese el nombre del jugador que desea consultar: ")
    for nombre_archivo in nombres_archivos:
        print(f"Datos de {nombre_jugador} en {nombre_archivo}:")
        jugador = consultar_datos_jugador(nombre_archivo, nombre_jugador)
        imprimir_datos_jugador(jugador)
        print("\n")  # Imprime una línea en blanco entre resultados

nombres_archivos = ['Testeo.csv', 'Estadistica.csv']  # lista de nombres de archivos

print("Que desea hacer?")
print("1. Agregar un nuevo jugador ")
print("2. Consultar sobre un jugador")
print("3. Eliminar un jugador")

opciones = int(input("Cual opcion quiere elegir?: "))

if opciones == 2:
    consultar_datos_jugadores(nombres_archivos)


while True:

    print("Que desea hacer?")
    print("1. Agregar un nuevo jugador ")
    print("2. Consultar sobre un jugador")
    print("3. Eliminar un jugador")

    opciones = int(input("Cual opcion quiere elegir?: "))

    if opciones == 2:
        consultar_datos_jugadores(nombres_archivos)
    else:  
        break
