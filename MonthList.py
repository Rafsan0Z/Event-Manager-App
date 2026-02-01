from Event import Event
from Day import Day

class Month_List:
    
    def __init__(self, month_name):
        self.month = month_name
        self.days = []

    def num_events(self):
        total = 0
        for day in self.days:
            total += day.num_events()
        return total 

    def __str__(self):
        result = self.month + '\n'
        for day in self.days:
            result += "------------------------------\n"
            result += "For the day {name}:\n".format(name=day.get_day_name() + " " + day.get_date_num())
            event_index = 0
            for event in day:
                result += "{index}. {detail}\n".format(index=event_index+1, detail=event)
            result += "------------------------------\n"






