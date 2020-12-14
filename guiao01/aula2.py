#Exercicio 4.1
impar = lambda x: x%2 != 0

#Exercicio 4.2
positivo = lambda x: x > 0

#Exercicio 4.3
comparar_modulo = lambda x,y: abs(x) < abs(y)

#Exercicio 4.4
import math
cart2pol = lambda x,y: (math.sqrt(x**2 + y**2), math.atan2(y,x))

#Exercicio 4.5
def ex5(f,g,h):
    return lambda x,y,z: h(f(x,y),g(y,z))

#Exercicio 4.6
def quantificador_universal(lista, f):
    if lista == []:
        return True
    else:
        return f(lista[0]) and quantificador_universal(lista[1:],f)

#Exercicio 4.9
def ordem(lista, f):
    if lista == []:
        return None
    else:
        primeiro = lista[0]
        menor = ordem(lista[1:], f)
        if menor != None and f(menor, primeiro):
            return menor
        else:
            return primeiro

#Exercicio 4.10
def filtrar_ordem(lista, f):
    if lista == []:
        return None
    else:
        return ( ordem(lista,f), [item for item in lista if item != ordem(lista,f)] )

#Exercicio 5.2a
# A funcao de ordenacao recebe, num parametro adicional, a relacao de ordem 
# (uma funcao binaria booleana para comparacao elemento a elemento) segundo a qual a lista de entrada deve ser ordenada.
def ordenar_seleccao(lista, ordem2):
    if lista == []:
        return []
    else:
        primeiro = lista[0]
        segundo = ordem(lista[1:], ordem2)
        aux = []
        if segundo != None and ordem(segundo, primeiro):
            aux.append()
        else:
            pass
