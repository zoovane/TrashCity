#   1. Importaciones:

from abc import ABC, abstractmethod #   Clases y decoradores, para definir clases y métodos abstractos
from datetime import datetime #   Se importa desde el módulo datetime para trabajar con fechas y horas
import random #    Se importa para generar valores aleatorios
import re #    Se importa para trabajar con expresiones regulares


#   2. Definición de clases:

class Persona: #    Es una clase base que representa a una persona con atributos como el nombre y el ID
    def __init__(self, nombre, id):
        self.nombre = nombre
        self.id = id

class Camion: #    Es una clase que representa un camión y tiene un atributo de placa
    def __init__(self, placa):
        self.placa = placa

class Turno: #  Es una clase que contiene información sobre los turnos
    def __init__(self, fecha_inicio, fecha_fin, ruta, camion, conductor, asistente_1, asistente_2):
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.ruta = ruta
        self.camion = camion
        self.conductor = conductor
        self.asistente_1 = asistente_1
        self.asistente_2 = asistente_2
        self.localizaciones = []
        self.recoleccion = {'vidrio': 0, 'papel': 0, 'plastico': 0, 'metal': 0, 'organico': 0}
    def clasificar_residuos(self, vidrio, papel, plastico, metal, organico):
        self.recoleccion['vidrio'] += vidrio
        self.recoleccion['papel'] += papel
        self.recoleccion['plastico'] += plastico
        self.recoleccion['metal'] += metal
        self.recoleccion['organico'] += organico

class Ruta: #   Es una clase que representa una ruta y tiene una lista de puntos geográficos que definen la ruta
    def __init__(self, puntos):
        self.puntos = puntos
    def __str__(self):
        return str(self.puntos)
    def agregar_localizacion(self, latitud, longitud, tiempo):
        self.localizaciones.append((latitud, longitud, tiempo))

class Command(ABC): #   Es una clase abstracta que define el método execute(), que será implementado por clases derivadas
    @abstractmethod
    def execute(self):
        pass

class RecolectarVidrioCommand(Command):
    #   Es una clase que hereda de Command y representa un comando específico para recolectar vidrio en un turno (random)
    def __init__(self, turno):
        self.turno = turno
        self.cantidad = 0
    def execute(self):
        self.cantidad = random.randint(0, 100)
        self.turno.recoleccion['vidrio'] += self.cantidad

class Invocador:    #   Es una clase que tiene un comando y puede ejecutarlo
    def set_command(self, command):
        self.command = command
    def execute_command(self):
        self.command.execute()


#   3. Funciones:

def validar_placa(placa):
    #   Es una función que verifica si una placa de camión cumple con un patrón de formato específico utilizando una expresión regular
    patron = r'^([A-Z]{2}[A-Z]{1}\s\d{3}$)|(^[A-Z]{2}\s\d{4}$)'
    if re.match(patron, placa):
        letras = re.findall(r'[A-Z]', placa)
        numeros = re.findall(r'\d', placa)
        if (len(letras) == 2 and len(numeros) == 4) or (len(letras) == 3 and len(numeros) == 3):
            return True
    return False

def input_entero_positivo(mensaje):
    #   Es una función que solicita al usuario un valor entero positivo y se asegura de que el valor ingresado cumpla con los requisitos
    while True:
        try:
            valor = int(input(mensaje))
            if valor > 0:
                return valor
            else:
                print("Error: Ingrese un número entero positivo.")
        except ValueError:
            print("Error: Ingrese un número entero válido.")

def calcular_vidrio_recolectado(turnos, fecha):
    #   Es una función que calcula la cantidad de vidrio recolectado en una fecha específica sumando 
    #   las cantidades de vidrio recolectadas en todos los turnos que coincidan con esa fecha
    vidrio_recolectado = 0
    for turno in turnos:
        if turno.fecha_inicio.date() == fecha.date():
            for residuo, cantidad in turno.recoleccion.items():
                if residuo == 'vidrio':
                    vidrio_recolectado += cantidad
    return vidrio_recolectado


#   4. Función 'main':

