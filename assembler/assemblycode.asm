section .data
    ; Datos de prueba (similares a los valores obtenidos desde Python)
    values_float: dd 25.5, 30.7, 35.2, 40.9
    num_values equ 4

section .text
    global ChangesArray
    extern malloc
    extern free_memory

ChangesArray:
    ; Entrada:
    ;   - edi: Puntero a los valores de punto flotante (values_float)
    ;   - esi: Tamaño del arreglo (num_values)
    ; Salida:
    ;   - eax: Puntero al nuevo arreglo de enteros

    push ebp
    mov ebp, esp

    ; Reservar memoria para el nuevo arreglo de enteros
    mov eax, esi
    shl eax, 2 ; Tamaño de cada elemento (4 bytes)
    call malloc
    mov ebx, eax ; ebx = Puntero al nuevo arreglo

    xor ecx, ecx ; Inicializar contador

convert_loop:
    ; Convertir float a int y sumar 1
    fld dword [edi + ecx*4] ; Cargar valor float
    fistp dword [ebx + ecx*4] ; Convertir a int y almacenar en el nuevo arreglo

    mov eax, dword [ebx + ecx*4] ; Cargar valor en eax
    inc eax ; Incrementar eax
    mov dword [ebx + ecx*4], eax ; Almacenar valor incrementado

    inc ecx
    cmp ecx, esi
    jl convert_loop

    mov eax, ebx ; Devolver el puntero al nuevo arreglo

    pop ebp
    ret
