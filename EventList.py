from collections.abc import MutableSequence
from EventExceptions import NotAnEventException
from Event import Event

class EventList(MutableSequence):
    
    def __init__(self):
        self.events = []

    def __len__(self):
        return len(self.events)
    
    def num_events(self):
        return self.__len__()

    def __getitem__(self):
        pass

    def __setitem__(self):
        pass

    def __delitem__(self):
        pass

    def insert(self):
        pass

    def add_event(self, event):
        if not isinstance(event, Event):
            raise NotAnEventException(event)
        self.append(event)

    def delete_event(self, event):
        pass

    def give_events(self):
        for event in self.events:
            yield event

    def __iter__(self):
        return self.give_events()
