from datetime import datetime
import json

# Archivos Jason para guardar datos
ARCHIVO_EQUIPOS = "equipos_labtech.json"
ARCHIVO_PRESTAMOS = "prestamos_labtech.json"

# Categorias
CATEGORIAS_VALIDAS = ("Laptop", "Adaptador", "Mouse", "Cable HDMI", "Kit basico")

def limpiar_texto(texto):
    return texto.strip()


def validar_texto_no_vacio(texto):
    return len(limpiar_texto(texto)) > 0


def validar_fecha(fecha):
    try:
        datetime.strptime(fecha, "%d/%m/%Y")
        return True
    except ValueError:
        return False


# Funciones de Entrada Reutilizables

def leer_texto(mensaje):
    while True:
        entrada = limpiar_texto(input(mensaje))
        if validar_texto_no_vacio(entrada):
            return entrada
        print("Error: el campo no puede estar vacío.")


def leer_fecha(mensaje):
    while True:
        fecha = limpiar_texto(input(mensaje))
        if validar_texto_no_vacio(fecha) and validar_fecha(fecha):
            return fecha
        print("Error: fecha invalida. Use el formato dd/mm/aaaa (ej. 17/11/2026).")


def seleccionar_categoria():
    print("\nCategorias disponibles:")
    for i, cat in enumerate(CATEGORIAS_VALIDAS, 1):
        print(f"  {i}. {cat}")

    while True:
        opcion = limpiar_texto(input("Seleccione el numero de categoria: "))
        if opcion.isdigit() and 1 <= int(opcion) <= len(CATEGORIAS_VALIDAS):
            return CATEGORIAS_VALIDAS[int(opcion) - 1]
        print("Error: seleccione una opcion valida.")


def buscar_equipo_por_codigo(equipos, codigo):
    codigo_normalizado = limpiar_texto(codigo).upper()
    for equipo in equipos:
        if equipo["codigo"].upper() == codigo_normalizado:
            return equipo
    return None


# Funciones de Persistencia 

def guardar_datos(equipos, prestamos):
    try:
        with open(ARCHIVO_EQUIPOS, "w", encoding="utf-8") as f_eq:
            json.dump(equipos, f_eq, indent=4, ensure_ascii=False)
        with open(ARCHIVO_PRESTAMOS, "w", encoding="utf-8") as f_pr:
            json.dump(prestamos, f_pr, indent=4, ensure_ascii=False)
        return True
    except OSError:
        print("Error: no se pudieron guardar los datos.")
        return False


def cargar_datos():
    equipos = []
    prestamos = []
    try:
        with open(ARCHIVO_EQUIPOS, "r", encoding="utf-8") as f_eq:
            equipos = json.load(f_eq)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        pass

    try:
        with open(ARCHIVO_PRESTAMOS, "r", encoding="utf-8") as f_pr:
            prestamos = json.load(f_pr)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        pass

    return equipos, prestamos