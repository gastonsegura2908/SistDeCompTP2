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