from utilidades import (
    CATEGORIAS_VALIDAS,
    limpiar_texto,
    validar_texto_no_vacio,
    leer_texto,
    leer_fecha,
    seleccionar_categoria,
    buscar_equipo_por_codigo,
    guardar_datos,
    cargar_datos
)


# 1. Registrar equipo disponible
def registrar_equipo(equipos, prestamos):
    print("\n------- REGISTRAR NUEVO EQUIPO -------")
    codigo = leer_texto("Codigo del equipo (ej. LAP-01): ").upper()

    if buscar_equipo_por_codigo(equipos, codigo) is not None:
        print(f"Error: ya existe un equipo registrado con el codigo '{codigo}'.")
        return

    nombre = leer_texto("Nombre o descripcion del equipo: ")
    categoria = seleccionar_categoria()

    nuevo_equipo = {
        "codigo": codigo,
        "nombre": nombre,
        "categoria": categoria,
        "estado": "Disponible"  # Todo equipo ingresa como disponible por defecto
    }

    equipos.append(nuevo_equipo)
    guardar_datos(equipos, prestamos)
    print(f"\nEquipo '{nombre}' ({codigo}) registrado correctamente como Disponible.")


# 2. Registrar un prestamo
def registrar_prestamo(equipos, prestamos):
    print("\n------- REGISTRAR PRESTAMO DE EQUIPO -------")
    if not equipos:
        print("No hay equipos registrados en el laboratorio.")
        return

    codigo = leer_texto("Ingrese el código del equipo a prestar: ").upper()
    equipo = buscar_equipo_por_codigo(equipos, codigo)

    # Requisito 3: Validar que el codigo exista
    if equipo is None:
        print(f"Error: el codigo '{codigo}' no existe en el inventario.")
        return

    # Requisito 4: Validar que este disponible
    if equipo["estado"] != "Disponible":
        print(f"Error: el equipo '{equipo['nombre']}' ({codigo}) esta marcado como No disponible.")
        return

    estudiante = leer_texto("Nombre completo del estudiante: ")
    fecha = leer_fecha("Fecha de prestamo (dd/mm/aaaa): ")

    # Actualizar estado del equipo y registrar el prestamo
    equipo["estado"] = "No disponible"
    nuevo_prestamo = {
        "codigo_equipo": equipo["codigo"],
        "nombre_equipo": equipo["nombre"],
        "estudiante": estudiante,
        "fecha_prestamo": fecha,
        "fecha_devolucion": None,
        "activo": True
    }

    prestamos.append(nuevo_prestamo)
    guardar_datos(equipos, prestamos)
    print(f"\nPrestamo exitoso: '{equipo['nombre']}' asignado a {estudiante} ({fecha}).")


# 3. Devolver equipo
def devolver_equipo(equipos, prestamos):
    print("\n------- DEVOLVER EQUIPO -------")
    if not equipos:
        print("No hay equipos registrados.")
        return

    codigo = leer_texto("Ingrese el codigo del equipo a devolver: ").upper()
    equipo = buscar_equipo_por_codigo(equipos, codigo)

    if equipo is None:
        print(f"Error: el codigo '{codigo}' no existe en el inventario.")
        return

    if equipo["estado"] == "Disponible":
        print(f"Aviso: el equipo '{equipo['nombre']}' ({codigo}) ya figura como Disponible.")
        return

    fecha_dev = leer_fecha("Fecha de devolucion (dd/mm/aaaa): ")
    equipo["estado"] = "Disponible"

    # Buscar el prestamo activo asociado para cerrarlo
    for prestamo in prestamos:
        if prestamo["codigo_equipo"] == equipo["codigo"] and prestamo["activo"]:
            prestamo["activo"] = False
            prestamo["fecha_devolucion"] = fecha_dev
            break

    guardar_datos(equipos, prestamos)
    print(f"\nDevolucion registrada: '{equipo['nombre']}' ({codigo}) vuelve a estar Disponible.")


# 4. Listar disponibilidad
def listar_disponibilidad(equipos):
    print("\n------- INVENTARIO Y DISPONIBILIDAD LABTECH -------")
    if not equipos:
        print("No hay equipos registrados aun.")
        return

    print(f"{'CODIGO':<10} | {'NOMBRE':<25} | {'CATEGORIA':<14} | {'ESTADO'}")
    print("-" * 68)
    for eq in equipos:
        print(f"{eq['codigo']:<10} | {eq['nombre']:<25} | {eq['categoria']:<14} | {eq['estado']}")

    disponibles = sum(1 for eq in equipos if eq["estado"] == "Disponible")
    print("-" * 68)
    print(f"Total equipos: {len(equipos)} | Disponibles: {disponibles} | Prestados: {len(equipos) - disponibles}")


# 5. Consultar cantidad de equipos disponibles por categoria
def consultar_disponibles_por_categoria(equipos):
    print("\n------- DISPONIBILIDAD POR CATEGORIA -------")
    if not equipos:
        print("No hay equipos registrados.")
        return

    for categoria in CATEGORIAS_VALIDAS:
        cantidad = sum(
            1 for eq in equipos
            if eq["categoria"] == categoria and eq["estado"] == "Disponible"
        )
        print(f"- {categoria:<15}: {cantidad} disponible(s)")


# 6. Mostrar menu principal
def mostrar_menu():
    """Despliega las opciones principales de la consola."""
    print("\n========== SISTEMA DE PRESTAMOS LABTECH ==========")
    print("1. Registrar equipo")
    print("2. Registrar prestamo")
    print("3. Devolver equipo")
    print("4. Listar disponibilidad general")
    print("5. Consultar disponibles por categoría")
    print("6. Salir")


def main():
    """Funcion coordinadora del flujo principal del programa."""
    equipos, prestamos = cargar_datos()
    print(f"Sistema LabTech iniciado. Equipos cargados: {len(equipos)}.")

    while True:
        mostrar_menu()
        opcion = limpiar_texto(input("\nSeleccione una opcion (1-6): "))

        # Reutilizacion directa de validar_texto_no_vacio en el menu principal
        if not validar_texto_no_vacio(opcion):
            print("Error: debe ingresar una opcion.")
            continue

        if opcion == "1":
            registrar_equipo(equipos, prestamos)
        elif opcion == "2":
            registrar_prestamo(equipos, prestamos)
        elif opcion == "3":
            devolver_equipo(equipos, prestamos)
        elif opcion == "4":
            listar_disponibilidad(equipos)
        elif opcion == "5":
            consultar_disponibles_por_categoria(equipos)
        elif opcion == "6":
            guardar_datos(equipos, prestamos)
            print("Datos guardados. Cerrando sistema LabTech...")
            break
        else:
            print("Error: opcion invalida. Elija un numero del 1 al 6.")


if __name__ == "__main__":
    main()