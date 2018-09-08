class Node:
  total = 0

  def __init__(self):
    self.childs = []
    self.parents = []
    self.number = Node.total
    Node.total = Node.total+1


  def __str__(self):
    return str(self.number)

class Graph:
  def __init__(self, regex):
    self.start = Node()
    self.end = Node()
    
    self.start.childs.append([regex, self.end])
    self.nodes = [self.start, self.end]   
    self.e_closures = [[self.start], [self.end]]

    self.end = [self.end]
	
  def generate_enfa(self):
    operations = ['+','*']

    for node in self.nodes:
      idx = 0
      while idx < len(node.childs):
        [regex, child] = node.childs[idx]
        
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

            node.childs.pop(idx)
            node.childs.append([r1, child])
            node.childs.append([r2, child])
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
            
            node.childs.pop(idx)
            node.childs.append([r1, aux_node])
            aux_node.childs.append([r2, child])
            idx -= 1

        # Process Kleene Star
        if not found_concatenation:
          if len(processed_regex) == 2:
            aux_node = Node()
            self.nodes.append(aux_node)
            self.e_closures.append([aux_node])           
            
            node.childs.pop(idx)
            node.childs.append(['&', aux_node])
            aux_node.childs.append([processed_regex[0], aux_node])
            aux_node.childs.append(['&', child])
            idx -= 1

        idx += 1

  def calculate_e_closure(self, node):
    idx = 0

    while idx < len(node.childs):
      [symbol, child] = node.childs[idx]
      if symbol == '&':
        node.childs.pop(idx)
        self.e_closures[node.number].extend(self.calculate_e_closure(child))
        if child in self.end:
          self.end.append(node)
      
      else:
        idx += 1
   
    return self.e_closures[node.number]
 
  def generate_nfa(self):    
    for node in self.nodes: 
      self.calculate_e_closure(node)

    for node in self.nodes:
      for symbol, child in node.childs:
        child.parents.append([symbol, node])    
    
    new_childs = []
    for node in self.nodes:
      sub_new_childs = []
      for symbol, child in node.childs:
        for grand_child in self.e_closures[child.number][1:]:       
          sub_new_childs.append([symbol, grand_child])           
          grand_child.parents.append([symbol, node]) 

      for child in self.e_closures[node.number][1:]:
        for symbol, grand_child in child.childs:  
          sub_new_childs.append([symbol, grand_child])
          grand_child.parents.append([symbol, node]) 
      
      new_childs.append(sub_new_childs)

    for idx, l in enumerate(new_childs):
      self.nodes[idx].childs.extend(l)      

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
      
      if not node.childs:
        s += ':\n'
        continue

      s += ': ['

      for regex, child in node.childs:
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
