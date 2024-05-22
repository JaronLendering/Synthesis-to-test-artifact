from catchStateChanges import catchStateChanges
class DummyApplication:
    def __init__(self):
        pass

    def output(self,output):
        print(output)

    def startMusic(self):
        print("startMusic")

    def stopMusic(self):
        print("stopMusic")

    def run(self):
        startNumber = input('give 0 for starting music and 1 for stopping music')
        if(startNumber == '0'):
            self.startMusic()
        elif(startNumber == '1'):
            self.stopMusic()

if __name__ == '__main__':
    app = DummyApplication()
    output_catcher = catchStateChanges()
    output_catcher.catchPrintMessages()
    app.run()
    print(output_catcher.print_log)