class Section(object):

    def __init__(self, name, range_start, range_end, project_names):
        self.name = name
        self.range_start = range_start
        self.range_end = range_end
        self.project_names = project_names


class Led(object):

    def __init__(self, primary_color, secondary_color):
        self.primary_color = primary_color
        self.secondary_color = secondary_color
