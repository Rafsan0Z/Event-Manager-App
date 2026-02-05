class Event:

    def __init__(self, name, time_string = None, duration_string = None, notes_string = None):
        self.event_name = name
        if time_string: self.start_time = self.process_time_string(time_string)
        else: self.start_time = '12am'
        if duration_string: self.duration = self.process_duration_string(duration_string)
        else: self.duration = 0
        if notes_string: self.notes = self.process_notes_string(notes_string)
        else: self.notes = ''

        self.is_done = False
        self.synchronous = False
        self.recorded = False
        self.notes_taken = False

    def __str__(self):
        return "{name} ({duration}) [{notes}]".format(name=self.name,duration=self.duration,notes=self.notes)
    
    def process_time_string(self, time_string):
        pass
    
    def process_duration_string(self, duration_string):
        pass

    def process_notes_string(self, notes_string):
        pass
    
    def edit_name(self):
        pass

    def edit_duration(self):
        pass

    def add_notes(self):
        pass

    def delete_notes(self):
        self.notes = ''

    def edit_time(self):
        pass

    def edit_date(self):
        pass

    def set_host(self, host):
        self.host = host