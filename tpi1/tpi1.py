# NAME: Francisca Ines Marcos de Barros
# NMEC: 93102
#
# Discussed with: Lucas Sousa (93019) , Hugo Paiva (93195)

from tree_search import *
from cidades import *
from strips import *

class MyNode(SearchNode):
    def __init__(self, state, parent, depth=0, offset=0): 
        super().__init__(state, parent)
        self.depth = depth
        self.offset = offset


class MyTree(SearchTree):

    def __init__(self,problem, strategy='breadth'): 
        super().__init__(problem,strategy)
        self.root = MyNode(problem.initial, None, 0, 0)
        self.open_nodes = [self.root]
        self.depths_counter = {} # key: depth , value: offset
        self.from_init = None    # Sub-Tree1 - From initial to middle
        self.to_goal = None      # Sub-Tree2 - From middle to goal

    def hybrid1_add_to_open(self,lnewnodes):
        self.open_nodes[:0] = reversed(lnewnodes[::2])    # Even Indexes
        self.open_nodes.extend(lnewnodes[1::2]) # Odd

    def hybrid2_add_to_open(self,lnewnodes):
        self.open_nodes.extend(lnewnodes)
        self.open_nodes.sort(key = lambda node: node.depth-node.offset)

    def search2(self):
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            if self.problem.goal_test(node.state):
                self.terminal = len(self.open_nodes)+1
                self.solution = node
                return self.get_path(node)
            self.non_terminal+=1
            node.children = []
            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,a)
                if newstate not in self.get_path(node):
                    newdepth = node.depth+1
                    if self.depths_counter.get(newdepth):
                        myoffset = self.depths_counter.get(newdepth)
                    else:
                        myoffset = self.depths_counter[newdepth] = 0
                    newnode = MyNode(newstate, node, newdepth, myoffset)
                    self.depths_counter[newdepth] += 1
                    node.children.append(newnode)
 
            self.add_to_open(node.children)
        return None


    def search_from_middle(self):
        middleState = self.problem.domain.middle(self.problem.initial, self.problem.goal)
        self.from_init = MyTree(SearchProblem(self.problem.domain, self.problem.initial, middleState), self.strategy) # Initial to middle
        self.to_goal = MyTree(SearchProblem(self.problem.domain, middleState, self.problem.goal), self.strategy) # Middle to Goal
        solution1 = self.from_init.search2()
        solution2 = self.to_goal.search2()
        res = solution1+solution2[1:]
        #print(solution1, solution2)
        return res

class MinhasCidades(Cidades):

    # state that minimizes heuristic(state1,middle)+heuristic(middle,state2)
    def middle(self,city1,city2):
        return min([city for city in self.coordinates.keys() if city != city1 and city != city2], key= lambda state: self.heuristic(city1, state)+self.heuristic(state, city2))  

class MySTRIPS(STRIPS):
    def result(self, state, action):
        if not all(p in state for p in action.pc):
            return None
        newstate = [c for c in state if c not in action.neg] # remove as condições que deixam de ser verdade
        newstate.extend(action.pos) # adicionar a condições que passam a ser verdade
        return newstate

    def sort(self, state):
        return sorted(state, key= lambda a: str(a)) # doesnt cast 


