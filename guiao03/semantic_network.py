

# Guiao de representacao do conhecimento
# -- Redes semanticas
# 
# Inteligencia Artificial & Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2020
# v1.9 - 2019/10/20
#


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#

from collections import Counter

class Relation:
    def __init__(self,e1,rel,e2):
        self.entity1 = e1
#       self.relation = rel  # obsoleto
        self.name = rel
        self.entity2 = e2
    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + ")"
    def __repr__(self):
        return str(self)


# Subclasse Association
class Association(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

#   Exemplo:
#   a = Association('socrates','professor','filosofia')

# Associacoes com valor unico
class AssocOne(Relation):
    def __init__(self, e1, assoc, e2):
        Relation.__init__(self, e1, assoc, e2)

# Associacoes com valores numericos
class AssocNum(Relation):
    def __init__(self, e1, assoc, e2):
        Relation.__init__(self, e1, assoc, float(e2))



# Subclasse Subtype
class Subtype(Relation):
    def __init__(self,sub,super):
        Relation.__init__(self,sub,"subtype",super)


#   Exemplo:
#   s = Subtype('homem','mamifero')

# Subclasse Member
class Member(Relation):
    def __init__(self,obj,type):
        Relation.__init__(self,obj,"member",type)

#   Exemplo:
#   m = Member('socrates','homem')

# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self,user,rel):
        self.user = user
        self.relation = rel
    def __str__(self):
        return "decl("+str(self.user)+","+str(self.relation)+")"
    def __repr__(self):
        return str(self)

#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)

# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#
class SemanticNetwork:
    def __init__(self,ldecl=None):
        self.declarations = [] if ldecl==None else ldecl
    def __str__(self):
        return str(self.declarations)
    def insert(self,decl):
        self.declarations.append(decl)
    # Permite 'questionar' a rede semantica
    """
        e1 - entidade1
        rel - relacao
        e2 - entidade2
    """
    def query_local(self,user=None,e1=None,rel=None,e2=None, rel_type=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (rel == None or d.relation.name == rel)
                and (e2 == None or d.relation.entity2 == e2)
                and (rel_type == None or isinstance(d.relation, rel_type)) ]
        return self.query_result
    def show_query_result(self):
        for d in self.query_result:
            print(str(d))

    # Lista (dos nomes) das associacoes existentes
    def list_associations(self):
        return list(set([declaration.relation.name for declaration in self.declarations if isinstance(declaration.relation, Association)]))

    # Lista das entidades declaradas como instancias de tipos
    def list_objects(self):
        return list(set([declaration.relation.entity1 for declaration in self.declarations if isinstance(declaration.relation, Member)]))

    # Lista de utilizadores existentes na rede
    def list_users(self):
        return list(set([declaration.user for declaration in self.declarations]))

    # Lista de tipos existente na rede
    def list_types(self):
        return list(set( 
            [d.relation.entity1 for d in self.declarations if isinstance(d.relation, Subtype)] +
            [d.relation.entity2 for d in self.declarations if isinstance(d.relation, Member) or isinstance(d.relation, Subtype)]
            ))
    
    # Dada uma entidade, devolva a lista (dos nomes) das associacoes localmente declaradas.
    def list_local_associations(self, entity):
        return list(set(
            [d.relation.name for d in self.declarations if isinstance(d.relation, Association) and entity in [d.relation.entity1, d.relation.entity2] ]
        ))

    # Dado um utilizador, devolva a lista (dos nomes) das relacoes por ele declaradas
    def list_relations_by_user(self, user):
        return list(set(
            [d.relation.name for d in self.declarations if d.user == user]
        ))

    # Dado um utilizador, devolva o numero de associacoes diferentes por ele utilizadas nas relacoes que declarou.
    def associations_by_user(self, user):
        return len(set( [d.relation.name for d in self.declarations if isinstance(d.relation, Association) and d.user == user]))
    
    # Dada uma entidade, devolva uma lista de tuplos
    # - cada tuplo contem (o nome de) uma associacao localmente declarada e o utilizador que a declarou.
    def list_local_associations_by_user(self, entity):
        return list(set( 
            [ (d.relation.name, d.user) for d in self.declarations if isinstance(d.relation, Association) and entity in [d.relation.entity1, d.relation.entity2]] 
        ))

    # Uma entidade A e predecessora (ou ascendente) de uma entidade B se existir uma cadeia de relacoes Member e/ou Subtype que liguem B a A
    # dadas duas entidades (dois tipos, ou um tipo e um objecto), devolva True se a primeira for predecessora da segunda, e False caso contrario.
    def predecessor(self, A, B):
        predec_b = [ d.relation.entity2 for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1 == B ] 

        return A in predec_b or any([self.predecessor(A, p) for p in predec_b])

    # dadas duas entidades (dois tipos, ou um tipo e um objecto), em que a primeira e predecessora da segunda
    # devolver uma lista composta pelas entidades encontradas no caminho desde a primeira ate a segunda entidade. 
    def predecessor_path(self, A, B):
        predec_b = [ d.relation.entity2 for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1 == B ] 

        if A in predec_b:
            return [A, B]
        
        for path in [self.predecessor_path(A, p) for p in predec_b]: # lista de listas em que cada lista é o caminho (se existir) de A até um p
            if not path is None: # existe um caminho
                return path + [B]

        return None # nao ha qualquer ligacao direta nem atraves de ninguem

    # query_local () nao faz heranca de conhecimento, apenas consulta declaracoes locais das entidades.
    # obter todas as declaracoes de associacoes locais ou herdadas por uma entidade. 
    # recebe como entrada a entidade e, opcionalmente, o nome da associacao.
    def query(self, entity, assoc_name=None):
        # query sobre predecessors
        pds = [ self.query(d.relation.entity2, assoc_name) for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1 == entity ]
        # extrair listas das listas 
        pds_query = [ d for sublist in pds for d in sublist ]

        return pds_query + self.query_local(e1=entity, rel=assoc_name, rel_type=Association)

    # obter todas as declaracoes locais (incluindo Member e Subtype) ou herdadas (apenas Association) por uma entidade. 
    # recebe como entrada a entidade e, opcionalmente, o nome da relacao. 
    def query2(self, entity, rel_name=None):
        # associacoes
        assoc = self.query(entity, rel_name)
        # concatenar as relacoes de tipo Member e Subtype locais
        return assoc + self.query_local(e1=entity, rel=rel_name, rel_type=(Member, Subtype))

    # cancelamento de heranca. Neste caso, 
    # quando uma associacao esta declarada numa entidade, a entidade nao herdara essa associacao das entidades predecessoras. 
    # recebe como entrada a entidade e o nome da associacao.
    def query_cancel(self, entity, assoc_name=None):
        pds = [ self.query_cancel(d.relation.entity2, assoc_name) for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1 == entity ]
        # declaracoes locais
        local = self.query_local(e1=entity, rel=assoc_name, rel_type=Association)
        # filtrar as declaracoes cuja relacao tem o mesmo nome que as locais
        pds_query = [ d for sublist in pds for d in sublist if d.relation.name not in [l.relation.name for l in local] ]
        # juntar filtro com declaracoes locais
        return pds_query + local

    # devolva uma lista com todas as declaracoes dessa associacao em entidades descendentes desse tipo.
    def query_down(self, entity, assoc_name, first=True):
        desc = [ self.query_down(d.relation.entity1, assoc_name, first=False) for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity2 == entity ]
        # extrair listas das listas
        desc_query = [ d for sublist in desc for d in sublist ] 
        if first:
            return desc_query
        # query local em cada patamar
        local = self.query_local(e1=entity, rel=assoc_name, rel_type=Association)

        return desc_query + local

    # devolva o valor mais frequente dessa associacao nas entidades descendentes.
    def query_induce(self, entity, assoc_name):
        desc = self.query_down(entity, assoc_name)
        # todos os valores
        values = [d.relation.entity2 for d in desc]
        # lista
        c = Counter(values).most_common(1)
        # extrair tuplo da lista
        for val, count in c:
            return val

        return None 

    # fazer consultas de valores das associacoes locais de uma dada entidade
    def query_local_assoc(self, entity, assoc_name):
        local = self.query_local(e1=entity, rel=assoc_name)

        for l in local:
            if isinstance(l.relation, AssocNum):
                values = [d.relation.entity2 for d in local]
                return sum(values)/len(local)

            if isinstance(l.relation, AssocOne):
                # lista de tuplos
                val, count = Counter([d.relation.entity2 for d in local]).most_common(1)[0]
                return val, count/len(local)

            if isinstance(l.relation, Association):
                # lista de valores mais frequentes
                mc = []
                freq = 0
                for val, count in Counter([d.relation.entity2 for d in local]).most_common():
                    mc.append((val, count/len(local)))
                    freq += count/len(local)
                    if freq > 0.75:
                        return mc

    def query_assoc_value(self, E, A):
        local = self.query_local(e1=E, rel=A)

        local_values = [l.relation.entity2 for l in local]

        # saber se sao todos iguais
        if len(set(local_values)) == 1:
            return local_values[0]

        # todos
        all_ = self.query(entity=E, assoc_name=A)
        # predecessores
        predecessor = [a for a in all_ if a not in local]
        # valores herdados
        predecessor_values = [i.relation.entity2 for i in predecessor]

        # percentagem de declaracoes de v na lista (de declaracoes)
        def perc(lista, value):
            if lista == []:
                return 0
            return len([l for l in lista if l.relation.entity2 == value])/len(lista)

        return max(local_values + predecessor_values, key=lambda v: (perc(local, v)+perc(predecessor, v))/2)


