# This code takes a regular expression (regex) as entry and generates
# the epsilon_nfa, and then the nfa (nondetermnistic finite automaton) 
# correspondent to the entered expression, returning those as output 

class Node:
  """
  Class representing the states in the automaton graph 
  """
  # Class variable to register total of nodes in the graph
  total = 0

  def __init__(self):
    self.children = [] # List of archs [symbol, node] from this state
    self.parents = []  # List of archs [symbol, node] to this state 
    self.number = Node.total   # Number that identifies the node
    Node.total = Node.total+1  # Total of nodes is updated

  def __str__(self):
    return str(self.number)

class Graph:
  """
  Class representing the automaton graph
  """
  def __init__(self, regex):
    """
    :param regex: regular expression that generates the graph 
    """
    self.start = Node() # Start of the automaton
    self.end = Node()   # Final states of the automaton, initially 
		        # composed of only one state
    
    self.start.children.append([regex, self.end])
    self.nodes = [self.start, self.end]   
    self.e_closures = [[self.start], [self.end]]

    self.end = [self.end] # Must be a list of final states
	
  def generate_enfa(self):
    """
    Generates a epsilon_nfa from a regex. Algorithm used is, for
    each arch in the graph:
    1) Parse the regex into a list of symbols. Subexpressions 
       separeted by parenthesis are stored as they are, without
       parenthesis, for later parsing.
    
    2) Look for unions in the regex. Unions must be separated in
       two archs between the same nodes.

    3) Look for concatenations, which must be separated generating
       a new node between the original nodes.

    4) Look for Kleene stars, which must generate a new node between
       the original nodes, separated by epsilon-transitions, with an
       arch to itself denoting the starred expression. 
      
    5) Repeat until each arch is denoted by an only symbol
    """
    operations = ['+','*'] # Characters representing operantions, 
                           # thus not included in a language

    for node in self.nodes:
      idx = 0
      while idx < len(node.children):
        [regex, child] = node.children[idx]
        
        processed_regex = process_regex(regex)
        if len(processed_regex) == 1:
          processed_regex = process_regex(''.join(processed_regex))

        # Process Unions
        found_union = False
        for idx2 in range(len(processed_regex)):
          if processed_regex[idx2] == '+':
            found_union = True
            r1 = processed_regex[:idx2]
            r2 = processed_regex[idx2+1:]

            node.children.pop(idx)
            node.children.append([r1, child])
            node.children.append([r2, child])
            idx -= 1
            
            break

        # Process Concatenations
        found_concatenation = False
        if not found_union:
          if len(processed_regex) == 2 and processed_regex[1] == '*':
            pass
          elif len(processed_regex) > 1:
            found_concatenation = True

            r1 = []
            r2 = []

            if processed_regex[1] == '*':
              r1 = processed_regex[:2]
              r2 = processed_regex[2:]
            else:
              r1 = processed_regex[0]
              r2 = processed_regex[1:]
          
            aux_node = Node()
            self.nodes.append(aux_node)
            self.e_closures.append([aux_node])
            
            node.children.pop(idx)
            node.children.append([r1, aux_node])
            aux_node.children.append([r2, child])
            idx -= 1

        # Process Kleene Star
        if not found_concatenation:
          if len(processed_regex) == 2:
            aux_node = Node()
            self.nodes.append(aux_node)
            self.e_closures.append([aux_node])           
            
            node.children.pop(idx)
            node.children.append(['&', aux_node])
            aux_node.children.append([processed_regex[0], aux_node])
            aux_node.children.append(['&', child])
            idx -= 1

        idx += 1

  def calculate_e_closure(self, node):
    """
    Recursive function for calculating the epsilon_closure of a node, 
    stored at the e_closures attribute from the graph. If a final
    node is in the e_closure, this node must also be a final node. 
    """
    idx = 0

    while idx < len(node.children):
      [symbol, child] = node.children[idx]
      if symbol == '&':
        node.children.pop(idx)
        self.e_closures[node.number].extend(self.calculate_e_closure(child))
        if child in self.end:
          self.end.append(node)
      
      else:
        idx += 1
   
    return self.e_closures[node.number]
 
  def generate_nfa(self):    
    """
    Generates a nfa from a previous epsilon_nfa. Algorithm used is, 
    for each node:
    1) Compute the epsilon_closure of this node
    
    2) Every arch from A to this node, must generate an arch to B,
       for each B in the e_closure.

    3) Every arch from B to A, must generate an arch from this node
       to be, for each B in the e_closure.

    4) If the original final state is in the e_closure, this is a
       final node too (done in calculate_e_closure())      
    """
    for node in self.nodes: 
      self.calculate_e_closure(node)

    for node in self.nodes:
      for symbol, child in node.children:
        child.parents.append([symbol, node])    
    
    new_children = []
    for node in self.nodes:
      sub_new_children = []
      for symbol, child in node.children:
        for grand_child in self.e_closures[child.number][1:]:       
          sub_new_children.append([symbol, grand_child])           
          grand_child.parents.append([symbol, node]) 

      for child in self.e_closures[node.number][1:]:
        for symbol, grand_child in child.children:  
          sub_new_children.append([symbol, grand_child])
          grand_child.parents.append([symbol, node]) 
      
      new_children.append(sub_new_children)

    for idx, l in enumerate(new_children):
      self.nodes[idx].children.extend(l)      

    idx = 1 
    while idx < len(self.nodes):
      if not self.nodes[idx].parents:
        self.nodes.pop(idx)
      else:
        idx += 1
         
  def __str__(self):
    s = ''
    for node in self.nodes:
      s += str(node)
      
      if not node.children:
        s += ':\n'
        continue

      s += ': ['

      for regex, child in node.children:
        s += '(' + regex[0] + ', ' + str(child) + '), '
      
      s = list(s)
      s = s[0:-1]
      s[-1] = ']\n'
      s = ''.join(s)
    
    s += '\nEnd: ['

    for node in self.end:
      s += str(node) + ', '
 
    s = list(s)
    s = s[0:-1]
    s[-1] = ']\n'
    s = ''.join(s)
 
    return s


def process_regex(regex):
  while regex != eliminate_start_end_parenthesis(regex):
    regex = eliminate_start_end_parenthesis(regex)

  processed = []

  parenthesis = 0
  start = 0
  end = 0

  for idx, c in enumerate(regex):
    if c == '(':
      if not parenthesis:
        start = idx
      parenthesis += 1
    elif c == ')':
      parenthesis -= 1
    if not parenthesis:
      end = idx
      block = regex[start:(end+1)]
      processed.append(''.join(block))
      start = idx+1
      end = idx+1

  for idx in range(len(processed)):
    while eliminate_start_end_parenthesis(processed[idx]) != processed[idx]:
      processed[idx] = eliminate_start_end_parenthesis(processed[idx])

  return processed

def eliminate_start_end_parenthesis(block):
  parenthesis = 0
  alter = True

  if block[0] == '(':
    for idx, c in enumerate(block):
      if c == '(':
        parenthesis += 1
      elif c == ')':
        parenthesis -= 1
      if not parenthesis and idx != (len(block)-1):
        alter = False
      if not parenthesis and idx == (len(block)-1) and alter:
        block = list(block)
        block = block[1:-1]
        block = ''.join(block)
       
  return block

regex = input()
g = Graph(regex)
g.generate_enfa()
print(g)

print('\n \n')

g.generate_nfa()
print(g)
