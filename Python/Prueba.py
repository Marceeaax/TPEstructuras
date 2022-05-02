import numpy as np
import requests
import csv
import matplotlib.pyplot as plt
import time

def insercion(arr1,arr2,arr3):
 
    # Ordenamiento por insercion, que suele ser eficaz con vectores no muy grandes
    # Extraido de geeksforgeeks
    for i in range(1, len(arr1)):
 
        key1 = arr1[i]
        if(len(arr2) > 0): key2 = arr2[i]
        if(len(arr3) > 0): key3 = arr3[i]

        j = i-1
        while j >= 0 and key1 > arr1[j] :
                arr1[j + 1] = arr1[j]
                if(len(arr2) > 0): arr2[j + 1] = arr2[j]
                if(len(arr3) > 0): arr3[j + 1] = arr3[j]
                j -= 1
        arr1[j + 1] = key1
        if(len(arr2) > 0): arr2[j + 1] = key2
        if(len(arr3) > 0): arr3[j + 1] = key3


lenguajes = ['Python', 'C', 'Java', 'C++', 'C#', 'Visual Basic', 'JavaScript', 'Assembly language', 'SQL', 'PHP', 'R', 'Delphi/Object Pascal', 'Go', 'Swift', 'Ruby', 'Classic Visual Basic', 'Objective-C', 'Perl', 'Lua', 'MATLAB']
repositorios = [275079, 43737, 163690, 45193, 46701, 912, 305721, 4722, 24021, 89460, 26173, 1890, 41607, 33834, 28159, 66, 5460, 3832, 9568, 9633]
rating = [89.97497178191097, 14.287677283211464, 53.532250413047386, 14.764031342526703, 15.25739804681749, 0.27678264710212497, 100.0, 1.5232860578102763, 7.8372675074839275, 29.246699710457868, 8.541329276471838, 0.5967512391421701, 13.590813171713206, 11.04774991411886, 9.19108144803782, 0.0, 1.7647347499631938, 1.2321080957288446, 3.1087337030311954, 3.129999509250626]

titulos = ['NOMBRE_LENGUAJE','NUMERO_APARICIONES']

for i in range(100):
    github = requests.get("https://github.com/topics/MATLAB?o=desc&s=updated",timeout=20)
    if(github.status_code > 300):
        print("Se produjo el error: ", github.status_code)
        print("Se deben esperar: ", github.headers['Retry-After'])
        print("Durmiendo por 70 segundos")
        time.sleep(70)
    else:
        print("Exito!")


