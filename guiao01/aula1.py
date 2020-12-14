#Exercicio 1.1
def comprimento(lista):
	if lista == []:
		return 0
	else:
		return 1+comprimento(lista[1:])

#Exercicio 1.2
def soma(lista):
	if lista == []:
		return 0
	else:
		return lista[0]+soma(lista[1:])

#Exercicio 1.3
def existe(lista, elem):
	if lista == []:
		return False
	elif lista[0] == elem:
		return True
	else:
		return existe(lista[1:], elem)

#Exercicio 1.4
def concat(l1, l2):
	if l1 == []:
		return l2
	if l2 == []:
		return l1
	l1.append(l2[0])
	return concat(l1, l2[1:])

#Exercicio 1.5
def inverte(lista):
	if lista == []:
		return []
	else:
		return inverte(lista[1:]) + [lista[0]]

#Exercicio 1.6
def capicua(lista):
	if lista == []:
		return True
	elif lista[0] == lista[-1]:
		return capicua(lista[1:-1])
	else:
		return False

#Exercicio 1.7
def explode(lista):
	if lista == []:
		return []
	else:
		return lista[0] + explode(lista[1:])

#Exercicio 1.8
def substitui(lista, original, novo):
	if lista == []:
		return []
	elif lista[0] == original:
		lista[0] = novo
	return [lista[0]] + substitui(lista[1:], original, novo)

#Exercicio 1.9
def junta_ordenado(lista1, lista2):
	if lista1 == []:
		return lista2
	if lista2 == []:
		return lista1
	return (lambda l1,l2: [min(l1,l2),max(l1,l2)])(lista1[0], lista2[0]) + junta_ordenado(lista1[1:], lista2[1:])

#Exercicio 1.10 - Dado um conjunto, na forma de uma lista, retorna uma lista de listas que representa o conjunto de todos os subconjuntos do conjunto dado.
def conjunto_subconjuntos(lista):
	if lista == []:    # conjunto vazio pertence a todos os conjuntos
		return [[]]
	else:
		subconjuntos = conjunto_subconjuntos(lista[1:])
		return subconjuntos + [[lista[0]] + conjunto for conjunto in subconjuntos]


## II

#Exercicio 2.1 - Dada uma lista de pares, produzir um par com as listas dos primeiros e segundos elementos desses pares.
# separar ([(a1, b1), ... (an, bn)]) = ([a1, ... an], [b1, ... bn])
def separar(lista):
	if lista == []:
		return ([],[])
	a1, b1 = lista[0] #1o tuplo
	listaA, listaB = separar(lista[1:]) #tuplo seguinte
	return ([a1]+listaA, [b1]+listaB)

#Exercicio 2.2 - Dada uma lista l e um elemento x, retorna um par formado pela lista dos elementos de l diferentes de x e pelo numero de ocorrencias x em l.
# remove_e_conta([1,6,2,5,5,2,5,2],2) = ([1,6,5,5,5],3)
def remove_e_conta(lista, elem):
	if lista == []:
		return ([], 0)
	lista2, count = remove_e_conta(lista[1:],elem)
	if lista[0] == elem:
		return (lista2, count+1)
	else:
		return ([lista[0]] + lista2, count)

#Exercicio 2.3 - Dada uma lista, retorna o nu ́mero de ocorrˆencias de cada elemento, na forma de uma lista de pares (elemento,contagem).
def conta_elem(lista):
	if lista == []:
		return ([], 0)
	lista2, count = remove_e_conta(lista, lista[0])
	return [(lista[0]), count] + conta_elem(lista2)


## III

#Exercicio 3.1
def cabeca(lista):
	if lista == []:
		return None
	return lista[0]

#Exercicio 3.2
def cauda(lista):
	if len(lista) < 2:
		return None
	return lista[1:]

#Exercicio 3.3
def juntar(l1, l2):
	if len(l1) != len(l2):
		return None
	elif not l1:
		return []
	else:
		return [(l1[0], l2[0])] + juntar(l1[1:], l2[1:])

#Exercicio 3.4
def menor(lista):
	if lista == []:
		return None
	min_numb = menor(lista[1:])	
	if min_numb == None or min_numb > lista[0]:
		return lista[0]
	else:
		return min_numb

#Exercicio 3.5 - Dada uma lista de numeros, retorna um par formado pelo menor elemento e pela lista dos restantes elementos.
def menor_listagem(lista):
	if lista == []:
		return None
	restantes = menor_listagem(lista[1:])
	if restantes == None:
		return [lista[0], lista[1:]]
	elif restantes[0] > lista[0]:
		return (lista[0], [restantes[0]]+lista[1:])
	else:
		return (restantes[0], [restantes[1]]+lista[0])

#Exercicio 3.6
def max_min(lista):
	if lista == []:
		return None
	lista2 = max_min(lista[1:])
	if lista2 == None:
		return (lista[0], lista[0])
	maximo, minimo = lista[0], lista[0]
	if minimo > lista2[0]:
		minimo = lista2[0]
	if maximo < lista2[1]:
		maximo = lista2[1]
	return minimo, maximo

#Exercicio 3.7 - Dada uma lista de numeros, retorna um triplo formado pelos dois menores elementos e pela lista dos restantes elementos.
def menores_lista(lista):
	if lista == []:
		return None
	menor1, restantes1 = menor_listagem(lista)
	menor2, restantes2 = menor_listagem(restantes1)
	return (menor1, menor2, restantes2)

#Exercicio 3.8 - Dada uma lista ordenada de numeros, calcular se possıvel a respectiva media e mediana, retornando-as num tuplo.
def media_mediana(lista):
	if lista == []:
		return None
	mediana = lista[len(lista)//2]
	total = 0
	for numb in lista:
		total += numb
	media = total/len(lista)
	return (media, mediana)
