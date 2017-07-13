class Section(object):

    def __init__(self, name, range_start, range_end, jobs):
        self.name = name
        self.range_start = range_start
        self.range_end = range_end
        self.jobs = jobs


class Led(object):

    def __init__(self, primary_color, secondary_color):
        self.primary_color = primary_color
        self.secondary_color = secondary_color


class Job(object):

    def __init__(self, name, pipeline=False):
        self.name = name
        self.pipeline = pipeline
        self.building = False
