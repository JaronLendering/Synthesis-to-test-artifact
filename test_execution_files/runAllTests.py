import os
import subprocess


if __name__ == "__main__":


    skip = [] # array of tests to skip
    for i in range(13):
        if i not in skip:
            arguments = [str(i),"--save_strategy"] #test index and if the strategy should be saved
            command = ["cmd", "/c", "start", "cmd", "/k", "python", os.path.join(os.path.dirname(os.path.abspath(__file__)), "specificationTests.py")] + arguments
            subprocess.Popen(command)

    skip = [0,1,2,9]
    for i in range(13):
        if i not in skip:
            arguments = [str(i),"--save_strategy","--better_MCTS"] #test index and if the strategy should be saved
            command = ["cmd", "/c", "start", "cmd", "/k", "python", os.path.join(os.path.dirname(os.path.abspath(__file__)), "specificationTests.py")] + arguments
            subprocess.Popen(command)

    exit(808)