
from bayes_net import *

# Exemplo dos acetatos:

bn = BayesNet()

# lista vazia -> nao tem dependencias
bn.add('r',[],0.001) # probabilidade roubo
bn.add('t',[],0.002) # probabilidade terramoto

# ja tem dependencias; preciso entradas para todas as combinacoes
bn.add('a',[('r',True ),('t',True )],0.950) # probabilidade alarme tocar sabendo que houve um roubo e terramoto
bn.add('a',[('r',True ),('t',False)],0.940)
bn.add('a',[('r',False),('t',True )],0.290)
bn.add('a',[('r',False),('t',False)],0.001)

bn.add('j',[('a',True )],0.900)
bn.add('j',[('a',False)],0.050)

bn.add('m',[('a',True )],0.700)
bn.add('m',[('a',False)],0.100)

conjunction = [('j',True),('m',True),('a',True),('r',False),('t',False)] # determinar a probabilidade de o joao avisar, da maria ter avisado, do alarme ter tocado, nao ter havido um roubo e nao ter havido um terramoto

print(bn.jointProb(conjunction)) # valor muito baixo

import pprint
pprint.pprint(bn.conjunctions(['b', 'c']))
pprint.pprint(bn.dependencies)
pprint.pprint(bn.jointProb(['t', True]))