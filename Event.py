class Event:
    
    def __init__(self, name, date, duration = None, notes = None):
        self.name = name
        self.date = date
        if duration: self.duration = duration
        else: self.duration = 0
        if notes: self.notes = notes
        else: self.notes = ''

        self.is_done = False
        self.synchronous = False
        self.notes_taken = False
        self.recorded = False
    
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