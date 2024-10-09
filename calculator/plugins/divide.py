class DivideCommand:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.result = None  

    def execute(self):
        if self.b == 0:
            self.result = "Cannot divide by zero."
        else:
            self.result = self.a / self.b  
        return self.result
