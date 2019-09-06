

class SlideSpecification(object):

    def __init__(self, slide_name, measure_name):
        self.slide_name = slide_name
        self.measure_name = measure_name
        self.options = []
        self.argument_from_option = {}

    def add_option(self, option_specification):
        self.options.append(option_specification)
        self.argument_from_option[option_specification.option_display_string] = option_specification.argument_value


class OptionSpecification(object):

    def __init__(self, option_display_string, default_enabled, argument_value):
        self.option_display_string = option_display_string
        self.default_enabled = default_enabled
        self.argument_value = argument_value





