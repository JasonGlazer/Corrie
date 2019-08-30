import datetime


class OpenStudioWorkFlow(object):

    def __init__(self, seed_file):
        self.steps = []
        self.seed_file = seed_file

    def add_step(self, next_step):
        self.steps.append(next_step)

    def return_workflow_dictionary(self):
        dictionary = {}
        dictionary['seed_file'] = self.seed_file
        # next line based on https://stackoverflow.com/questions/2150739/iso-time-iso-8601-in-python
        dictionary['created_at'] = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        list_of_steps = []
        for step in self.steps:
            list_of_steps.append(step.return_step_dictionary())
        dictionary['steps'] = list_of_steps
        return dictionary


class OpenStudioStep(object):

    def __init__(self, name, measure_dir_name, arguments):
        self.arguments = arguments
        self.name = name
        self.measure_dir_name = measure_dir_name

    def return_step_dictionary(self):
        step = {}
        step['name'] = self.name
        step['measure_dir_name'] = self.measure_dir_name
        step['arguments'] = self.arguments
        return step
