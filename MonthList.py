from Event import Event
class Month_List:
    
    def __init__(self):
        self.events = []
        self.month = ''

    
    def add_event(self, event):
        if not isinstance(event, Event):
            print("Placeholder for an error type")
        else:
            self.events.append(event)
    
    def delete_event(self):
        pass

    def give_events(self):
        for event in self.events:
            yield event

    def __iter__(self):
        return self.give_events()




