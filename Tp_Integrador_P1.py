import csv

# =============================================================
# GESTIÓN DE PAÍSES - datos_paises.csv
# =============================================================
# Nota general sobre el manejo de archivos CSV en este programa:
#   - encoding="utf-8" → soporta caracteres especiales como tildes y ñ
#   - newline=""       → evita líneas en blanco extra en Windows
# Estas opciones se aplican en todas las funciones que abren archivos.
# =============================================================

def crear_archivo():
    """
    Crea el archivo datos_paises.csv con los datos iniciales de los países.
 
    Escribe el encabezado (nombre, poblacion, superficie, continente) y
    cuatro países predefinidos usando writelines(), que escribe toda la
    lista de líneas en una sola llamada.
 
    Parámetros: ninguno
    Retorna: ninguno
    """
    with open("datos_paises.csv", "w", newline="", encoding="utf-8") as archivo:
        lista= ["nombre,poblacion,superficie,continente\n",  
                "Argentina,45376763,2780400,América\n",  
                "Japón,125800000,377975,Asia\n",  
                "Brasil,213993437,8515767,América\n", 
                "Alemania,83149300,357022,Europa\n"]
        
        archivo.writelines(lista)
        print("\nLista creada\n")
       
        
#Agrega un pais en la ultima linea. 
def agregar_pais():
    """
    Solicita al usuario los datos de un nuevo país y lo agrega al archivo CSV.
 
    Validaciones aplicadas:
      - nombre y continente: solo letras (se aceptan espacios entre palabras,
        por ejemplo 'Estados Unidos' o 'América del Norte').
      - poblacion y superficie: deben ser enteros positivos.
 
    Usa modo append ('a') para no sobreescribir los datos ya guardados.
 
    Parámetros: ninguno
    Retorna: ninguno
    """
    try:
        with open("datos_paises.csv", "a", newline="", encoding="utf-8") as archivo:
            nombre = input("Ingrese el nombre del pais: ").title()
            continente= input("Ingrese el contintente al que pertenece: ").title()
            
            # Valida que cada palabra del nombre contenga solo letras
            if not all(palabra.isalpha() for palabra in nombre.split()): 
                raise ValueError("Caracter invalido en el nombre")
            # Valida que cada palabra del continente contenga solo letras
            if not all (palabra.isalpha() for palabra in continente.split()): 
                raise ValueError("Caracter invalido en el continente")
            
            poblacion= int(input("Ingrese la cantidad de habitantes: "))
            superficie= int(input("Ingrese la superficie en KM²: "))

            if poblacion <= 0 or superficie <= 0:
                raise ValueError("La población y la superficie deben ser enteros positivos")
            
            linea= f"{nombre},{poblacion},{superficie},{continente}\n"
            archivo.write(linea)
    except FileNotFoundError:
        print("Error: El archivo no existe")
    except ValueError as e:
        print(f"Error: {e}")

#Actualiza los datos de poblacion y superficie. No se puede actualizar el nombre ni el continente.
def actualizar_datos():
    '''Permite actualizar la población y superficie de un país existente en el archivo CSV.
    - Lee todo el archivo en memoria usando csv.DictReader para facilitar la actualización.
    - Solicita el nombre del país a actualizar y valida que exista.
    - Si el país existe, solicita los nuevos valores de población y superficie, validando que sean enteros positivos.
    - Escribe de nuevo todo el archivo con los datos actualizados usando csv.DictWriter.
    Parámetros: ninguno
    Retorna: ninguno
    '''
    
    try:
        with open("datos_paises.csv", "r", newline="", encoding="utf-8") as archivo:
            lector= csv.DictReader(archivo)
            columnas= lector.fieldnames
            filas=list(lector)
        
        nombre_actualizar= input("Ingrese el pais: ").title()
        encontrado=False        

        for fila in filas:
            
            if nombre_actualizar == fila["nombre"]:
                
                poblacio_actualizar= int(input("Ingrese la poblacion: "))
                superficie_actualizar=int(input("Ingrese la superficie en KM²: "))

                if poblacio_actualizar <=0 or superficie_actualizar <=0: 
                    raise ValueError("Ingrese valores enteros positivos")
                # Actualiza solo los campos permitidos; nombre y continente no se modifican
                fila["poblacion"] = poblacio_actualizar
                fila["superficie"] = superficie_actualizar
                encontrado=True
                break
        
        if encontrado == True:
            # Reescribe el archivo completo con los datos actualizados
            with open("datos_paises.csv", "w", newline="", encoding="utf-8") as archivo:
                escritor=csv.DictWriter(archivo, fieldnames=columnas)
                escritor.writeheader() # escribe la línea de encabezado
                escritor.writerows(filas)# escribe todas las filas (incluida la modificada)
        else:
            print("No se ha encontrado el pais para actualizar...")
    except FileNotFoundError: print("Error: El archivo no existe")        
    except ValueError as e: print(f"Error: {e}")

