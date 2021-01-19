# Pesquisa para resolucao de problemas de atribuicao
# 
# Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2019
#


class ConstraintSearch:

    # domains é um dicionário com o domínio de cada variável;
    # constaints e' um dicionário com a restrição aplicável a cada aresta;
    def __init__(self,domains,constraints):
        self.domains = domains
        self.constraints = constraints
        self.calls = 0

    # domains é um dicionário com os domínios actuais
    # de cada variável
    # ( ver acetato "Pesquisa com propagacao de restricoes
    #   em problemas de atribuicao - algoritmo" )
    def search(self,domains=None):
        self.calls += 1 
        
        if domains==None:
            domains = self.domains

        # se alguma variavel tiver lista de valores vazia, falha
        if any([lv==[] for lv in domains.values()]):
            return None

        # se nenhuma variavel tiver mais do que um valor possivel, sucesso
        if all([len(lv)==1 for lv in list(domains.values())]):
            # se valores violam restricoes, falha
            # ( verificacao desnecessaria se for feita a propagacao
            #   de restricoes )
            """ for (var1,var2) in self.constraints:
                constraint = self.constraints[var1,var2]
                if not constraint(var1,domains[var1][0],var2,domains[var2][0]):
                    return None  """
            return { v:lv[0] for (v,lv) in domains.items() }
       
        # continuação da pesquisa
        # ( falta fazer a propagacao de restricoes )
        for var in domains.keys():
            if len(domains[var])>1:
                for val in domains[var]:
                    newdomains = dict(domains)
                    newdomains[var] = [val]

                    newdomains = self.propagate(newdomains, [(n, v) for n,v in self.constraints if v == var])

                    solution = self.search(newdomains)
                    if solution != None:
                        return solution
        return None

    def propagate(self, domains, neighbours):
        while neighbours != []:
            neighbour, var = neighbours.pop(0)
            values = []
            for val in domains[var]:
                constraint = self.constraints[neighbour, var]
                values = [ x for x in domains[neighbour] if constraint(neighbour, x, var, val) ]
                if len(values) < len(domains[neighbour]):
                    domains[neighbour] = values
                    # Extender nos abertos com neighbours dos neighbours
                    neighbours.extend( [ (nn, n) for nn, n in self.constraints if n == neighbour ] )
        return domains