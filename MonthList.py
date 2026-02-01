from Event import Event
class Month_List:
    
    def __init__(self, month_name):
        self.events = []
        self.month = month_name

    
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




