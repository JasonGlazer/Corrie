import os
import time
import subprocess



class RunSimulation(object):

    def __init__(self, saved_data):
        self.saved_data = saved_data
        print(saved_data)

    def list_of_simulations(self):
        sim_names = ['wwr01', 'wwr02', 'wwr03']
        print(sim_names)
        return sim_names

    def run_open_studio(self,sim_name):
        #time.sleep(2)

        # osw_file_name, results_path = setup_open_studio_workflow_file(sim_name)
        # run_openstudio(osw_file_name, working_path, openstudio_path)
        # simulation_results = extract_results(results_path)
        # collect_results.append(sim_name, simulation_results)
        # - after this populate the excel and powerpoint files

        #subprocess.run(['i:/openstudio-2.8.0/bin/openstudio','run','-w', 'workflow-min.osw'], cwd='D:/projects/SBIR SimArchImag/5 SimpleBox/os-test/emptyCLI')
        #subprocess.run(['I:/openstudio-2.8.1-cli-only/bin/openstudio.exe','run','-w', 'workflow.osw'], cwd='D:/projects/SBIR SimArchImag/5 SimpleBox/os-test/bar-test02_cli')
        subprocess.run(['C:/openstudio-2.8.1-cli-ep/bin/openstudio.exe','run','-w', 'workflow.osw'], cwd='C:/Users/jglaz/Documents/projects/SBIR SimArchImag/5 SimpleBox/os-test/bar-test02_cli')
        ""

    def collected_results(self):
        return ['list_of_results',]

    def populate_excel(self, results):
        # maybe this belongs in a different class
        pass

    def populate_powerpoint(self, results):
        # maybe this belongs in a different class
        pass