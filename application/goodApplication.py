import random

from application.abstractApplication import AbstractApplication


class GoodApplication(AbstractApplication):
    def last_line_state(self):
        self.print_ouput("long line finish")

    def run(self):
        user_input,program_output = self.do_IO_actions(lambda: "None")
        if(user_input == "lines"):
            user_input,program_output = self.do_IO_actions(lambda: "None")
            if(user_input == "go0"):
                for i in range(20):
                    user_input, program_output = self.do_IO_actions(lambda: "None")
                    if(user_input != "go0"):
                        exit() # go1 is the only one in the specs, so I just break out of it when it is not go1, it doesn't matter what i do anyways
            if (user_input == "go1"):
                for i in range(20):
                    user_input, program_output = self.do_IO_actions(lambda: "None")
                    if (user_input != "go1"):
                        exit()
            if (user_input == "go2"):
                for i in range(20):
                    user_input, program_output = self.do_IO_actions(lambda: "None")
                    if (user_input != "go2"):
                        exit()
            else:
                exit() # go1 is the only one in the specs, so I just break out of it when it is not go1, it doesn't matter what i do anyways
            self.last_line_state()

        elif(user_input == "choices"):
            self.choice(0,4,"")
            pass
        elif user_input == "loop":
            while True:
                user_input, output = self.do_IO_actions(lambda: None if random.random() < 0.1 else 'L1', True)
                if output == 'L1':
                    self.do_IO_actions(lambda: "L1 back")
                elif output == None:
                    if user_input == 'L2':
                        self.do_IO_actions(lambda: "L2 back")



    def choice(self,dept, max_dept, choice_num):
        if dept < max_dept:
            user_input, program_output = self.do_IO_actions(lambda : "None")#self.do_IO_actions(lambda:random.choice([f"next{choice_num}2",f"next{choice_num}3",f"next{choice_num}4", "None"]))

            if( program_output == f"next{choice_num}2" or program_output == f"next{choice_num}3" or program_output == f"next{choice_num}4" ):
                self.choice(dept+1,max_dept,program_output[4:])
                return
            elif(program_output == "None"):
                if user_input == f"next{choice_num}0" or user_input == f"next{choice_num}1":
                    self.choice(dept+1, max_dept, user_input[4:])
                    return

            exit()



