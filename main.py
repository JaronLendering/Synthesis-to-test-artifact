from strategy import Strategy

if __name__ == "__main__":
    root = Strategy("Root")

    child1 = Strategy("Child 1")
    child2 = Strategy("Child 2")

    root.add_child(child1,"1")
    root.add_child(child2,"2")

    child1.add_child(Strategy("Child 1.1"),"1.1")
    child1.add_child(Strategy("Child 1.2"), "1.2")

    child2.add_child(Strategy("Child 2.1"), "2.1")

    print(root)