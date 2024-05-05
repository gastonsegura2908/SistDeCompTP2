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
Interfaz grafica para la primer iteración.

Los puntos representados en la gráfica (de color celeste, por la bandera de Argentina), se procesan como se ve en la primera imagen de la terminal. Se transforman de float a integer y se incrementan en uno. Luego se reorganizan por año, para que al representarlos en la gráfica, sean cronológicos.

Como añadidido, la interfaz grafica posee un boton que, al presionarlo, permite almacenar el grafico obtenido. El mismo se guarda en la raiz del proyecto.
![Grafico almacenado.](https://github.com/FedericaMayorga01/SistDeCompTP2/assets/131220584/07d553d8-5219-4e12-9f9f-ef6e15f1b858)
Grafico almacenado.




```C
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

---
### Test

Se realizan utilizando pytest, el cual es un marco de pruebas que permite a los usuarios escribir códigos de prueba utilizando el lenguaje de programación Python. Se coloca `python -m pytest` en la terminal, para ejecutar el codigo que se encuentra en el programa llamado test_MainProcess.py. En el mismo se realizan 4 pruebas:

1. `test_value_get()`: testea si se pudieron obtener correctamente los datos provenientes de la api,utilizando el comando request. Si efectivamente devuelve 200 es porque la solicitud se completo con exito.
2. `test_get_country()`: testea si se ingreso correctamente Argentina como pais para obtener los datos del indice GINI.
3. `test_button_position()`: testea si efectivamente la posicion que se calcula del boton es un numero mayor a 0.
4. `test_pre_post_c_function()`: testea si la lista que contiene los valores de los indices GINI tiene un tamaño mayor a 0.
  
Al ejecutar el comando `python -m pytest` :  
![Test.](https://github.com/FedericaMayorga01/SistDeCompTP2/assets/131220584/954db504-9126-4449-802a-91af5c5e7328)

Se puede observar que los cuatro tests han pasado con exito.

---
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


```C
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

El codigo en `Assembly`:
```asm
section .text
    global ChangesArray   

ChangesArray:
    ; Start 
    push ebp                        
    mov ebp, esp                    

    ; Convert float to int
    fld dword [ebp+8]               
    fistp dword [ebp-4]             

    ; Add 1 to the integer
    mov eax, dword [ebp-4]         
    add eax, 1                      

    ; Exit
    mov esp, ebp                    
    pop ebp                         
    ret
```
Código en Assembly para la segunda iteración.

Este es un código en lenguaje ensamblador que define una función llamada `ChangesArray`. 
1. **`section .text`**: Esta línea indica que el código que sigue es el código del programa, es decir, las instrucciones que la CPU ejecutará.
2. **`global ChangesArray`**: Esta línea hace que la función **`ChangesArray`** sea visible para otros archivos. Esto es útil cuando se enlazan varios archivos de ensamblador juntos.
3. **`push ebp`** y **`mov ebp, esp`**: Estas dos líneas son un patrón común al comienzo de una función. Guardan el puntero de pila actual (**`esp`**) en **`ebp`**. Esto se hace para que **`ebp`** pueda usarse para acceder a los argumentos de la función y a las variables locales.
4. **`fld dword [ebp+8]`** y **`fistp dword [ebp-4]`**: Estas dos líneas convierten un número de punto flotante a un número entero. **`fld`** carga el argumento de la función (que es un número de punto flotante) en la pila de la FPU (Floating Point Unit). Luego, **`fistp`** convierte el número de punto flotante en la cima de la pila de la FPU a un número entero y lo almacena en la variable local en **`[ebp-4]`**.
5. **`mov eax, dword [ebp-4]`** y **`add eax, 1`**: Estas dos líneas incrementan el número entero por 1. **`mov`** carga el número entero en el registro **`eax`**, y luego **`add`** incrementa el valor en **`eax`** por 1.
6. **`mov esp, ebp`** y **`pop ebp`**: Estas dos líneas son un patrón común al final de una función. Restauran el puntero de pila (**`esp`**) y el puntero de base (**`ebp`**) a sus valores antes de la llamada a la función. Esto se hace para limpiar la pila antes de retornar de la función.
7. **`ret`**: Esta línea es la instrucción de retorno. Hace que la función retorne al código que la llamó.



Para poder depurar el codigo, se agrega una parte de _debug_ para hacer un simple seguimiento sobre el _stackframe_. 
![Agregado de debugeo.](https://github.com/FedericaMayorga01/SistDeCompTP2/assets/131220584/77a3c416-d297-4b1f-89e7-185a22d8ba01)
Agregado de debugeo.

Este es su resultado por terminal de la depuración con gdb:
```asm
Reading symbols from debug...
(gdb) break main
Breakpoint 1 at 0x11ca: file debug.c, line 5.
(gdb) run
Starting program: /home/federica/Documents/Sistemas_de_Computacion/practico_2/SistDeCompTP2/debug/debug 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".

Breakpoint 1, main () at debug.c:5
5       int main(){
(gdb) next
6           float gini_values[5] = {0.1, 0.2, 0.3, 0.4, 0.5};
(gdb) x/4x $sp
0xffffc8f0:     0xf7fbe4a0      0xf7fd6f20      0xf7d914be      0xf7fbe4a0
(gdb) next
7           for(int i = 0; i < 5; i++) {
(gdb) x/4x $sp
0xffffc8f0:     0xf7fbe4a0      0xf7fd6f20      0x3dcccccd      0x3e4ccccd
(gdb) next
8               int result = ChangesArray(gini_values[i]);
(gdb) x/4x $sp
0xffffc8f0:     0x00000000      0xf7fd6f20      0x3dcccccd      0x3e4ccccd
(gdb) next
9               printf("ChangesArray returned %d for input %f\n", result, gini_values[i]);
(gdb) x/4x $sp
0xffffc8f0:     0x00000000      0x00000001      0x3dcccccd      0x3e4ccccd
(gdb) next
ChangesArray returned 1 for input 0.100000
7           for(int i = 0; i < 5; i++) {
(gdb) next
8               int result = ChangesArray(gini_values[i]);
(gdb) x/4x $sp
0xffffc8f0:     0x00000001      0x00000001      0x3dcccccd      0x3e4ccccd
(gdb) next
9               printf("ChangesArray returned %d for input %f\n", result, gini_values[i]);
(gdb) next
ChangesArray returned 1 for input 0.200000
7           for(int i = 0; i < 5; i++) {
(gdb) next
8               int result = ChangesArray(gini_values[i]);
(gdb) x/4x $sp
0xffffc8f0:     0x00000002      0x00000001      0x3dcccccd      0x3e4ccccd
(gdb) next
9               printf("ChangesArray returned %d for input %f\n", result, gini_values[i]);
(gdb) next
ChangesArray returned 1 for input 0.300000
7           for(int i = 0; i < 5; i++) {
(gdb) next
8               int result = ChangesArray(gini_values[i]);
(gdb) x/4x $sp
0xffffc8f0:     0x00000003      0x00000001      0x3dcccccd      0x3e4ccccd
(gdb) next
9               printf("ChangesArray returned %d for input %f\n", result, gini_values[i]);
(gdb) next
ChangesArray returned 1 for input 0.400000
7           for(int i = 0; i < 5; i++) {
(gdb) next
8               int result = ChangesArray(gini_values[i]);
(gdb) x/4x $sp
0xffffc8f0:     0x00000004      0x00000001      0x3dcccccd      0x3e4ccccd
(gdb) next
9               printf("ChangesArray returned %d for input %f\n", result, gini_values[i]);
(gdb) next
ChangesArray returned 1 for input 0.500000
7           for(int i = 0; i < 5; i++) {
(gdb) next
11          return 0;
(gdb) x/4x $sp
0xffffc8f0:     0x00000005      0x00000001      0x3dcccccd      0x3e4ccccd
(gdb) next
12      }
(gdb) continue
```

Estos comandos en la terminal de gdb realizan las siguientes acciones:
1. **`gdb -q debug`**: Este comando inicia GDB con el programa **`debug`** en modo silencioso (la opción **`q`** significa “quiet”).
2. **`break main`**: Este comando establece un punto de interrupción en la función **`main`**.
3. **`run`**: Este comando inicia la ejecución del programa. El programa se detiene en el primer punto de interrupción, que es la función **`main`**.
4. **`next`**: Este comando ejecuta la siguiente línea de código. En este caso, ejecuta la línea 6, que inicializa el array **`gini_values`**.
5. **`x/4x $sp`**: Este comando examina 4 palabras de memoria en formato hexadecimal a partir de la dirección apuntada por el puntero de pila (**`$sp`**).

Vemos cómo los valores del _stackframe_ cambian a medida que se pasan los `gini_values` como parámetro. De esta forma, confirmamos el uso correcto del puntero `sp` y del _stackframe_. Los valores se muestran en el orden en que están en la memoria, comenzando desde la dirección apuntada por `$sp` y continuando hacia direcciones de memoria más altas. En otras palabras, el primer valor es el contenido de la memoria en la dirección `$sp`, el segundo valor es el contenido de la memoria en la dirección `$sp + 1 * tamaño_de_palabra`, y así sucesivamente.



```asm
Reading symbols from debug...
(gdb) break main
Breakpoint 1 at 0x11ca: file debug.c, line 5.
(gdb) run
Starting program: /home/federica/Documents/Sistemas_de_Computacion/practico_2/SistDeCompTP2/debug/debug 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".

Breakpoint 1, main () at debug.c:5
5       int main(){
(gdb) disassemble main
Dump of assembler code for function main:
   0x565561ad <+0>:     lea    0x4(%esp),%ecx
   0x565561b1 <+4>:     and    $0xfffffff0,%esp
   0x565561b4 <+7>:     push   -0x4(%ecx)
   0x565561b7 <+10>:    push   %ebp
   0x565561b8 <+11>:    mov    %esp,%ebp
   0x565561ba <+13>:    push   %ebx
   0x565561bb <+14>:    push   %ecx
   0x565561bc <+15>:    sub    $0x20,%esp
   0x565561bf <+18>:    call   0x565560b0 <__x86.get_pc_thunk.bx>
   0x565561c4 <+23>:    add    $0x2e10,%ebx
	 0x565561ca <+29>:    mov    %gs:0x14,%eax
   0x565561d0 <+35>:    mov    %eax,-0xc(%ebp)
	 ...
   0x56556270 <+195>:   ret    
End of assembler dump.
```
Vemos en esta parte, los primero movimiento del stack en `assembler`.

1. **`lea 0x4(%esp),%ecx`**: Este comando carga la dirección de **`esp + 4`** en el registro **`ecx`**. **`lea`** significa “load effective address”.
2. **`and $0xfffffff0,%esp`**: Este comando realiza una operación AND bit a bit en **`esp`** y **`0xfffffff0`**, y almacena el resultado en **`esp`**. Esto se utiliza a menudo para alinear **`esp`** a un límite de 16 bytes.
3. **`push -0x4(%ecx)`**: Este comando empuja el valor en la dirección **`ecx - 4`** en la pila.
4. **`push %ebp`**: Este comando empuja el valor de **`ebp`** en la pila.
5. **`mov %esp,%ebp`**: Este comando mueve el valor de **`esp`** a **`ebp`**. Esto se hace a menudo al comienzo de una función para establecer un nuevo marco de pila.
6. **`push %ebx`**: Este comando empuja el valor de **`ebx`** en la pila.
7. **`push %ecx`**: Este comando empuja el valor de **`ecx`** en la pila.
8. **`sub $0x20,%esp`**: Este comando resta **`0x20`** de **`esp`**, efectivamente reservando **`0x20`** bytes de espacio en la pila.
9. **`call 0x565560b0 <__x86.get_pc_thunk.bx>`**: Este comando llama a la función en la dirección **`0x565560b0`**. Esta función es probablemente una función de thunk que se utiliza para obtener el contador de programa actual.
10. **`add $0x2e10,%ebx`**: Este comando suma **`0x2e10`** a **`ebx`**.
11. **`mov %gs:0x14,%eax`**: Este comando mueve el valor en la dirección **`0x14`** del segmento **`gs`** a **`eax`**. Esto se utiliza a menudo para acceder a datos específicos del hilo en sistemas operativos multihilo.
12. **`mov %eax,-0xc(%ebp)`**: Este comando mueve el valor de **`eax`** a la dirección **`ebp - 0xc`**.

Una instrucción muy útil es `info registers`:
```asm
(gdb) info registers
eax            0x565561ad          1448436141
ecx            0xffffc930          -14032
edx            0xffffc950          -14000
ebx            0x56558fd4          1448447956
esp            0xffffc8f0          0xffffc8f0
ebp            0xffffc918          0xffffc918
esi            0xffffc9e4          -13852
edi            0xf7ffcb80          -134231168
eip            0x565561ca          0x565561ca <main+29>
eflags         0x206               [ PF IF ]
cs             0x23                35
ss             0x2b                43
ds             0x2b                43
es             0x2b                43
fs             0x0                 0
gs             0x63                99
(gdb) nexti
0x565561d0      5       int main(){
```
Sección de codigo en Assembly que muestra información de los registros.

Con la instrucción `info registers` podemos ver los registros del procesador. En la primer columna esta el nombre del registro, en la segunda columna sus valores en hexadecimal y en la ultima, sus valores decimales.
