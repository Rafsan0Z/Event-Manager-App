from collections.abc import MutableSequence
from EventExceptions import NotAnEventException
from datetime import timedelta as dur
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
        
    def does_event_exist(self, new_event):
        for event in self.events:
            if event == new_event: return True
        return False


    def __setitem__(self, i, event):
        self.check_event_type(event)
        self.events[i] = event

    def __delitem__(self, i):
        del self.events[i]

    def __insert_pos(self, new_event):
        index = 0
        for event in self.events:
            if new_event.start_time <= event.start_time:
                break
            index += 1
        return index

    def insert(self, i, event):
        self.check_event_type(event)
        if self.does_event_exist(event): return
        index = self.__insert_pos(event)
        self.events.insert(index, event)

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
    
    def total_duration(self):
        total_time = dur()
        for event in self.events:
            total_time += event.duration
        return total_time

    def __str__(self):
        result = ''
        event_index = 0
        for event in self.events:
            result += str(event_index + 1) + ". " + str(event) + '\n'
            event_index += 1
        return result