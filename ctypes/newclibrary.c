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

