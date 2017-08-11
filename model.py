class Section(object):

    def __init__(self, name, range_start, range_end, jobs):
        self.name = name
        self.range_start = range_start
        self.range_end = range_end
        self.jobs = jobs


class Led(object):

    def __init__(self, primary_color, secondary_color=None):
        self.primary_color = primary_color
        self.secondary_color = secondary_color


class Job(object):

    def __init__(self, name, pipeline=False):
        self.name = name
        self.pipeline = pipeline
        self.building = False


class SectionState(object):

    def __init__(self, state, building=False):
        self.state = state
        self.intValue = self.state_to_numbers(state)
        self.building = building

    states = {
        "FAILURE": -5,
        "UNSTABLE": -3,
        "ABORTED": -1,
        "SUCCESS": 1,
    }

    def number_to_state(self, number):
        for key, value in self.states.iteritems():
            if number == value:
                return key

    def state_to_numbers(self, state):
        return self.states.get(state, -1)
