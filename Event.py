from datetime import timedelta as dur

class Event:

    def __init__(self, name, time_string = '', duration_string = '', notes_string = ''):
        self.event_name = name

        self.time_string = time_string
        self.process_time_string()

        self.duration_string = duration_string
        self.process_duration_string()

        self.notes_string = notes_string
        self.__process_notes_string()

        self.is_done = False
        self.synchronous = False
        self.recorded = False
        self.notes_taken = False

    def __str__(self):
        duration_print = '' if not self.duration_string else ' for ' + self.duration_string
        event_line = "At {time}, {name}{duration}. Notes: \n".format(
            time = self.time_string,
            name = self.event_name,
            duration = duration_print,
        )
        if not len(self.notes):
            return event_line + "Nothing at this time\n"
        notes_lines = ''
        for note in self.notes:
            notes_lines += '(*) ' + note + '\n'
        return event_line + notes_lines
    
    def process_time_string(self):
        return 
    
    def process_duration_string(self):
        hours = 0
        mins = 0

        duration_block = self.duration_string.split()
        if 'hour' in duration_block or 'hours' in duration_block:
            hours = int(duration_block[0].strip())
        if 'min' in duration_block or 'mins' in duration_block:
            mins = int(duration_block[-2].strip())
        
        self.duration = dur(hours=hours, minutes=mins)

    def __process_notes_string(self):
        self.notes = []
        note_block = self.notes_string.split('and')
        last_note = note_block[-1].strip()
        other_notes = " ".join(note_block[:-1])
        for each in other_notes.split(','):
            if each.strip():
                self.notes.append(each.strip())
        if last_note: self.notes.append(last_note)

    
    def edit_duration_string(self, string):
        self.duration_string = string
        self.process_duration_string()

    def edit_name(self, name):
        self.name = name

    def edit_duration(self, hours = 0, mins = 0):
        self.duration = dur(hours=hours, minutes=mins)

    def add_notes(self, extra_notes):
        for note in extra_notes.strip().split(','):
            if note: self.notes.append(note)

    def delete_notes(self):
        self.notes = []

    def edit_time(self, time_string):
        self.process_time_string(time_string)

    def set_host(self, host):
        self.host = host


class DocumentedEvent(Event):

    def add_start_index(self, index):
        self.__start_index = index

    def add_end_index(self, index):
        self.__end_index = index

    def enableEditToken(self):
        self.__edit = True
    
    def disableEditToken(self):
        self.__edit = False

    def enableChangedToken(self):
        self.__changed = True

    def disableChangedToken(self):
        self.__changed = False


# Plan for the above mentioned class:
# When an in app change has been made
# Turn on the edit token when an edit is made
# When the app is closing, check for this token, and flush those changes to the doc
# The changed token is an optimization tool
# So indices will not have to be re-loaded for tabs or subtabs 
# After re-loading the indices the changed token will be set off