from collections.abc import MutableSequence
from abc import ABC, abstractmethod
from Event import DocumentedEvent

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

    def get_change_string(self):
        return 'Undo' if self.done else 'Redo'

    @abstractmethod
    def undo(self):
        pass

    @abstractmethod
    def redo(self):
        pass

    def __str__(self):
        return f"------------------------------------------------[{self.get_change_string()}]\n"

class Add(Change):

    def __init__(self, event , year_num, month_name, day_name, date_num, db_handler):
        self.event = event
        self.year = year_num
        self.month = month_name
        self.day = day_name
        self.date = date_num
        self.db_handler = db_handler
        self.redo()

    def undo(self):
        # check if the yearlist has this event and if so remove it:
        self.done = False
                        
        
    def redo(self):
        #check if the yearlist doesn't have this event and if so, add it:
        year_list = self.db_handler.getYearList()
        year_list.add_event(self.event, self.year, self.month, self.day, self.date)
        self.done = True

    def __str__(self):
        result = super().__str__()
        result += 'Adding new event\n'
        result += f'Event name: {self.event.event_name}\n'
        result += f'Event start time: {self.event.time_string}\n'
        result += f'Event duration: {self.event.duration_string}\n'
        result += f'Event date: {self.day} the {self.date}, {self.month} of {self.year}\n'
        result += "------------------------------------------------\n"
        return result

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
        result = super().__str__()
        result += 'Editing event name\n'
        result += f'Original event name: {self.old_name}\n'
        result += f'New event name: {self.new_name}\n'
        result += "------------------------------------------------\n"
        return result
    
class EditTime(Change):

    def __init__(self, event, db_handler, start_time):
        super().__init__(event, db_handler)
        self.new_start_time = start_time
        self.old_start_time = event.time_string

    def undo(self):
        year_list = self.db_handler.getYearlist()
    
    def redo(self):
        pass

    def __str__(self):
        result = super().__str__()
        result += 'Editing event start time\n'
        result += f'Original event start time: {self.old_start_time}\n'
        result += f'New event time: {self.new_start_time}\n'
        result += "------------------------------------------------\n"
        return result
    

class EditDuration(Change):

    def __init__(self, event, db_handler, duration):
        super().__init__(event, db_handler)
        self.new_duration = duration
        self.old_duration = event.duration_string

    def undo(self):
        year_list = self.db_handler.getYearlist()
    
    def redo(self):
        pass

    def __str__(self):
        result = super().__str__()
        result += 'Editing event duration\n'
        result += f'Original event duration: {self.old_duration}\n'
        result += f'New event duration: {self.new_duration}\n'
        result += "------------------------------------------------\n"
        return result
    
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

    def add_event_change(self, event_name, time_string, duration_string, year_num, month_name, day_name, date_num, db_handler):
        new_event = DocumentedEvent(event_name, time_string, duration_string)
        add_change = Add(new_event, year_num, month_name, day_name, date_num, db_handler)
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