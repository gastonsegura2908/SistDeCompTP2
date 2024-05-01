import requests
import ctypes
import matplotlib
#import _tkinter
#matplotlib.use('TkAgg')
#matplotlib.use('Agg')
import matplotlib.pyplot as plt

from matplotlib.widgets import Button

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
    #clibrary = ctypes.CDLL("/home/federica/Documents/Sistemas_de_Computacion/practico_2/SistDeCompTP2/ctypes/clibrary.so")
    #clibrary = ctypes.CDLL("/home/gaston/Documentos/SdC_Proyectos/SistDeCompTP2/ctypes/clibrary.so")
    #clibrary = ctypes.CDLL("/home/gaston/Documentos/SdC_Proyectos/SistDeCompTP2/ctypes/newclibrary_c.so")
    clibrary = ctypes.CDLL("/home/gaston/Documentos/SdC_Proyectos/SistDeCompTP2/libgini.so")
    return clibrary

# Asigna nombre a la funcion de C utilizada
#func = get_c_library().ChangesArray #PARTE 1
func = get_c_library().CallAssemblyFunction 


# Define el tipo de los argumentos y el valor de retorno de la función
def function_in_c():
    # func.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.c_int]
    # func.restype = ctypes.POINTER(ctypes.c_int)
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
# Crea un array de C de values float a partir de la lista de Python
# def get_values_c():
#     values_c = (ctypes.c_float * len(values))(*values)
#     return values_c

# # Llama a la función de c. new_values_c es un puntero a la memoria que fue asignada en la función CallAssemblyFunction del código de C para almacenar el nuevo array de ints.
# def get_new_values_c():
#     new_values_c = func(get_values_c(), len(values))
#     return new_values_c

# # Convierte el resultado a una lista de Python(un objeto python)
# def get_values_po():
#     values_po = get_new_values_c()[:len(values)]
#     return values_po










# Empareja el orden de los years y los values
#years, valores_po = zip(*sorted(zip(years, get_values_po())))
years, valores_po = zip(*sorted(zip(years, results)))

# Crea una lista de índices para el eje y
#indices = list(range(len(valores_po)))

# Crea una figura con un fondo gris
fig = plt.figure(figsize=(10, 5), facecolor = 'grey')

# Crea el gráfico y lo agrega a la figura
ax = fig.add_axes([0.1, 0.2, 0.8, 0.7])
ax.set_facecolor('white')
ax.grid(True)
ax.plot(years, results, color = 'lightblue', linewidth = 2, linestyle = '-.')
ax.set_title("Cambio de values de GINI - Argentina")
ax.set_ylim(20, 60)

# Etiqueta los ejes
ax.set_xlabel("Año")
ax.set_ylabel("Valor de GINI")

# Ajusta los margenes del grafico
#plt.subplots_adjust(bottom=0.2, right=0.85)

# Calcula la posición del borde izquierdo del botón para centrarlo
def button_position():
    button_left = 0.5 - 0.2 / 2  # 0.5 (mitad de la figura) - 0.2 / 2 (mitad del ancho del botón)
    return button_left

# Crea el botón y lo agrega a la figura
button = fig.add_axes([button_position(), 0.05, 0.2, 0.075])  # Posición y tamaño del botón
btn = Button(button, 'Guardar imagen', color = 'lightblue')

# Función que se ejecutará cuando se presione el botón
def on_button_clicked(event):
    plt.savefig("Cambio_de_valores_de_GIN_Argentina.png")
    print('Imagen guardada!')

# Conecta la función al evento del botón
btn.on_clicked(on_button_clicked)

# Muestra el gráfico
plt.show()

# # Libera memoria. llama a funcion de programa en c.
# get_c_library().free_memory(get_new_values_c()) 
