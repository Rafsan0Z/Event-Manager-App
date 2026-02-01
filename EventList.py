from collections.abc import MutableSequence
from EventExceptions import NotAnEventException
from Event import Event

class EventList(MutableSequence):
    
    def __init__(self):
        self.events = []

    def __len__(self):
        return len(self.events)
    
    def num_events(self):
        return len(self)

    def __getitem__(self, i):
        return self.events[i]

    def check_event_type(self, event_candidate):
        if not isinstance(event_candidate, Event):
            raise NotAnEventException(event_candidate)

    def __setitem__(self, i, event):
        self.check_event_type(event)
        self.events[i] = event

    def __delitem__(self, i):
        del self.events[i]

    def insert(self, i, event):
        self.check_event_type(event)
        self.events.insert(i, event)

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
