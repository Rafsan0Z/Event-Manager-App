from Event import Event
class Day:
    
    def __init__(self, month_name):
        self.date_num = None
        self.day_name = None
        self.month_name = month_name
        self.events = []

    def get_date_num(self):
        return self.date_num

    def get_day_name(self):
        return self.day_name
    
    def set_date_num(self, num):
        self.date_num = num
    
    def set_day_name(self, day):
        self.day_name = day
    
    def add_event(self, event):
        if not isinstance(event, Event):
            print("Placeholder for an ErrorType!")
        else:
            self.events.append(event)
    
    def delete_event(self):
        pass

    def give_events(self):
        for event in self.events:
            yield event
    
    def __iter__(self):
        return self.give_events()
    
    def num_events(self):
        return len(self.events)