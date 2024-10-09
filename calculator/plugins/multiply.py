class MultiplyCommand:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.result = None  

    def execute(self):
        self.result = self.a * self.b  
        return self.result

