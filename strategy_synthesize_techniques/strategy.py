class Strategy:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child, transition):
        self.children.append((child, transition))

    def repr_as_image(self):
        pass
    def __repr__(self, level=0):
        rep = ("  " * level + self.name + "\n")
        for child, line_name,isInput in self.children:
            rep +=("  " * (level + 1) + f"---{line_name}{'!' if isInput else '0'}---\n")
            rep += child.__repr__(level + 2)
        return rep

    def process_input(self, transition_value):
        for child,transition in self.children:
            if (transition == transition_value): #TODO: make it check if a transition is in a message or is the message
                print(f"Transition: {self} --({transition_value})--> {child}")
                return child
        raise Exception(f"No valid transition for input '{transition_value}' in node '{self}'.")
