import Queue

goal_state=[0,1,2,3,4,5,6,7,8] #state is formatted as a list, with each 3 consecutive elements making up a row, with the first tuple being the top row, the second being the second row, etc.
practice_state=[1,2,0,3,4,5,6,7,8]
initial_state=[0,3,5,4,2,7,6,8,1]
actions=['up','down','left','right'] #list of actions, actions are handled within Problem class

class Problem(object):
    def __init__(self,initial_state,goal_state=None):
        self.initial_state=initial_state
        self.goal_state=goal_state
    def actions(self,state):
        #return all possible valid actions for the given state
        possible_actions=[]
        location=state.index(0)
        if(location>2): #if blank is not in top row then it can move up
            possible_actions.append("up")
        if(location<6): #if blank is not in bottom row then it can move down
            possible_actions.append("down")
        if(location%3!=0): #if blank is not in left column then it can move left
            possible_actions.append("left")
        if location%3!=2: #if blank is not in right column then it can move right
            possible_actions.append("right")
        return possible_actions
    def result(self,state,action):
        #returns resulting state as list of taking given action from given state
        location=state.index(0)
        if action=="up": #if action is up new location is one row up
            new_location=location-3
        elif action=="down": #if action is down new location is one row down
            new_location=location+3
        elif action=="left": #if action is left new location is one column left
            new_location=location-1
        elif action=="right": #if action is right new location is one column right
            new_location=location+1
        state[new_location],state[location]=state[location],state[new_location]
        return state
    def goal_test(self,state):
        #returns true if given state matches goal state
        return state==self.goal_state
class Node(object):
    def __init__(self,state,parent=None,action="None",path_cost=0,depth=0):
        self.state=state
        self.parent=parent
        self.action=action
        self.path_cost=path_cost
        self.depth=depth
    def expand(self,problem):
        #returns list of possible child nodes from current node
        return [self.child_node(problem,action) for action in problem.actions(self.state)]
    def child_node(self,problem,action):
        #returns the child node from the given current state and action
        return Node(problem.result(self.state[:],action),self,action, self.path_cost+1,self.depth+1)
    def solution(self):
        #prints off actions taken to reach current node from initial state
        return [node.action for node in self.path()[1:]]
    def pretty_solution(self):
        #returns string containing prettily formatted solution/path
        pretty_solution=""
        for node in self.path()[:]:
            pretty_solution+="Step "+str(node.depth)+" : "+node.action+"\n"+node.pretty_state()+"\n"
        return pretty_solution
    def path(self):
        #returns list of nodes from initial node to current node
        node,path_back=self,[]
        while node:
            path_back.append(node)
            node=node.parent
        return list(reversed(path_back))
    def pretty_state(self):
        #returns string of prettily formatted state of current node
        pretty_state=""
        for i in [0,3,6]:
            pretty_state+=str(self.state[i])+' '+str(self.state[i+1])+' '+str(self.state[i+2])+'\n'
        return pretty_state
    def __eq__(self,other):
        #returns true if current node matches other node, false otherwise
        return isinstance(other,Node) and self.state==other.state
    def __hash__(self):
        return hash(self.state)
def Cost2Go(state,goal_state):
    #returns number of differences between given state and goal state
    n=0
    for i in range(len(state)):
        if state[i]!=goal_state[i]:
            n+=1
    return n
def get_priority(node,goal_state):
    return node.path_cost+Cost2Go(node.state,goal_state)
def iterative_astar_search(node,problem):
    #performs essentially bfs but with priority queue where path_cost+cost2go is priority
    #returns prettily formatted solution or "No solution found" to get from given node to given probem's goal state
    
    #initialize frontier and explored
    frontier=Queue.PriorityQueue()
    explored=[]
    frontier.put((get_priority(node,problem.goal_state),node))
    while not frontier.empty(): #while items in frontier
        node=frontier.get()[1]
        if problem.goal_test(node.state): #if the node is goal state return solution
            return node.pretty_solution()
        explored.append(node.state)
        for action in problem.actions(node.state):
            new_node=node.child_node(problem,action)
            """
            if new node hasn't been explored, add it to frontier.
            otherwise, if it's already in explored then it had at least as good priority because path cost has to have been at least as little and cost2go is the same
            """
            if new_node.state not in explored:
                frontier.put((get_priority(new_node,problem.goal_state),new_node))
    return "No solution found"

print iterative_astar_search(Node(initial_state),Problem(initial_state,goal_state))