#Buscar paies por nombre completo o parcial
def buscar_pais():
    """
    Busca un país por nombre completo o parcial en el archivo CSV.
 
    Formatea la entrada con title() para mejorar la coincidencia
    (por ejemplo 'argentina' → 'Argentina').
    La búsqueda es parcial: 'Arg' encuentra 'Argentina'.
    Muestra el primer resultado encontrado y detiene la búsqueda.
 
    Parámetros: ninguno
    Retorna: ninguno
    """
    try:
        nombre= input("Ingrese el pais: ").title()
        
        # Acepta nombres compuestos como 'Estados Unidos'
        if not all (palabra.isalpha() for palabra in nombre.split()): 
            raise ValueError("Caracter invalido en el nombre") #Lo cambie para que acepte nombres con espacios como "Estados Unidos"
        
        encontrado=False
        
        with open("datos_paises.csv", "r", newline="", encoding="utf-8") as archivo:
            lector= csv.DictReader(archivo)
            #Búsqueda parcial: verifica si el nombre ingresado está contenido en el campo
            for lista in lector:
                if nombre in lista["nombre"]:
                    print(f"Nombre: {lista["nombre"]} | Poblacion: {lista["poblacion"]} | Superficie: {lista["superficie"]} | Continente: {lista["continente"]}")
                    
                    encontrado=True

                    break
            if not encontrado: print(f"{nombre} no existe en el archivo")

    except FileNotFoundError:print("Error: El archivo no existe")
    except ValueError as e: print(f"Error: {e}")

#Filtra por nombre, poblacion y superficie (ascendente y descendente)
def filtrar():
    """
    Filtra y ordena los países por nombre, población o superficie.
 
    Submenú principal:
      1) Por nombre      → orden alfabético ascendente
      2) Por población   → orden numérico ascendente
      3) Por superficie  → el usuario elige ascendente o descendente
 
    Usa list.sort() con el parámetro key para ordenar sin crear
    una lista nueva. Las funciones auxiliares se definen fuera del
    bloque 'with' para mantener el código organizado.
 
    Parámetros: ninguno
    Retorna: ninguno
    """
    def obtener_nombre(pais):
        return pais["nombre"]
    
    def obtener_poblacion(pais):
        return pais["poblacion"]
    
    def obtener_superficie(pais):
        return pais["superficie"]
    
    """Imprime todos los países de la lista en el formato estándar."""
    def mostrar_paises(paises):
        for pais in paises:
            print(f"Nombre: {pais['nombre']} | Poblacion: {pais['poblacion']} | Superficie: {pais['superficie']} | Continente: {pais['continente']}")
    
    try:
        print("Filtrar")
        print("1)Por Nombre")
        print("2)Por Poblacion")
        print("3)Por Superficie")
        
        filtro= int(input("Opcion: "))
        if filtro <1 or filtro >3: raise ValueError("Valor fuera de rango")
        paises=[]
        with open("datos_paises.csv", "r", newline="", encoding="utf-8") as archivo:
            lector= csv.DictReader(archivo)
            
            for lista in lector:
                datos ={"nombre": lista["nombre"], 
                        "poblacion": int(lista["poblacion"]), 
                        "superficie": int(lista["superficie"]), 
                        "continente": lista["continente"]
                        }
                
                paises.append(datos)

            if filtro == 1:
                paises.sort(key=obtener_nombre)
                mostrar_paises(paises)

            elif filtro == 2:
                paises.sort(key=obtener_poblacion)
                mostrar_paises(paises)

            elif filtro == 3:
                print("1) Ascendente  2) Descendente")
                opciones= int(input("Opcion: "))
                if opciones < 1 or opciones > 2: 
                    raise ValueError("Valor fuera de rango (1 o 2)")
                
                if opciones == 1:
                    paises.sort(key=obtener_superficie)
                    mostrar_paises(paises)

                # reverse=False → de menor a mayor | reverse=True → de mayor a menor
                elif opciones == 2:
                    paises.sort(key=obtener_superficie, reverse=(opciones == 2))
                    mostrar_paises(paises)

    except FileNotFoundError: print("Error: El archivo no existe")    
    except ValueError as e:
        print(f"Error: {e}")

