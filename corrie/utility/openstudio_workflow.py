import datetime


class OpenStudioWorkFlow(object):

    run_directory = 'run'

    def __init__(self, seed_file):
        self.steps = []
        self.seed_file = seed_file

    def add_step(self, next_step):
        self.steps.append(next_step)

    def add_argument_value(self, measure_dir_name, argument_key, argument_value):
        found = False
        for step in self.steps:
            if step.measure_dir_name == measure_dir_name:
                step.arguments[argument_key] = argument_value
                found = True
                break
        if not found:
            argument_dict = {}
            argument_dict[argument_key] = argument_value
            new_step = OpenStudioStep(measure_dir_name, argument_dict)
            self.steps.append(new_step)

    def return_workflow_dictionary(self):
        dictionary = {}
        dictionary['seed_file'] = self.seed_file
        dictionary['run_directory'] = 'run-'+ self.run_directory
        # dictionary['measure_paths'] = ['C:\\Users\\jglaz\\Documents\\projects\\SBIR SimArchImag\\5 SimpleBox\\os-test\\bar-seed\\measure\\',]
        dictionary['measure_paths'] = ['D:/SBIR/measures/',]
        # next line based on https://stackoverflow.com/questions/2150739/iso-time-iso-8601-in-python
        dictionary['created_at'] = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        list_of_steps = []
        for step in self.steps:
            list_of_steps.append(step.return_step_dictionary())
        dictionary['steps'] = list_of_steps
        return dictionary


class OpenStudioStep(object):

    def __init__(self, measure_dir_name, arguments):
        self.arguments = arguments
        # self.measure_dir_name = 'C:\\Users\\jglaz\\Documents\\projects\\SBIR SimArchImag\\5 SimpleBox\\os-test\\bar-seed\\measure\\' + measure_dir_name
        # self.measure_dir_name = 'D:/SBIR/measures/' + measure_dir_name
        self.measure_dir_name =  measure_dir_name

    def return_step_dictionary(self):
        step = {}
        step['arguments'] = self.arguments
        step['measure_dir_name'] = self.measure_dir_name
        return step
