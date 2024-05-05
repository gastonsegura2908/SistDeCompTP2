# Sistemas de Computacion
Repositorio destinado al trabajo práctico #2 de la parte practica de la materia Sistemas de Computación.  
### GRUPO: The Tux Titans
### INTEGRANTES : 
- Federica Mayorga
- Gaston Marcelo Segura
- Lourdes Guyot

---
### Consigna:

Se debe diseñar e implementar una interfaz que muestre el índice GINI. La capa superior recuperará la información del banco mundial [API WorldBank](https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22). Se recomienda el uso de API Rest y Python. Los datos de consulta realizados deben ser entregados a un programa en C (capa intermedia) que convocará rutinas en ensamblador para que hagan los cálculos de conversión de float a enteros y devuelva el índice de un país como Argentina u otro sumando uno (+1). Luego el programa en C o Python mostrará los datos obtenidos.

Se debe utilizar el stack para convocar, enviar parámetros y devolver resultados. O sea utilizar las convenciones de llamadas de lenguajes de alto nivel a bajo nivel.

En una primera iteración se resolverá todo el trabajo práctico usando C con Python sin ensamblador. En la siguiente iteración usarán los conocimientos de ensamblador para completar el TP.

**IMPORTANTE: En esta segunda iteración deberán mostrar los resultados con gdb, para ello pueden usar un programa de C puro. Cuando depuren muestran el estado del área de memoria que contiene el stack antes, durante y después de la función.**

***Casos de prueba, diagramas de bloques, diagrama de secuencia, pruebas de performance para comparar C y Python son bienvenidos, profiling de la app de C es un plus.***

---
### Breve introducción

Para este desarrollo utilizamos las bibliotecas .so, también conocidas como bibliotecas compartidas. Son similares a las bibliotecas DLL en Windows. Se llaman "compartidas" porque varios programas pueden usarlas al mismo tiempo. Esto significa que pueden contener código y datos que varios programas utilizan simultáneamente, lo que ayuda a ahorrar recursos del sistema. Las bibliotecas .so se cargan en tiempo de ejecución, a diferencia de las bibliotecas estáticas (.a) que se incluyen en el programa en el momento de la compilación.

### Primera iteración

Para la primer iteración del trabajo, se observa en terminal:

