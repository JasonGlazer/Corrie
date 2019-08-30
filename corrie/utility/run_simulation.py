import os
import time
import subprocess
import json

from corrie.utility.openstudio_workflow import OpenStudioStep
from corrie.utility.openstudio_workflow import OpenStudioWorkFlow

class RunSimulation(object):

    def __init__(self, saved_data):
        self.saved_data = saved_data
        print(saved_data)

    def list_of_simulations(self):
        sim_names = []
        slide_details = self.saved_data['slideDetails']
        slide_order = self.saved_data['slideOrder']
        for slide_name, should_run in slide_order:
            if should_run:
                selection_mode, include_incremental, options = slide_details[slide_name]
                for option_name, enabled_option in options:
                    if enabled_option:
                        sim_names.append((slide_name,option_name))
        #for sim in sim_names:
        #    print(sim)
        return sim_names

    def run_open_studio(self,sim_name):
        time.sleep(2)

        # osw_file_name, results_path = setup_open_studio_workflow_file(sim_name)
        # run_openstudio(osw_file_name, working_path, openstudio_path)
        # simulation_results = extract_results(results_path)
        # collect_results.append(sim_name, simulation_results)
        # - after this populate the excel and powerpoint files

        #subprocess.run(['i:/openstudio-2.8.0/bin/openstudio','run','-w', 'workflow-min.osw'], cwd='D:/projects/SBIR SimArchImag/5 SimpleBox/os-test/emptyCLI')
        #subprocess.run(['I:/openstudio-2.8.1-cli-only/bin/openstudio.exe','run','-w', 'workflow.osw'], cwd='D:/projects/SBIR SimArchImag/5 SimpleBox/os-test/bar-test02_cli')
        #subprocess.run(['C:/openstudio-2.8.1-cli-ep/bin/openstudio.exe','run','-w', 'workflow.osw'], cwd='C:/Users/jglaz/Documents/projects/SBIR SimArchImag/5 SimpleBox/os-test/bar-test02_cli')
        self.create_osw()
        #subprocess.run(['C:/openstudio-2.8.1-cli-ep/bin/openstudio.exe','run','-w', 'workflow.osw'], cwd='C:/Users/jglaz/Documents/projects/SBIR SimArchImag/5 SimpleBox/os-test/bar-test03_cli')
        ""

    def create_osw(self):
        work_flow = OpenStudioWorkFlow('../bar-seed.osm')
        work_flow.add_step(OpenStudioStep('ChangeBuildingLocation','dg-ChangeBuildingLocation',{"weather_file_name" : "C:\\EnergyPlusV9-1-0\\WeatherData\\USA_CO_Golden-NREL.724666_TMY3.epw"}))
        arguments = {"bldg_type_a" : "MediumOffice",
            "ns_to_ew_ratio" : 0.9,
            "num_stories_above_grade" : 2,
            "template" : "90.1-2007",
            "total_bldg_floor_area" : 11000,
            "wwr" : 0.33}
        work_flow.add_step(OpenStudioStep('Create Bar From Building Type Ratios','CreateBarFromBuildingTypeRatios',arguments))
        work_flow.add_step((OpenStudioStep('OpenStudio Results', 'OpenStudioResults',{})))
        workflow_dictionary = work_flow.return_workflow_dictionary()
        # print(json.dumps(workflow_dictionary, indent=4))
        osw_file_name = 'C:/Users/jglaz/Documents/projects/SBIR SimArchImag/5 SimpleBox/os-test/bar-seed/workflow.osw'
        with open(osw_file_name, 'w') as f:
            json.dump(workflow_dictionary, f, indent=4)

    def collected_results(self):
        return ['list_of_results',]

    def populate_excel(self, results):
        # maybe this belongs in a different class
        pass

    def populate_powerpoint(self, results):
        # maybe this belongs in a different class
        pass