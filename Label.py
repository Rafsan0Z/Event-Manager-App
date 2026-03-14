class Label:

    def __init__(self, name = ""):
        self.name = name
        if name != '' and name == str.upper(name):
            self.type = "Default"
        elif name != '':
            self.type = "Custom"
        else:
            self.type = "ERROR"
        self.sub_labels = None
    
    def set_name(self, name):
        self.name = name

    def __init_subLabels(self):
        self.sub_labels = []
    
    def add_sublabels(self, add):
        if not self.sub_labels:
            self.__init_subLabels()
        if isinstance(add, str):
            self.sub_labels.append(Label(add))
        elif isinstance(add, Label):
            self.sub_labels.append(add)
    
    def __str__(self):
        result = f'{self.name}, a {self.type} label'
        if self.sub_labels:
            result += ' with the following sub labels: \n'
            index = 1
            for label in self.sub_labels:
                result += f'   {index}. {label.name}\n'
                index += 1
        return result