![Salida por terminal de la primer iteración.](https://github.com/FedericaMayorga01/SistDeCompTP2/assets/131220584/26dabf06-f34e-444d-a753-67dd00f1eeef)


Salida por terminal de la primer iteración.

El comando `gcc -shared -o clibrary.so clibrary.c` es usado para compilar un archivo de código en C (`clibrary.c`) en una biblioteca compartida (`clibrary.so`).

- `gcc`: Es el compilador de GNU para el lenguaje C.
- `shared`: Esta opción le indica al compilador que genere una biblioteca compartida en lugar de un ejecutable.
- `o clibrary.so`: La opción `o` se usa para especificar el nombre del archivo de salida, que en este caso es `clibrary.so`.
- `clibrary.c`: Este es el archivo de entrada, el código en C que se va a compilar.

Esto genera en pantalla, utilizando Python como interfaz, una gráfica de los valores GINI de la API que pertenecen al archivo JSON, con la palabra clave "Argentina".

![Interfaz grafica para la primer iteración.](https://github.com/FedericaMayorga01/SistDeCompTP2/assets/131220584/90139278-80ba-42c6-bf17-eb2960cb17f3)

Los puntos representados en la gráfica (de color celeste, por la bandera de Argentina), se procesan como se ve en la primera imagen de la terminal. Se transforman de float a integer y se incrementan en uno. Luego se reorganizan por año, para que al representarlos en la gráfica, sean cronológicos.

Como añadidido, la interfaz grafica posee un boton mediante el cual, al presionarlo, se puede almacenar el grafico obtenido. El mismo se guarda en la raiz del proyecto.
![grafico almacenado](https://)  

```
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/*
    Esta funcion transforma de tipo float a tipo int y le suma 1 
    a cada elemento de la array proveniente del codigo en python 
    @param arr :arreglo con los indices gini
    @param size :tamaño del arreglo
*/
int* ChangesArray(float *arr,int size){
    int* array_int = malloc(size * sizeof(int));
    for(int i=0;i<size;i++){
        array_int[i]=(int)arr[i];
        array_int[i]++;
    }
    return array_int;
}

void free_memory(int *arr){
    free(arr);
}
```
Código de la primer iteración en C.

Este código C define dos funciones:

1. `ChangesArray(float *arr,int size)`: Esta función toma un arreglo de números en punto flotante y su tamaño. Convierte cada número del arreglo a un entero y le suma uno. Devuelve el nuevo arreglo de enteros.
2. `free_memory(int *arr)`: Esta función libera la memoria que fue previamente reservada para un arreglo de enteros.

TESTS:  
Se realizan utilizando pytest, el cual es un marco de pruebas que permite a los usuarios escribir códigos de prueba utilizando el lenguaje de programación Python. Se coloca `python -m pytest` en la terminal, para ejecutar el codigo que se encuentra en el programa llamado test_MainProcess.py. En el mismo se realizan 4 pruebas:

1. `test_value_get()`: testea si se pudieron obtener correctamente los datos provenientes de la api,utilizando el comando request. Si efectivamente devuelve 200 es porque la solicitud se completo con exito.
2. `test_get_country()`: testea si se ingreso correctamente Argentina como pais para obtener los datos del indice GINI.
3. `test_button_position()`: testea si efectivamente la posicion que se calcula del boton es un numero mayor a 0.
4. `test_pre_post_c_function()`: testea si la lista que contiene los valores de los indices GINI tiene un tamaño mayor a 0.
  
Al ejecutar el comando `python -m pytest` :  
![tests](https://)  
Se puede observar que los cuatro tests han pasado con exito.

### Segunda iteración

Para la segunda iteración del trabajo, se observa en terminal:
![Comandos para la segunda iteración por terminal.](https://github.com/FedericaMayorga01/SistDeCompTP2/assets/131220584/d69c9e65-47bf-4a62-8da9-2d7462884248)

Estos comandos en la terminal realizan las siguientes acciones:

- `gcc -c -m32 -Wall Werror -fPIC newclibrery.c -o newclibrary_c.o`: Compila el archivo de código C `newclibrary.c` en un archivo de objeto `newclibrary_c.o` utilizando las opciones especificadas: `c` para compilar o ensamblar el código fuente sin enlazar, `m32` para generar código para una arquitectura de 32 bits, `Wall` para habilitar todos los mensajes de advertencia, `Werror` para tratar todas las advertencias como errores, y `fPIC` para generar código de posición independiente.
- `nasm -f elf32 assemblycode.ase -o aseemblycode_asm.o`: Compila el archivo de código de ensamblador `assemblycode.ase` en un archivo de objeto `assemblycode_asm.o` utilizando el formato `elf32`.
- `gcc -m32 -shared -o libgini.so ./assembler/assemblycode_asm.o ./ctypes/nreclibrary_c.o`: Enlaza los archivos de objeto `assemblycode_asm.o` y `newclibrary_c.o` en una biblioteca compartida `libgini.so` utilizando las opciones especificadas: `m32` para generar código para una arquitectura de 32 bits y `shared` para crear una biblioteca compartida.

Para activar el entorno virtual de Python, utilizando los siguientes comandos:
![Comandos para activar el entorno virtual de Python 32b en terminal.](https://github.com/FedericaMayorga01/SistDeCompTP2/assets/131220584/de08e997-ee36-4645-99ad-e31013bb0386)

Por problemas no resueltos con el módulo 'matplotlib', se continúa con la segunda iteración sin usar este módulo. Además, no es necesario el uso de la interfaz gráfica. Centrándonos solo en el desarrollo y depuración en gdb.
Realizando las modificaciones en el código, para lograr este avance, obtenemos en terminal:
![Comandos exitosos de activación del entorno virtual de Python 32b en terminal.](https://github.com/FedericaMayorga01/SistDeCompTP2/assets/131220584/7662cbb1-fdd2-49a4-bdb3-47816ef17c54)


```
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Prototipo de la función en ensamblador
extern int ChangesArray(float gini_index);

// Función en C que se comunica con Python y llama a la función en ensamblador
int CallAssemblyFunction(float gini_index) {
    // Llamar a la función en ensamblador

    return ChangesArray(gini_index);
}
```
Código de la segunda iteración en C.

Este código en C define una función que se conecta con una función en lenguaje ensamblador.

1. `CallAssemblyFunction(float gini_index)` toma un índice GINI (un número de punto flotante) como argumento. Luego, llama a la función `ChangesArray(float gini_index)`, que está escrita en ensamblador.

El propósito de este código es permitir una interacción entre un programa en C y una función en ensamblador, lo que permite realizar operaciones específicas de bajo nivel en el índice GINI.
