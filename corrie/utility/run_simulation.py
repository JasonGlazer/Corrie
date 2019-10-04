import os
import time
import subprocess
import json
import os.path
from pubsub import pub

from corrie.utility.openstudio_workflow import OpenStudioStep
from corrie.utility.openstudio_workflow import OpenStudioWorkFlow
from corrie.utility.update_presentation import UpdatePresentation


class RunSimulation(object):

    def __init__(self):
        pass

    def set_current_file_name(self, current_corrie_file_name):
        self.current_corrie_file_name = current_corrie_file_name
        root, ext = os.path.splitext(self.current_corrie_file_name)
        self.path_to_simulation_folder = root + "_simulations"
        if not os.path.exists(self.path_to_simulation_folder):
            os.mkdir(self.path_to_simulation_folder)

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
                    time.sleep(0.5)
                    work_flow = OpenStudioWorkFlow('./bar-seed.osm')
                    self.workflow_initial_steps(work_flow)
                    self.workflow_previous_steps(work_flow, workflow_arguments)
                    self.workflow_current_option(work_flow, option_name, osw_list, argument_value)
                    self.workflow_final_steps(work_flow)
                    work_flow.run_directory = self.combined_slide_option_name(slide_name, option_name)
                    root_name = self.root_filename_from_slide_option(slide_name, option_name)
                    osw_name = self.create_osw(root_name, work_flow)
                    print('osw_name: ',osw_name)
                    subprocess.run(['C:/openstudio-2.8.0/bin/openstudio.exe','run','-w', osw_name], cwd=self.path_to_simulation_folder)
                    #subprocess.run(['C:/openstudio-2.8.1-cli-ep/bin/openstudio.exe','run','-w', osw_name], cwd=self.path_to_simulation_folder)
                    #subprocess.run(['C:/openstudio-2.8.0/bin/openstudio.exe','run','-w', osw_name], cwd='C:/Users/jglaz/Documents/projects/SBIR SimArchImag/5 SimpleBox/os-test/bar-seed')
                    metric_value_for_option = self.get_output_metric_value(root_name)
                    # assuming "selection mode" is "automatic" will need something more sophisticated for other selection modes
                    if metric_value_for_option < selected_metric_value:
                        selected_metric_value = metric_value_for_option
                        selected_option = (option_name, osw_list, argument_value)
            if include_incremental:
                workflow_arguments.append(selected_option)

    def workflow_initial_steps(self, work_flow):
        arguments =  {"weather_file_name" : self.saved_data['weatherPath']}
        work_flow.add_step(OpenStudioStep('dg-ChangeBuildingLocation', arguments))

        arguments = {"bldg_type_a" : "MediumOffice",
            "ns_to_ew_ratio" : 0.9,
            "building_rotation": 0,
            "num_stories_above_grade" : 2,
            "num_stories_below_grade" : 0,
            "template" : self.saved_data['baselineCode'].replace('ASHRAE ', ''),
            "total_bldg_floor_area" : 11000,
            "wwr" : 0.33}
        work_flow.add_step(OpenStudioStep('CreateBarFromBuildingTypeRatios', arguments))

        arguments =  {
            "system_type" : "PSZ-AC with gas coil heat",
            "template" : self.saved_data['baselineCode'].replace('ASHRAE ', '')
         }
        work_flow.add_step(OpenStudioStep('CreateTypicalBuildingFromModel', arguments))


    def workflow_previous_steps(self, work_flow, workflow_arguments):
        for workflow_argument in workflow_arguments:
            option_name, osw_list, argument_value = workflow_argument
            self.workflow_current_option(work_flow, option_name, osw_list, argument_value)

    def workflow_current_option(self, work_flow, option_name, osw_list, argument_value):
        print('option_name', option_name)
        print('osw_list', osw_list)
        print('argument_value', argument_value)
        print('---------')
        for osw_item in osw_list:
            measure_dir_name, argument_key = osw_item
            work_flow.add_argument_value(measure_dir_name, argument_key, argument_value)

    def workflow_final_steps(self, work_flow):
        work_flow.add_step(OpenStudioStep('OpenStudioResults',{}))

    def create_osw(self, root_name, work_flow):
        workflow_dictionary = work_flow.return_workflow_dictionary()
        # print(json.dumps(workflow_dictionary, indent=4))
        osw_name = root_name + ".osw"
        with open(osw_name, 'w') as f:
            json.dump(workflow_dictionary, f, indent=4)
        return osw_name

    def collect_results(self):
        slide_details = self.saved_data['slideDetails']
        slide_order = self.saved_data['slideOrder']
        running_slides = [slide_name for slide_name, should_run in slide_order if should_run]
        self.collected_results = {}
        for slide_name in running_slides:
            selection_mode, include_incremental, options_list, osw_list = slide_details[slide_name]
            option_results = {}
            for option_name, enabled_option, argument_value in options_list:
                if enabled_option:
                    root_name = self.root_filename_from_slide_option(slide_name, option_name)
                    # print('root_name: ',root_name)
                    base, tail = os.path.split(root_name)
                    run_folder_name = os.path.join(base, 'run-' + tail)
                    result_json_file_name = os.path.join(run_folder_name, 'results.json')
                    # print('result_json_file_name: ', result_json_file_name)
                    if os.path.exists(result_json_file_name):
                        with open(result_json_file_name, 'r') as results_file:
                            results_data = json.load(results_file)
                            os_results = results_data['OpenStudioResults']
                            # print(os_results)
                            net_site_energy = os_results['net_site_energy']
                            print('For [{}--{}] the net_site_energy:  {}'.format(slide_name, option_name,net_site_energy))
                            option_results[option_name] = os_results
            self.collected_results[slide_name] = option_results
        # print('collected_results: ', collected_results)
        return self.collected_results

    def populate_excel(self, results):
        # maybe this belongs in a different class
        pass

    def populate_powerpoint(self):
        update_presentation = UpdatePresentation(self.saved_data, self.collected_results, self.current_corrie_file_name)
        # update_presentation.test1()
        update_presentation.create_slides()


    def root_filename_from_slide_option(self, slide_name, option_name):
        clean_file_name = self.combined_slide_option_name(slide_name, option_name)
        root_file_name_path = os.path.join(self.path_to_simulation_folder, clean_file_name)
        return root_file_name_path

    def combined_slide_option_name(self, slide_name, option_name):
        file_name = "{}__{}".format(slide_name, option_name)
        clean_file_name = self.remove_invalid_file_characters(file_name)
        return clean_file_name

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
