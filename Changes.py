from collections.abc import MutableSequence
from abc import ABC, abstractmethod

class Change(ABC):

    def __init__(self, event, db_handler):
        self.load_event_info(event)
        self.db_handler = db_handler
        self.set_index()

    def set_index(self):
        self.year_list = self.db_handler.getYearList()

    def load_event_info(self, event):
        if not (event.year_num and event.month_name and event.day_name and event.date_num):
            print("Event lacks the necessary info")
            del self
            return
        else:
            self.event = event
            self.year_num = event.year_num 
            self.month_name = event.month_name 
            self.date_num = event.date_num
            self.day_name = event.day_name 

    @abstractmethod
    def undo(self):
        pass

    @abstractmethod
    def redo(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

class Add(Change):

    def undo(self):
        # check if the yearlist has this event and if so remove it:
        pass
        
    def redo(self):
        #check if the yearlist doesn't have this event and if so, add it:
        pass

    def __str__(self):
        return 'Adding event'

class Remove(Add):

    def undo(self):
        super().redo()

    def redo(self):
        super().undo()

    def __str__(self):
        return 'Removing event'

class EditName(Change):

    def __init__(self, event, db_handler, name):
        super().__init__(event, db_handler)
        self.new_name = name
        self.old_name = self.event.event_name

    def undo(self):
        year_list = self.db_handler.getYearList()
        # find the event based on the yearlist and if it exists:
        # see if the event name is the new_name and if so:
        # set event's name equal to self.old_name

    def redo(self):
        pass

    def __str__(self):
        result = "------------------------------------------------\n"
        result += 'Editing event name\n'
        result += f'{self.event}\n'
        result += "------------------------------------------------\n"
        return result
    
class EditTime(Change):

    def __init__(self, event, db_handler, start_time):
        super().__init__(event, db_handler)
        self.new_start_time = start_time
        self.old_start_time = event.start_time

    def undo(self):
        year_list = self.db_handler.getYearlist()
    
    def redo(self):
        pass

    def __str__(self):
        return 'Editing event time'
    

class EditDuration(Change):

    def __init__(self, event, db_handler, duration):
        super().__init__(event, db_handler)
        self.new_duration = duration
        self.old_duration = event.duration

    def undo(self):
        year_list = self.db_handler.getYearlist()
    
    def redo(self):
        pass

    def __str__(self):
        return 'Editing event duration'
    
class EditNotes(Change):

    def __init__(self, event, db_handler, note_index, note):
        super().__init__(event, db_handler)
        self.new_note = note
        self.old_note = event.notes
        self.note_index = note_index

    def undo(self):
        pass

    def redo(self):
        pass

    def __str__(self):
        return 'Editing event notes'

class ChangeList(MutableSequence):

    def __init__(self):
        self.changes = []

    def __len__(self):
        return len(self.changes)
    
    def __getitem__(self, index):
        return self.changes[index]
    
    def __setitem__(self, index, change):
        self.changes[index] = change

    def __delitem__(self, index):
        del self.changes[index]

    def insert(self, index, change):
        self.changes.insert(index, change)

    def add_event_change(self, event, db_handler):
        add_change = Add(event, db_handler)
        self.changes.append(add_change)

    def remove_event_change(self, event, db_handler):
        remove_change = Remove(event, db_handler)
        self.changes.append(remove_change)

    def edit_name_change(self, event, db_handler, new_name):
        name_change = EditName(event, db_handler, new_name)
        self.changes.append(name_change)
    
    def edit_duration_change(self, event, db_handler, new_duration):
        duration_change = EditDuration(event, db_handler, new_duration)
        self.changes.append(duration_change)

    def edit_time_change(self, event, db_handler, new_start_time):
        time_change = EditTime(event, db_handler, new_start_time)
        self.changes.append(time_change)


    # def __str__(self):
    #     result = 'Here are all the changes queued: \n'
    #     index = 1
    #     for change in self.changes:
    #         result += f'{index} {change} \n'
    #         index += 1
    #     return result