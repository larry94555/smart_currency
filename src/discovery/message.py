class Message:
    def __init__(self, message=None):
        print(f"Message::init")
        self.subject = message

    def getSubject(self):
        return self.subject
        
