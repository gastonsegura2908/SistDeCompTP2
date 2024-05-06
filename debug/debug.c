#include <stdio.h>

extern int ChangesArray(float gini_index);

int main(){
    float gini_values[5] = {0.1, 0.2, 0.3, 0.4, 0.5};
    for(int i = 0; i < 5; i++) {
        int result = ChangesArray(gini_values[i]);
        printf("ChangesArray returned %d for input %f\n", result, gini_values[i]);
    }
    return 0;
}