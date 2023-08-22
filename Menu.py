from tabulate import tabulate
print("======================================================")
print("* Practica 1 - Lenguajes formales y de programación *")
print("======================================================\n")

#Crear el nodo y lista enlazada
class NodoProducto:
    def __init__(self, nombre, cantidad, precio, ubicacion):
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio
        self.ubicacion = ubicacion
        self.siguiente = None

class ListaEnlazadaProductos:
    def __init__(self):
        self.cabeza = None
    def agregar(self, nombre, cantidad, precio, ubicacion):
        nuevo_producto = NodoProducto(nombre, cantidad, precio, ubicacion)
        if not self.cabeza:
            self.cabeza = nuevo_producto
            print("Se ingreso al inventario: ", cantidad," ", nombre, "en la ubicacion ", ubicacion )
            return
        actual = self.cabeza
        while actual.siguiente:
            actual = actual.siguiente
        actual.siguiente = nuevo_producto
        print("Se ingreso al inventario: ", cantidad," ", nombre, "en la ubicacion ", ubicacion )
#Funcion para ver como se estaba ingresando la lista 
    def mostrar(self):
        actual = self.cabeza
        while actual:
            print(f"Nombre: {actual.nombre}, Cantidad: {actual.cantidad}, Precio: {actual.precio}, Ubicación: {actual.ubicacion}")
            actual = actual.siguiente
    def __str__(self) -> str:
        pass

# Métodos para agregar y vender productos
    def buscar_producto(self, nombre):
        actual = self.cabeza
        while actual:
            if actual.nombre == nombre:
                return actual
            actual = actual.siguiente
        return None

    def agregar_stock(self, nombre, cantidad_a_agregar, ubicacion_nueva):
        producto = self.buscar_producto(nombre)
        if producto:
            producto.cantidad += cantidad_a_agregar
            producto.ubicacion = ubicacion_nueva
            print("Se agregaron ", cantidad_a_agregar, " ", nombre, " en la ", ubicacion_nueva, ".")
        else:
            print("Producto no encontrado.")

    def vender_producto(self, nombre, cantidad_a_vender, verificar_ubi):
        producto = self.buscar_producto(nombre)
        if producto:
            if producto.cantidad >= cantidad_a_vender and producto.ubicacion == verificar_ubi:
                producto.cantidad = producto.cantidad -cantidad_a_vender
                print("Se vendieron ", cantidad_a_vender, " ", nombre, " en la ", verificar_ubi, ".")
            else:
                print("No hay suficiente stock para la venta.")
        else:
            print("Producto no encontrado.")        

#Leer el archivo.inv y crear los primeros datos.
def leer_datos_desde_archivo(archivo, lista):
    try:
        with open(archivo, "r", encoding="UTF-8") as archivo:
            lineas = archivo.readlines()
        for linea_num, linea in enumerate(lineas, start=1):
            datos = linea.strip().split(";")
            if len(datos) != 4:
                print(f"Error en la línea {linea_num}: Formato incorrecto")
                continue
            nombre, cantidad, precio, ubicacion = datos
            try:
                nombre = str(nombre).strip("crear_producto ")
                cantidad = int(cantidad)
                precio = float(precio)
            except ValueError:
                print(f"Error en la línea {linea_num}: Datos numéricos inválidos")
                continue

            lista.agregar(nombre, cantidad, precio, ubicacion)
    except FileNotFoundError:
        print(f"El archivo '{archivo}' no fue encontrado")
    except Exception as e:
        print(f"Error durante la lectura del archivo: {e}")

#Metodo para actualizar el inventario
def Actualizar_datos(archivo, lista):
    try:
        with open(archivo, "r", encoding="UTF-8") as archivo_lectura:
            lineas = archivo_lectura.readlines()
        for linea_num, linea in enumerate(lineas, start=1):
            datos = linea.replace(" ", ";").split(";")
            if len(datos) != 4:
                print(f"Error en la línea {linea_num}: Formato incorrecto")
                continue
            accion, nombre, cantidad, ubicacion = datos
            try:
                cantidad = int(cantidad)
            except ValueError:
                print(f"Error en la línea {linea_num}: Cantidad inválida")
                continue
            if accion == "agregar_stock":
                lista.agregar_stock(nombre, cantidad, ubicacion) 
            elif accion == "vender_producto":
                lista.vender_producto(nombre, cantidad, ubicacion) 
            else:
                print(f"Acción no reconocida en la línea {linea_num}") 
    except FileNotFoundError:
        print(f"El archivo '{archivo}' no fue encontrado")
    except Exception as e:
        print(f"Error durante la lectura del archivo: {e}")
       

def mostrar_menu():
    print("============ SISTEMA DE INVENTARIO ============")
    print("| |1|   Cargar inventario inicial             |")
    print("| |2|   Cargar instrucciones de movimientos   |")
    print("| |3|   Crear informe de inventario           |")
    print("| |4|   Salir                                 |")
    print("===============================================")
lista_productos = ListaEnlazadaProductos()

def Generar_reporte():
    datos_tabulados = []
    actual = lista_productos.cabeza
    while actual:
        precio_total = float(actual.cantidad*actual.precio)
        datos_tabulados.append([actual.nombre, actual.cantidad, actual.precio,precio_total, actual.ubicacion])
        actual = actual.siguiente
    encabezados = ["NOMBRE", "CANTIDAD", "PRECIO","VALOR TOTAL", "UBICACIÓN"]
    tabla = tabulate(datos_tabulados, headers=encabezados, tablefmt="grid")
    nombre_archivo = "Resultados_201901403.txt"
    with open(nombre_archivo, "w", encoding="UTF-8") as archivo:
        archivo.write("Informe del Inventario: \n")
        archivo.write(tabla)

while True:
    mostrar_menu()
    opcion = input("Seleccione una opción (1/2/3) o 4 para salir: ")
    if opcion == "1":
        #Ingresar el nombre del archivo .inv
        leer_datos_desde_archivo("inventario.inv", lista_productos)
    elif opcion == "2":
        #Ingresar el nombre del archivo .mov
        Actualizar_datos("movimientos.mov", lista_productos)
    elif opcion == "3":
        Generar_reporte()
        print("\nSe ha Generaro el reporte exitosamente\n")
    elif opcion == "4":
        print("\nSaliendo del programa...")
        break
    else:
        print("Opción inválida. Por favor, seleccione una opción válida.")