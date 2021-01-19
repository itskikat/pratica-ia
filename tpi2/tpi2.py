#encoding: utf8

# NAME: Francisca Ines Marcos de Barros
# NMEC: 93102
#
# Discussed with: Lucas Sousa (93019) , Hugo Paiva (93195)

from semantic_network import *
from bayes_net import *
from constraintsearch import *
from collections import Counter

class MyBN(BayesNet):

    def individual_probabilities(self):
        # IMPLEMENTAR AQUI
        output = {}
        for var in self.dependencies.keys():
            variaveis = [k for k in self.dependencies.keys() if k != var] 
            output[var] = sum( [ self.jointProb( [(var, True)] + c) for c in self.conjunctions(variaveis) ] )
        return output

    # Conjuncoes
    def conjunctions(self, variaveis):
        if len(variaveis) == 1:
            return [ [(variaveis[0], True)], [(variaveis[0], False)] ]
        l = []
        for c in self.conjunctions(variaveis[1:]):
            l.append([(variaveis[0], True)] + c)
            l.append([(variaveis[0], False)] + c) 
        return l


class MySemNet(SemanticNetwork):
    def __init__(self):
        SemanticNetwork.__init__(self)

    # From P classes
    def query_local(self,user=None,e1=None,relname=None,e2=None, rel_type=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (relname == None or d.relation.name == relname)
                and (e2 == None or d.relation.entity2 == e2)
                and (rel_type == None or isinstance(d.relation, rel_type)) ]
        return self.query_result

    def translate_ontology(self):
        #IMPLEMENTAR AQUI
        subs = [d.relation for d in self.declarations if isinstance(d.relation, Subtype)]
        relations = {}
        for s in subs:
            if s.entity2 not in relations.keys():
                relations[s.entity2] = set()
            relations[s.entity2].add(s.entity1)
        output = []
        for key in sorted(relations.keys()):
            values = ''
            for value in sorted(relations[key]):
                values += f'{value[0].upper()+value[1:]}(x) or '
            output.append(f'Qx {values[:-4]} => {key[0].upper()+key[1:]}(x)')
        return output

    def query_inherit(self,entity,assoc):
        #IMPLEMENTAR AQUI
        inverse = [i for i in self.declarations if isinstance(i.relation, Association) and i.relation.entity2 == entity]
        if inverse:
            for i in inverse:
                local = [l for l in self.query_local(e2=entity, relname=i.relation.name) if l.relation.inverse != None]
                preds = [d.relation.entity1 for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity2 == entity]
        else:
            local = self.query_local(e1=entity, relname=assoc)
            preds = [d.relation.entity2 for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1 == entity]
        outcome = []
        for p in preds:
            outcome += self.query_inherit(p, assoc)
        return local+outcome

    def query(self,entity,relname):
        #IMPLEMENTAR AQUI
        all_ = self.query_local(e1=entity, relname=relname)
        rels = self.query_local(relname=relname, rel_type=Association) # Associations with that name
        local = self.query_local(e1=entity, relname=relname, rel_type=Association) # Local relations
        preds = [d for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1 == entity] # Predecessors
        singles = [s for s in local if s.relation.cardinality == 'single'] # Single cardinality
        multiples = [m for m in local if m.relation.cardinality == 'multiple'] # Multiple cardinality
        outcome = [] # output
        for a in all_:
            if a in singles or isinstance(a.relation, (Member, Subtype)):
                preds = [d for d in preds if d.relation.name != a.relation.name]
        if len(singles) > 1:
            # Most common value
            outcome += [Counter([s.relation.entity2 for s in singles]).most_common(1)[0][0]]
        for pred in [d.relation.entity2 for d in preds]:
            outcome += self.query(pred, relname) # Query nos predecessores
        properties = [l.relation.assoc_properties() for l in rels]
        c = Counter(properties).most_common(1) # most common
        return list(set( outcome + [ l.relation.entity2 for l in all_ if l in multiples and l.relation.assoc_properties() == c[0][0] or isinstance(l.relation,(Member, Subtype)) ] )) if len(c)>0 else list(set( outcome + [ l.relation.entity2 for l in all_ if l in multiples or isinstance(l.relation,(Member,Subtype)) ] ))


class MyCS(ConstraintSearch):

    def search_all(self,domains=None,xpto=None):
        # Pode usar o argumento 'xpto' para passar mais
        # informação, caso precise
        #
        # IMPLEMENTAR AQUI
        
        # Vals that were already visited 
        if not xpto:
            xpto = set()
            

        if domains==None:
            domains = self.domains

        # se alguma variavel tiver lista de valores vazia, falha
        if any([lv==[] for lv in domains.values()]):
            return None

        # se nenhuma variavel tiver mais do que um valor possivel, sucesso
        if all([len(lv)==1 for lv in list(domains.values())]):
            return { v:lv[0] for (v,lv) in domains.items() }

        solutions = []
        # continuação da pesquisa
        for var in domains.keys():
            if len(domains[var])>1:
                for val in domains[var]:
                    if val not in xpto:
                        xpto.add(val)
                        newdomains = dict(domains)
                        newdomains[var] = [val]
                        newdomains = self.propagate(newdomains, [(v1,v2) for (v1,v2) in self.constraints if v2==var] )
                        solution = self.search_all(newdomains, xpto=xpto)
                        if solution != None:
                            solutions.append(solution)
        return solutions
        
    # Propagar restruicoes
    def propagate(self, domains, neighbours):
        while neighbours != []:
            neighbour, var = neighbours.pop(0)
            values = []
            for val in domains[var]:
                constraint = self.constraints[neighbour, var]
                values = [ x for x in domains[neighbour] if constraint(neighbour, x, var, val) ]
                if len(values) < len(domains[neighbour]):
                    domains[neighbour] = values
                    if not values:
                        return domains
                    # Extender nos abertos com neighbours dos neighbours
                    neighbours.extend( [ (nn, n) for nn, n in self.constraints if n == neighbour ] )
        return domains

