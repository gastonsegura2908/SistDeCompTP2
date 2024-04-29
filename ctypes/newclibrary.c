#include <stdio.h>
#include <string.h>
#include <stdlib.h>


// Prototipo de la función en ensamblador
extern int* ChangesArray(float* arr, int size);

// Función en C que se comunica con Python y llama a la función en ensamblador
int* CallAssemblyFunction(float* values, int num_values) {
    // Llamar a la función en ensamblador
    int* new_values = ChangesArray(values, num_values);

    // Devolver los resultados al archivo Python
    return new_values;
}

void free_memory(int *arr){
    free(arr);
}