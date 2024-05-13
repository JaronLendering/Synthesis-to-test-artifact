class Strategy:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child, line_name):
        self.children.append((child,line_name))

    def repr_as_image(self):
        pass
    def __repr__(self, level=0):
        rep = ("  " * level + self.name + "\n")
        for child, line_name in self.children:
            rep +=("  " * (level + 1) + f"---{line_name}---\n")
            rep += child.__repr__(level + 2)
        return rep