def estadistica():
    '''Permite mostrar estadísticas sobre los países en el archivo CSV, como el país con mayor y menor población.
    - Lee el archivo CSV usando csv.DictReader y almacena los datos en una lista de diccionarios para facilitar el análisis.
    - Inicializa variables para almacenar la población menor y mayor, así como los nombres de los países correspondientes.
    - Recorre la lista de países y compara la población de cada país con las variables de menor y mayor población, actualizando estas variables según sea necesario.
    - Al finalizar el recorrido, muestra el nombre del país con mayor población y el nombre del país con menor población.
    Parámetros: ninguno
    Retorna: ninguno
    '''
    try:
        paises=[]
        with open("datos_paises.csv", "r", newline="", encoding="utf-8") as archivo:
            lector= csv.DictReader(archivo)
            for lista in lector:
                for lista in lector:
                    datos ={"nombre": lista["nombre"], "poblacion": int(lista["poblacion"]), "superficie": int(lista["superficie"]), "continente": lista["continente"]}
                    paises.append(datos)
            
            menor=8300000000
            mayor = 0
            nombre_menor, nombre_mayor=""

            for pais in paises:
                poblacion = pais["poblacion"]
                
                if poblacion < menor:
                    menor = poblacion
                    nombre_menor = pais["nombre"]
                
                if poblacion> mayor:
                    mayor = poblacion
                    nombre_mayor = pais["nombre"]

    except FileNotFoundError: print("Error: El archivo no existe")         
    
    print("")
    print("Pais con mayor poblacion")
    print("")


opcion=0
while opcion != 7:

    '''Muestra el menú principal y solicita al usuario que seleccione una opción.
    - El menú incluye opciones para crear la lista, agregar un país, actualizar datos, buscar un país, filtrar los países, mostrar estadísticas y salir del programa.
    - Valida que la opción ingresada sea un número entero entre 1 y 7, mostrando un mensaje de error si el valor es inválido.
    - Llama a la función correspondiente según la opción seleccionada por el usuario.
    Parámetros: ninguno
    Retorna: ninguno
     '''
  
    print("=" * 10 + "| Menu Principal | " + "=" * 10)
    print("1) Crear Lista\n2) Agregar un País\n3) Actualizar Datos\n4) Buscar\n5) Filtrar\n6) Estadísticas\n7) Salir")
    print("="*39)
    try:
        opcion = int(input("Ingrese una opción: "))
        if opcion<=0 or opcion >7: raise ValueError("Valor fuera de rango")
        if opcion==1: crear_archivo()
        elif opcion==2: agregar_pais()
        elif opcion==3: actualizar_datos()
        elif opcion==4: buscar_pais()
        elif opcion==5: filtrar()
    except ValueError as e:
        print(f"Error: {e}")

input("\nPrograma finalizado... presione Enter para Finalizar")