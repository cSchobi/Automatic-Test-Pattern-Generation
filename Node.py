class Node(object):

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

class InNode(Node):

    def __init__(self, name):
        super().__init__(name)

class OutNode(Node):
    
    def __init__(self, name):
        super().__init__(name)
    
class InteriorNode(Node):
    pass

class GateInNode(InteriorNode):

    def __init__(self, name):
        super().__init__(name)

class GateOutNode(InteriorNode):
    
    def __init__(self, name):
        super().__init__(name)
