import requests
import ctypes

# URL de la api
api_url = "https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22"

# Obtiene TODOS los datos de la api
def value_get():
    response = requests.get(api_url)
    return response

# Convierte la respuesta en un diccionario de Python y lo retorna
def get_data():
    data = value_get().json()
    return data

# Define el país que desea buscar y lo retorna
def get_country():
    country_to_search = "Argentina"
    return country_to_search

# Inicializa una lista vacía para almacenar los values y otra para almacenar los años
values = []
years = []

# Filtra todos los datos obtenidos con value_get() para obtener solo los del pais que queremos,y a esos los guardamos en una lista que es retornada
def filter_and_fill():
    for item in get_data()[1]:  #data[1] contiene los datos reales, data[0] contiene metadatos
        # Comprueba si el valor del país coincide con el país que se desea buscar
        if item["country"]["value"] == get_country():
            # Si el valor no es None, se añade a la respectiva lista
            if item["value"] is not None:
                values.append(item["value"])
                years.append(item["date"])
    return values  

filter_and_fill()
# Imprime los values
print(values)
print(years)

# Crea una biblioteca de objetos, Dynamic Link Library(DLL), y la retorna
def get_c_library():
    clibrary = ctypes.CDLL("/home/federica/Documents/Sistemas_de_Computacion/practico_2/SistDeCompTP2/libgini.so")    
    #clibrary = ctypes.CDLL("/home/gaston/Documentos/SdC_Proyectos/SistDeCompTP2/libgini.so")
    return clibrary

# Asigna nombre a la funcion de C utilizada
func = get_c_library().CallAssemblyFunction 


# Define el tipo de los argumentos y el valor de retorno de la función
def function_in_c():
    func.argtypes = [ctypes.c_float]
    func.restype = ctypes.c_int
    
function_in_c()

results = []

def call_C_Function():
    for value in values:
        result = func(ctypes.c_float(value))    
        results.append(result)

call_C_Function()
print(results)    