def main():
    #   Se crean listas vacías para almacenar camiones, conductores, asistentes, rutas y turnos
    rutas = []
    conductores = []
    asistentes = []
    camiones = []
    turnos = []

    rutas_preexistentes = [
        [(40.7128, -74.0060), (41.8781, -87.6298), (51.5074, -0.1278)],
        [(-33.8679, 151.2073), (-22.9068, -43.1729), (-34.6037, -58.3816), (48.8566, 2.3522)],
        [(41.9028, 12.4964), (52.5200, 13.4050)]
    ]
    for puntos in rutas_preexistentes:
        ruta = Ruta(puntos)
        rutas.append(ruta)

    print("Bienvenid@ al sistema de manejo de residuos TrashCity")

    #   Se solicita al usuario la cantidad de camiones disponibles y se le pide que ingrese las placas de los camiones
    num_camiones = input_entero_positivo("\nIngrese la cantidad de camiones disponibles: ")
    print("\nPor favor, ingrese la placa del camión utilizando la siguiente nomenclatura:") 
    print("- Las letras deben estar en mayúscula.")
    print("- Para placas con 2 letras y 4 números, escriba las 2 letras seguidas de un espacio y luego los 4 números.")
    print("  Ejemplo: AB 1234")
    print("- Para placas con 3 letras y 3 números, escriba las 3 letras seguidas de un espacio y luego los 3 números.")
    print("  Ejemplo: ABC 123")
    for i in range(num_camiones):
        placa_valida = False
        while not placa_valida:
            placa = input(f"\nIngrese la placa del camión {i+1}: ")
            if not validar_placa(placa):
                print("La placa ingresada no cumple con la nomenclatura de Colombia o tiene una cantidad incorrecta de letras o números. Intente nuevamente.")
            else:
                placa_valida = True
        camion = Camion(placa)
        camiones.append(camion)

    #   Se solicita al usuario la cantidad de conductores y asistentes disponibles, y se le pide que ingrese información sobre ellos (nombre e ID)
    
    num_conductores = input_entero_positivo("\nIngrese la cantidad de conductores disponibles: ")
    for i in range(num_conductores):
        nombre = input(f"\nIngrese el nombre completo del conductor {i+1}: ")
        while True:
            id = input(f"\nIngrese el ID (10 dígitos) del conductor {i+1}: ")
            if id.isdigit() and len(id) == 10:
                break
            else:
                print("El ID debe ser una cadena de 10 dígitos numéricos. Inténtelo nuevamente.")
        conductor = Persona(nombre, id)
        conductores.append(conductor)

    num_asistentes = 0
    while num_asistentes < 2:
        try:
            num_asistentes = int(input("\nIngrese la cantidad de asistentes disponibles (mínimo 2): "))
            if num_asistentes < 2:
                print("Error: Ingrese al menos 2 asistentes.")
        except ValueError:
            print("Error: Ingrese un número entero válido.")
    for i in range(num_asistentes):
        nombre = input(f"\nIngrese el nombre completo del asistente {i+1}: ")
        id = input_entero_positivo(f"\nIngrese el ID (10 dígitos) del asistente {i+1}: ")
        asistente = Persona(nombre, id)
        asistentes.append(asistente)

    #   Se solicita al usuario la cantidad de turnos a registrar y se le pide que ingrese información sobre cada turno, 
    #   incluyendo fecha, hora de inicio, hora de fin, ruta seleccionada, camión asignado, conductor asignado y asistentes asignados
    
    num_turnos = input_entero_positivo("\nIngrese la cantidad de turnos a registrar: ")
    for i in range(num_turnos):
        while True:
            try:
                fecha = input(f"\nIngrese la fecha del turno {i+1} (YYYY-MM-DD): ")
                fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
                break
            except ValueError:
                print("Error: Ingrese una fecha válida en el formato especificado (YYYY-MM-DD).")
        while True:
            try:
                hora_inicio = input(f"\nIngrese la hora de inicio del turno {i+1} (HH:MM): ")
                hora_inicio = datetime.strptime(hora_inicio, "%H:%M").time()
                break
            except ValueError:
                print("Error: Ingrese una hora válida en el formato especificado (HH:MM).")
        while True:
            try:
                hora_fin = input(f"\nIngrese la hora de fin del turno {i+1} (HH:MM): ")
                hora_fin = datetime.strptime(hora_fin, "%H:%M").time()
                break
            except ValueError:
                print("Error: Ingrese una hora válida en el formato especificado (HH:MM).")
        #   Se combina la fecha y la hora para obtener las fechas de inicio y fin completas
        fecha_inicio = datetime.combine(fecha, hora_inicio)
        fecha_fin = datetime.combine(fecha, hora_fin)
        print("\nRutas preexistentes:")
        for i, ruta in enumerate(rutas):
            print(f"{i+1}. {ruta}")
        ruta_seleccionada = None
        while True:
            try:
                ruta_seleccionada = int(input("\nRuta seleccionada: "))
                if ruta_seleccionada > 0 and ruta_seleccionada <= len(rutas):
                    break
                else:
                     print("Error: Seleccione una opción válida.")
            except ValueError:
                 print("Error: Ingrese un número entero válido.") 
        ruta = rutas[ruta_seleccionada-1]
        print("\nSeleccione el camión del turno:")
        for j, camion in enumerate(camiones):
            print(f"{j+1}. {camion.placa}")
        camion_seleccionado = None
        while camion_seleccionado is None:
            try:
                opcion = int(input("\nCamión seleccionado: "))
                if opcion in range(1, len(camiones)+1):
                    camion_seleccionado = camiones[opcion-1]
                else:
                    print("Error: Seleccione una opción válida.")
            except ValueError:
                print("Error: Ingrese un número entero válido.")
        print("\nSeleccione el conductor del turno:")
        for j, conductor in enumerate(conductores):
            print(f"{j+1}. {conductor.nombre} ({conductor.id})")
        conductor_seleccionado = None
        while conductor_seleccionado is None:
            try:
                opcion = int(input("\nConductor seleccionado: "))
                if opcion in range(1, len(conductores)+1):
                    conductor_seleccionado = conductores[opcion-1]
                else:
                    print("Error: Seleccione una opción válida.")
            except ValueError:
                print("Error: Ingrese un número entero válido.")
        print("\nSeleccione los asistentes del turno:")
        for j, asistente in enumerate(asistentes):
            print(f"{j+1}. {asistente.nombre} ({asistente.id})")
        asistente_1_seleccionado = None
        while asistente_1_seleccionado is None:
            try:
                opcion = int(input("\nPrimer asistente seleccionado: "))
                if opcion in range(1, len(asistentes)+1):
                    asistente_1_seleccionado = opcion - 1
                else:
                    print("Error: Seleccione una opción válida.")
            except ValueError:
                print("Error: Ingrese un número entero válido.")
        asistente_2_seleccionado = None
        while asistente_2_seleccionado is None:
            try:
                opcion = int(input("\nSegundo asistente seleccionado: "))
                if opcion in range(1, len(asistentes)+1) and opcion != asistente_1_seleccionado+1:
                    asistente_2_seleccionado = opcion - 1
                else:
                    print("Error: Seleccione una opción válida y diferente al primer asistente.")
            except ValueError:
                print("Error: Ingrese un número entero válido.")
        asistente_1 = asistentes[asistente_1_seleccionado]
        asistente_2 = asistentes[asistente_2_seleccionado]
        turno = Turno(fecha_inicio, fecha_fin, ruta, camion, conductor, asistente_1, asistente_2)
        turnos.append(turno)

    #   Se crea un objeto Invocador y se asocia un comando RecolectarVidrioCommand a cada turno. 
    #   Luego, se ejecuta cada comando y se muestra la cantidad de vidrio recolectado en cada turno

    invocador = Invocador()
    for turno in turnos:
        command = RecolectarVidrioCommand(turno)
        invocador.set_command(command)
        invocador.execute_command()
        print(f"\nLa cantidad de vidrio recolectado en el turno {turnos.index(turno)+1} fue de {command.cantidad}")
    fecha = input("\nIngrese la fecha para calcular la cantidad de vidrio recolectado (YYYY-MM-DD): ")
    fecha = datetime.strptime(fecha, "%Y-%m-%d")
    vidrio_recolectado = calcular_vidrio_recolectado(turnos, fecha)
    print(f"\nLa cantidad de vidrio recolectado en la fecha {fecha.date()} es: {vidrio_recolectado}")

main()