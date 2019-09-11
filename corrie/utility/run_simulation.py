import os
import time
import subprocess
import json
from pubsub import pub

from corrie.utility.openstudio_workflow import OpenStudioStep
from corrie.utility.openstudio_workflow import OpenStudioWorkFlow


class RunSimulation(object):

    def __init__(self, saved_data):
        self.saved_data = saved_data
        print(saved_data)

    def run_simulations(self):
        slide_details = self.saved_data['slideDetails']
        slide_order = self.saved_data['slideOrder']
        # determine number of total simulations
        total_simulation_count = 0
        running_slides = [slide_name for slide_name, should_run in slide_order if should_run]
        for slide_name in running_slides:
            selection_mode, include_incremental, options_list, osw_list = slide_details[slide_name]
            for option_name, enabled_option, argument_value in options_list:
                if enabled_option:
                    total_simulation_count = total_simulation_count + 1
        # now perform actual simulations
        count = 0
        # initial workflow arguments
        workflow_arguments = []
        for slide_name in running_slides:
            selection_mode, include_incremental, options_list, osw_list = slide_details[slide_name]
            selected_metric_value = 1.0e+300
            selected_option = ''
            for option_name, enabled_option, argument_value in options_list:
                if enabled_option:
                    count = count + 1
                    pub.sendMessage('listenerUpdateStatusBar', message='Simulation {} of {}:  {} >>> {} '.format(count, total_simulation_count, slide_name, option_name))
                    time.sleep(1)
                    root_name = self.root_filename_from_slide_option(slide_name, option_name)
                    self.create_osw(root_name, option_name, workflow_arguments, osw_list, argument_value)
                    # subprocess.run(['C:/openstudio-2.8.1-cli-ep/bin/openstudio.exe','run','-w', 'workflow.osw'], cwd='C:/Users/jglaz/Documents/projects/SBIR SimArchImag/5 SimpleBox/os-test/bar-test03_cli')
                    metric_value_for_option = self.get_output_metric_value(root_name)
                    # assuming "selection mode" is "automatic" will need something more sophisticated for other selection modes
                    if metric_value_for_option < selected_metric_value:
                        selected_metric_value = metric_value_for_option
                        selected_option = (option_name, osw_list, argument_value)
            if include_incremental:
                workflow_arguments.append(selected_option)


    def create_osw(self, root_name, option_name, workflow_arguments, osw_list, argument_value):
        work_flow = OpenStudioWorkFlow('../bar-seed.osm')
        work_flow.add_step(OpenStudioStep('dg-ChangeBuildingLocation',
                                          {"weather_file_name" : self.saved_data['weatherPath']}))
        arguments = {"bldg_type_a" : "MediumOffice",
            "ns_to_ew_ratio" : 0.9,
            "num_stories_above_grade" : 2,
            "template" : self.saved_data['baselineCode'],
            "total_bldg_floor_area" : 11000,
            "wwr" : 0.33}
        work_flow.add_step(OpenStudioStep('CreateBarFromBuildingTypeRatios', arguments))
        work_flow.add_step((OpenStudioStep('OpenStudioResults',{})))
        workflow_dictionary = work_flow.return_workflow_dictionary()
        # print(json.dumps(workflow_dictionary, indent=4))
        osw_name = root_name + ".osw"
        with open(osw_name, 'w') as f:
            json.dump(workflow_dictionary, f, indent=4)

    def collected_results(self):
        return ['list_of_results',]

    def populate_excel(self, results):
        # maybe this belongs in a different class
        pass

    def populate_powerpoint(self, results):
        # maybe this belongs in a different class
        pass

    def root_filename_from_slide_option(self, slide_name, option_name):
        file_name = "{}__{}".format(slide_name, option_name)
        clean_file_name = self.remove_invalid_file_characters(file_name)
        root_file_name_path = os.path.join('C:/Users/jglaz/Documents/projects/SBIR SimArchImag/5 SimpleBox/os-test/bar-seed', clean_file_name)
        return root_file_name_path

    def remove_invalid_file_characters(self, file_name):
        # https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file
        newname = file_name.replace('<', '')
        newname = newname.replace('>', '')
        newname = newname.replace(':', '')
        newname = newname.replace('"', '')
        newname = newname.replace('/', '')
        newname = newname.replace('\\', '')
        newname = newname.replace('|', '')
        newname = newname.replace('?', '')
        newname = newname.replace('*', '')
        # some other special characters not explicitly excluded
        newname = newname.replace('#', '')
        newname = newname.replace('%', '')
        newname = newname.replace('$', '')
        newname = newname.replace('=', '')
        newname = newname.replace('.', '')
        # just get rid of spaces too to make them a little easier deal with
        newname = newname.replace(' ', '_')
        return newname

    def get_output_metric_value(self, root_name):
        return 0
