import numpy as np

class Node(object):
    def __init__(self, energy = 1.0, state = np.array([1.0, 0.0]), name = None):
        self.state = state
        self.energy = energy
        self.name = name
        
    def __str__(self):
        if self.name is not None:
            node_string = 'Node "{}"\n'.format(self.name)
        else: 
            node_string = 'Unnamed Node:'
        node_string += 'Energy: {0}\nCurrent state: {1}'.format(self.energy,self.state)
        return node_string
    
    def update_state(self, new_state):
        self.state = new_state
        return
    
class Layer(object):
    def __init__(self, num_nodes, states='default', energies='default', name = None):
        self.num_nodes = num_nodes
        if name is not None:
            self.name = name
        else:
            self.name = "Unnamed"
        
        default_state = np.array([1.0,0.0])
        default_energy = 1.0
        
        self.nodes = []
        for ctr in range(self.num_nodes):
            if states == 'default':
                node_state = default_state
            else:
                if np.shape(states)[0] != num_nodes: 
                    print 'Warning: states are inconsistent with num_nodes, using default value'
                    node_state = default_state 
                else:
                    node_state = states[ctr]
            if energies == 'default':
                node_energy = default_energy
            else:
                if len(energies) != num_nodes:
                    print 'Warning: energies are inconsistent with num_nodes, using default value'
                    node_energy = default_energy
                else:
                    node_energy = energies[ctr]
            node_name = self.name + str(ctr)            
            self.nodes.append(Node(energy = node_energy, state = node_state, name = node_name))
            
    def __str__(self):
        layer_string = 'Layer "{0}"\n*************************\nNumber of nodes: {1}\n\n'.format(self.name,self.num_nodes)
        layer_string += 'Layer contains:\n-------------------\n'
        for node in self.nodes:
            layer_string += node.__str__()+'\n-------------------\n'
        return layer_string
    
    def update_nodes(self, new_states):
        for ctr, state in enumerate(new_states):
            self.nodes[ctr].update_state(state)
            
    def node_states(self):
        states = []
        for node in self.nodes:
            states.append(node.state)
        return states
            
class System(object):
    def __init__(self, name = None):
        self.name = name
        self.layers = {}
        self.couplings = {}
        
    def __str__(self):
        if self.name == None:
            system_string = 'Unnamed system'
        else: 
            system_string = 'System "{0}"'.format(self.name)
        system_string += ':\n============================\n\n'
        
        if len(self.layers) == 0:
            system_string += 'Currently no layers specified.'
        else:
            system_string += 'Layers:\n\n'
            for layer in self.layers.values():
                system_string += layer.__str__() + '\n'
        system_string += '*************************\n\n'
        
        if len(self.couplings.values()) == 0:
            system_string += 'Currently no couplings specified.\n\n'
        else:
            system_string += 'Couplings:\n\n'
            for name, coupling in self.couplings.items():
                system_string += name + ':\n'
                system_string += str(coupling)+'\n-------------------\n'
        
        return system_string
    
    def add_layer(self, num_nodes, states='default', energies='default', name = None):
        layer_name = name
        new_layer = Layer(num_nodes, states=states, energies=energies, name = layer_name)
        self.layers[layer_name]=new_layer
        
    def couple_layers(self, layerX, layerY, couplings):
        if layerX in self.layers.keys() and layerY in self.layers.keys():
            self.couplings[layerX+'_to_'+layerY]=couplings