from constraintsearch import *

region = ['A', 'B', 'C', 'D', 'E']
colors = ['red', 'blue', 'green', 'yellow', 'white']

neighbours_a = { 
    "A": "BED",
    "B": "AEC",
    "C": "BED",
    "D": "AEC",
    "E": "ABCD"
 }

neighbours_b = { 
    "A": "BED",
    "B": "AEC",
    "C": "BEF",
    "D": "AEF",
    "E": "ABCDF",
    "F": "DEC"
}

neighbours_c = { 
    "A": "BFED",
    "B": "AFC",
    "C": "BFGD",
    "D": "AEGC",
    "E": "AFGD",
    "F": "ABCGE",
    "G": "EFCD"
}

def mapa_constraint(r1, c1, r2, c2):
    if c1 == c2:
        return False
    return True

def make_constraint_graph(region, neighbours):
    return { (X,Y):mapa_constraint for X in region for Y in neighbours[X] }

def make_domain(region, colors):
    return { reg:colors for reg in region }


cs = ConstraintSearch(make_domain(neighbours_a.keys(), colors), make_constraint_graph(neighbours_a.keys(), neighbours_a))
print(cs.search())
""" cs_a = ConstraintSearch(make_domain(neighbours_a.keys(), colors), make_constraint_graph(neighbours_a.keys(), neighbours_a))
print(cs_a.search())
cs_b = ConstraintSearch(make_domain(neighbours_b.keys(), colors), make_constraint_graph(neighbours_b.keys(), neighbours_b))
print(cs_b.search())
cs_c = ConstraintSearch(make_domain(neighbours_c.keys(), colors), make_constraint_graph(neighbours_c.keys(), neighbours_c))
print(cs_c.search()) """
