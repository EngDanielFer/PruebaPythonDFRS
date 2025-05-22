def numero_mas_frecuente(lista):
    if not lista:
        return None
    veces = {}
    for numero in lista:
        veces[numero] = veces.get(numero, 0) + 1
    num_lista = max(veces, key=veces.get)
    reps = veces[num_lista]
    print(f"Número que más se repite: {num_lista}, repetido {reps} veces")
    return num_lista

lista_num = input("Ingresa la lista con los números separados por espacios")

lista_numeros = list(map(int, lista_num.split()))

numero_mas_frecuente(lista_numeros)