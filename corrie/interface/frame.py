import wx
import json
import os
import sys
from pubsub import pub


from corrie.interface import general_options
from corrie.utility.run_simulation import RunSimulation
from corrie.utility.initialize_data import InitializeData

# wx callbacks need an event argument even though we usually don't use it, so the next line disables that check
# noinspection PyUnusedLocal
class CorrieFrame(wx.Frame):
    OutputToolbarIconSize = (16, 15)
    current_file_name = r"c:\temp\test1.corrie"

    def __init__(self, *args, **kwargs):

        kwargs["style"] = wx.DEFAULT_FRAME_STYLE

        wx.Frame.__init__(self, *args, **kwargs)

        pub.subscribe(self.listener_update_statusbar, "listenerUpdateStatusBar")

        # Set the title!
        self.set_window_title_with_filename(self.current_file_name)
        self.SetSize(900, 700)

        # set the window exit
        self.Bind(wx.EVT_CLOSE, self.handle_frame_close)

        self.status_bar = self.CreateStatusBar(1)

        self.building_choice = None
        self.front_faces_choice = None
        self.baseline_code_choice = None
        #self.width_field = None
        #self.depth_field = None
        self.powerpoint_filepick = None
        self.excel_filepick = None
        self.weather_filepick = None
        self.occ_areas_text_controls = []
        self.slide_list = None
        self.slide_details_box = None
        self.value_choice = None
        self.select_mode_choice = None
        self.incremental_checkbox = None
        self.general_options_values = None


        self.all_slide_details = self.populate_all_slide_details()
        self.general_options_values = self.populate_general_options()

        self.build_menu()
        self.gui_build()
        self.Refresh()

        self.run_simulation = RunSimulation()

        # self.print_standard_paths()

    def handle_frame_close(self, event):
        self.Destroy()

    def gui_build(self):
        pnl = wx.Panel(self)

        initializer = InitializeData()
        self.building_dict = initializer.populate_buildings()

        building_label = wx.StaticText(pnl, label='Building')
        building_options = list(self.building_dict.keys())
        self.building_choice = wx.Choice(pnl, choices=building_options)
        self.building_choice.SetSelection(3)
        self.Bind(wx.EVT_CHOICE, self.handle_building_choice_select, self.building_choice)

        front_faces_label = wx.StaticText(pnl, label='Front Faces')
        front_faces_option = ['North', 'North East', 'East', 'South East', 'South', 'South West', 'West', 'North West']
        self.front_faces_choice = wx.Choice(pnl, choices=front_faces_option)
        self.front_faces_choice.SetSelection(0)

        baseline_code_label = wx.StaticText(pnl, label='Baseline Code')
        baseline_code_option = ['', ]
        self.baseline_code_choice = wx.Choice(pnl, choices=baseline_code_option)
        self.baseline_code_choice.SetSelection(0)

        building_hbox = wx.BoxSizer(wx.HORIZONTAL)
        building_hbox.Add(building_label, 0, wx.ALL, 10)
        building_hbox.Add(self.building_choice, 1, wx.ALL | wx.EXPAND, 10)
        building_hbox.Add(front_faces_label, 0, wx.ALL, 10)
        building_hbox.Add(self.front_faces_choice, 1, wx.ALL | wx.EXPAND, 10)
        building_hbox.Add(baseline_code_label, 0, wx.ALL, 10)
        building_hbox.Add(self.baseline_code_choice, 1, wx.ALL | wx.EXPAND, 10)

        #lot_boundaries_label = wx.StaticText(pnl, label='Lot Boundaries (feet)')
        #width_label = wx.StaticText(pnl, label='Width')
        #self.width_field = wx.TextCtrl(pnl, value="500")
        #depth_label = wx.StaticText(pnl, label='Depth')
        #self.depth_field = wx.TextCtrl(pnl, value="500")

        #lot_hbox = wx.BoxSizer(wx.HORIZONTAL)
        #lot_hbox.Add(lot_boundaries_label, 0, wx.ALL, 10)
        #lot_hbox.Add(width_label, 0, wx.ALL, 10)
        #lot_hbox.Add(self.width_field, 1, wx.ALL | wx.EXPAND, 10)
        #lot_hbox.Add(depth_label, 0, wx.ALL, 10)
        #lot_hbox.Add(self.depth_field, 1, wx.ALL | wx.EXPAND, 10)

        powerpoint_label = wx.StaticText(pnl, label='PowerPoint File', size=(90, -1))
        self.powerpoint_filepick = wx.FilePickerCtrl(pnl, style=wx.FLP_DEFAULT_STYLE | wx.FLP_SMALL, message='Select the PowerPoint file', wildcard='PowerPoint files (*.pptx)|*.pptx')

        powerpoint_hbox = wx.BoxSizer(wx.HORIZONTAL)
        powerpoint_hbox.Add(powerpoint_label, 0, wx.ALL, 10)
        powerpoint_hbox.Add(self.powerpoint_filepick, 1, wx.ALL | wx.EXPAND, 10)

        excel_label = wx.StaticText(pnl, label='Excel File', size=(90, -1))
        self.excel_filepick = wx.FilePickerCtrl(pnl, style=wx.FLP_DEFAULT_STYLE | wx.FLP_SMALL, message='Select the Excel file', wildcard='Excel files (*.xlsx)|*.xlsx')

        excel_hbox = wx.BoxSizer(wx.HORIZONTAL)
        excel_hbox.Add(excel_label, 0, wx.ALL, 10)
        excel_hbox.Add(self.excel_filepick, 1, wx.ALL | wx.EXPAND, 10)

        weather_label = wx.StaticText(pnl, label='Weather File', size=(90, -1))
        self.weather_filepick = wx.FilePickerCtrl(pnl, style=wx.FLP_DEFAULT_STYLE | wx.FLP_SMALL, message='Select the EnergyPlus Weather file', wildcard='EnergyPlus Weather files (*.epw)|*.epw')

        weather_hbox = wx.BoxSizer(wx.HORIZONTAL)
        weather_hbox.Add(weather_label, 0, wx.ALL, 10)
        weather_hbox.Add(self.weather_filepick, 1, wx.ALL | wx.EXPAND, 10)

        occ_area_label = wx.StaticText(pnl, -1, "Occupancy Areas")
        sqft_label = wx.StaticText(pnl, -1, "(square feet)")

        occ_area_sizer = wx.FlexGridSizer(cols=2, vgap=5, hgap=5)
        occ_area_sizer.AddGrowableCol(0)
        occ_area_sizer.AddGrowableCol(1)
        occ_area_sizer.Add(occ_area_label, 0,  wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.TOP | wx.BOTTOM, 5)
        occ_area_sizer.Add(sqft_label, 0, wx.TOP | wx.BOTTOM, 5)

        max_num_occ_areas = 10
        for count in range(max_num_occ_areas):
            label = wx.StaticText(pnl, -1, 'xxxx', size=(150, -1))
            text_control = wx.TextCtrl(pnl, -1, '0', size=(80, -1))
            self.occ_areas_text_controls.append((label, text_control))
            occ_area_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.TOP | wx.BOTTOM, 5) #  wx.ALIGN_RIGHT |
            occ_area_sizer.Add(text_control, 0, wx.TOP, 5)

        occ_areas = {'Quick Service Restaurant': 30000, 'Full Service Restaurant': 0, 'Retail Standalone': 0, 'junk': 0}
        self.update_occ_areas(occ_areas)

        #call to initialize the screen
        self.handle_building_choice_select(wx.EVT_CHOICE)

        slides_label = wx.StaticText(pnl, label='Slides')

        slide_list_text = list(self.all_slide_details.keys())
        slide_list_order = list(range(len(slide_list_text)))
        self.slide_list = wx.RearrangeCtrl(pnl, 1, size=wx.DefaultSize, items=slide_list_text, order=slide_list_order)
        slide_list_ctrl = self.slide_list.GetList()
        self.Bind(wx.EVT_LISTBOX, self.handle_slide_list_ctrl_click, slide_list_ctrl)
        slide_list_ctrl.SetSelection(0)

        slides_sizer = wx.BoxSizer(wx.VERTICAL)
        slides_sizer.Add(slides_label, 0, wx.ALL, 5)
        slides_sizer.Add(self.slide_list, 1, wx.ALL | wx.EXPAND, 5)

        self.slide_details_box = wx.StaticBox(pnl, -1, "Slide Details for: Aspect Ratio")
        top_border, other_border = self.slide_details_box.GetBordersForSizer()
        slide_details_sizer = wx.BoxSizer(wx.VERTICAL)
        slide_details_sizer.AddSpacer(top_border)

        select_mode_hbox = wx.BoxSizer(wx.HORIZONTAL)
        select_mode_label = wx.StaticText(self.slide_details_box, label='Selection Mode')
        select_mode_options = ['Automatic', 'Exclude Best Option', 'Exclude Two Best Options',
                               'Exclude Three Best Options', 'Select Option 1', 'Select Option 2', 'Select Option 3',
                               'Select Option 4', 'Select Option 5', 'Select Option 6', 'Select Option 7',
                               'Select Option 8']
        self.select_mode_choice = wx.Choice(self.slide_details_box, choices=select_mode_options)
        self.select_mode_choice.SetSelection(0)
        self.Bind(wx.EVT_CHOICE, self.handle_select_mode_choice_select, self.select_mode_choice)
        select_mode_hbox.Add(select_mode_label, 0, wx.ALL, 5)
        select_mode_hbox.Add(self.select_mode_choice, 1, wx.ALL, 5)
        slide_details_sizer.Add(select_mode_hbox, 0, wx.ALL, 5)

        option_simulated_label = wx.StaticText(self.slide_details_box, label="Options Simulated")
        slide_details_sizer.Add(option_simulated_label, 0, wx.ALL, 5)

        value_options = ['none',]
        self.value_choice = wx.CheckListBox(self.slide_details_box, 1, size=wx.DefaultSize, choices=value_options)
        self.Bind(wx.EVT_CHECKLISTBOX, self.handle_value_choice_check, self.value_choice)
        slide_details_sizer.Add(self.value_choice, 1, wx.ALL | wx.EXPAND, 5)

        self.incremental_checkbox = wx.CheckBox(self.slide_details_box, label='Include in Incremental Improvements')
        selection_mode, include_incremental, options_list, osw_list = self.all_slide_details[slide_list_ctrl.GetString((slide_list_ctrl.GetSelection()))]
        self.set_slide_details(selection_mode, include_incremental, options_list)
        self.Bind(wx.EVT_CHECKBOX, self.handle_incremental_checkbox_check, self.incremental_checkbox)

        slide_details_sizer.Add(self.incremental_checkbox, 0, wx.ALL, 5)
        self.slide_details_box.SetSizer(slide_details_sizer)

        self.run_simulations_button = wx.Button(pnl, 1, "Run Simulations", size=(140, 30))
        self.run_simulations_button.Bind(wx.EVT_BUTTON, self.handle_run_simulation_button)
        cancel_simulations_button = wx.Button(pnl, 1, "Cancel Simulations", size=(140, 30))

        run_cancel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        run_cancel_sizer.Add(self.run_simulations_button, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        run_cancel_sizer.Add(cancel_simulations_button, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        bottom_right_sizer = wx.BoxSizer(wx.VERTICAL)
        bottom_right_sizer.Add(self.slide_details_box, 1, wx.ALL | wx.ALIGN_TOP |wx.EXPAND, 5)
        bottom_right_sizer.Add(run_cancel_sizer, 0, wx.ALL | wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT | wx.EXPAND, 5)

        bottom_hbox = wx.BoxSizer(wx.HORIZONTAL)
        bottom_hbox.Add(occ_area_sizer, 1, wx.ALL | wx.EXPAND, 5)
        bottom_hbox.Add(slides_sizer, 2, wx.ALL | wx.EXPAND, 5)
        bottom_hbox.Add(bottom_right_sizer, 2, wx.ALL | wx.EXPAND, 5)

        main_vbox = wx.BoxSizer(wx.VERTICAL)
        main_vbox.Add(building_hbox, 0, wx.EXPAND | wx.LEFT, border=20)
        #main_vbox.Add(lot_hbox, 0, wx.EXPAND | wx.LEFT, border=20)
        main_vbox.Add(powerpoint_hbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)
        main_vbox.Add(excel_hbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)
        main_vbox.Add(weather_hbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)
        main_vbox.Add(bottom_hbox, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)
        main_vbox.Add(self.status_bar,0)

        pnl.SetSizer(main_vbox)
        pnl.Fit()

    def update_occ_areas(self, occ_areas):
        for (label, text_control) in self.occ_areas_text_controls:
            label.SetLabel('')
            text_control.Show(False)
        for index, (name, area) in enumerate(occ_areas.items()):
            label, text_control = self.occ_areas_text_controls[index]
            label.SetLabel(name)
            text_control.Show(True)
            text_control.SetValue(str(area))

    def populate_all_slide_details(self):
        all_slide_details = {}
        #aspect ratio
        aspect_ratio_options = []
        aspect_ratio_options.append(["width 1.0 : depth 3.0", True, '0.33'])
        aspect_ratio_options.append(["width 1.0 : depth 2.5", False, '0.40'])
        aspect_ratio_options.append(["width 1.0 : depth 2.0", True, '0.50'])
        aspect_ratio_options.append(["width 1.0 : depth 1.5", False, '0.67'])
        aspect_ratio_options.append(["width 1.0 : depth 1.0 (square)", True, '1.00'])
        aspect_ratio_options.append(["width 1.5 : depth 1.0", False, '1.5'])
        aspect_ratio_options.append(["width 2.0 : depth 1.0", True, '2.0'])
        aspect_ratio_options.append(["width 2.5 : depth 1.0", False, '2.5'])
        aspect_ratio_options.append(["width 3.0 : depth 1.0", True, '3.0'])
        all_slide_details['Aspect Ratio'] = ['Automatic',True, aspect_ratio_options, [('CreateBarFromBuildingTypeRatios','ns_to_ew_ratio'),]]

        stories_options = []
        stories_options.append(["One Floor", True, '1'])
        stories_options.append(["Two Floors", True, '2'])
        stories_options.append(["Three Floors", True, '3'])
        stories_options.append(["Four Floors", False, '4'])
        all_slide_details['Number of Stories'] = ['Exclude Best Option',False, stories_options, [('CreateBarFromBuildingTypeRatios','num_stories_above_grade'),]]

        orientation_options = []
        orientation_options.append(["Entrance Faces North", True, '0'])
        orientation_options.append(["Entrance Faces North East", False, '45'])
        orientation_options.append(["Entrance Faces East", True, '90'])
        orientation_options.append(["Entrance Faces South East", False, '135'])
        orientation_options.append(["Entrance Faces South", True, '180'])
        orientation_options.append(["Entrance Faces South West", False, '225'])
        orientation_options.append(["Entrance Faces West", True, '270'])
        orientation_options.append(["Entrance Faces North West", False, '315'])
        all_slide_details['Orientation'] = ['Automatic',False, orientation_options, [('CreateBarFromBuildingTypeRatios','building_rotation'),]]

        wall_insulation_options = []
        wall_insulation_options.append(["R15", False, '15'])
        wall_insulation_options.append(["R17", False, '17'])
        wall_insulation_options.append(["R19", True, '19'])
        wall_insulation_options.append(["R23", True, '23'])
        wall_insulation_options.append(["R27", True, '27'])
        wall_insulation_options.append(["R31", False, '31'])
        wall_insulation_options.append(["R35", False, '35'])
        all_slide_details['Wall Insulation'] = ['Automatic', True, wall_insulation_options, [('IncreaseInsulationRValueForExteriorWalls','r_value'),]]

        roof_insulation_options = []
        roof_insulation_options.append(["R25", False, '25'])
        roof_insulation_options.append(["R29", True, '29'])
        roof_insulation_options.append(["R33", True, '33'])
        roof_insulation_options.append(["R37", True, '37'])
        roof_insulation_options.append(["R41", True, '41'])
        roof_insulation_options.append(["R45", True, '45'])
        roof_insulation_options.append(["R50", False, '50'])
        roof_insulation_options.append(["R55", False, '55'])
        roof_insulation_options.append(["R60", False, '60'])
        all_slide_details['Roof Insulation'] = ['Automatic', True, roof_insulation_options, [('IncreaseInsulationRValueForRoofs','r_value'),]]

        wwr_options = []
        wwr_options.append(["2%", False, '0.02'])
        wwr_options.append(["4%", False, '0.04'])
        wwr_options.append(["6%", False, '0.06'])
        wwr_options.append(["8%", False, '0.08'])
        wwr_options.append(["10%", False, '0.10'])
        wwr_options.append(["15%", False, '0.15'])
        wwr_options.append(["20%", False, '0.20'])
        wwr_options.append(["25%", True, '0.25'])
        wwr_options.append(["30%", True, '0.30'])
        wwr_options.append(["35%", True, '0.35'])
        wwr_options.append(["40%", True, '0.40'])
        wwr_options.append(["45%", True, '0.45'])
        wwr_options.append(["50%", True, '0.50'])
        wwr_options.append(["60%", False, '0.60'])
        wwr_options.append(["70%", False, '0.70'])
        wwr_options.append(["80%", False, '0.80'])
        all_slide_details['Window to wall ratio'] = ['Automatic', True, wwr_options, [('CreateBarFromBuildingTypeRatios','wwr'),]]

#        fenestration_options = []
#        # from CSBR-UMN (2013) - See MaxTech final report
#        fenestration_options.append(["U-Factor=0.99 SHGC=0.72 Tvis=0.74", False])
#        fenestration_options.append(["U-Factor=0.55 SHGC=0.61 Tvis=0.64", False])
#        fenestration_options.append(["U-Factor=0.55 SHGC=0.45 Tvis=0.39", False])
#        fenestration_options.append(["U-Factor=0.53 SHGC=0.18 Tvis=0.08", False])
#        fenestration_options.append(["U-Factor=0.39 SHGC=0.27 Tvis=0.43", True])
#        fenestration_options.append(["U-Factor=0.39 SHGC=0.23 Tvis=0.30", False])
#        fenestration_options.append(["U-Factor=0.39 SHGC=0.35 Tvis=0.57", True])
#        fenestration_options.append(["U-Factor=0.38 SHGC=0.26 Tvis=0.52", True])
#        fenestration_options.append(["U-Factor=0.22 SHGC=0.28 Tvis=0.49", True])
#        fenestration_options.append(["U-Factor=0.21 SHGC=0.19 Tvis=0.28", False])
#        fenestration_options.append(["U-Factor=0.97 SHGC=0.44 Tvis=0.50", True])
#        fenestration_options.append(["U-Factor=0.55 SHGC=0.48 Tvis=0.44", True])
#        all_slide_details['Fenestration Options'] = ['Automatic',True, fenestration_options]

# the overhang measure is OS seems to always fail - need to debug
#        overhang_options = []
#        overhang_options.append(["Depth is 0.2 x Window Height", True, '0.2'])
#        overhang_options.append(["Depth is 0.3 x Window Height", False, '0.3'])
#        overhang_options.append(["Depth is 0.4 x Window Height", True, '0.4'])
#        overhang_options.append(["Depth is 0.5 x Window Height", False, '0.5'])
#        overhang_options.append(["Depth is 0.6 x Window Height", True, '0.6'])
#        overhang_options.append(["Depth is 0.7 x Window Height", False, '0.7'])
#        overhang_options.append(["Depth is 0.8 x Window Height", True, '0.8'])
#        # note also have to have arguments "facade" : "All", "function" : "Add"
#        all_slide_details['Window Overhang'] = ['Automatic',True, overhang_options, [('AddRemoveOrReplaceWindowOverhangs','projection_factor'),]]

        lighting_options = []
        lighting_options.append(["0.40 W/sqft", False, '0.40'])
        lighting_options.append(["0.45 W/sqft", False, '0.45'])
        lighting_options.append(["0.50 W/sqft", False, '0.50'])
        lighting_options.append(["0.55 W/sqft", False, '0.55'])
        lighting_options.append(["0.60 W/sqft", True, '0.60'])
        lighting_options.append(["0.65 W/sqft", False, '0.65'])
        lighting_options.append(["0.70 W/sqft", True, '0.70'])
        lighting_options.append(["0.75 W/sqft", False, '0.75'])
        lighting_options.append(["0.80 W/sqft", True, '0.80'])
        lighting_options.append(["0.85 W/sqft", False, '0.85'])
        lighting_options.append(["0.90 W/sqft", False, '0.90'])
        lighting_options.append(["0.95 W/sqft", False, '0.95'])
        lighting_options.append(["1.00 W/sqft", False, '1.00'])
        lighting_options.append(["1.05 W/sqft", False, '1.05'])
        all_slide_details['Lighting Power Density'] = ['Automatic',True, lighting_options, [('SetLightingLoadsByLPD','lpd'),]]
        return all_slide_details

    def handle_slide_list_ctrl_click(self, event):
        self.refresh_slide_list_details()

    def refresh_slide_list_details(self):
        slide_list_ctrl = self.slide_list.GetList()
        slide_selected = slide_list_ctrl.GetString(slide_list_ctrl.GetSelection())
        self.slide_details_box.SetLabel("Slide Details for: " + slide_selected)
        selection_mode, include_incremental, options_list, osw_list = self.all_slide_details[slide_selected]
        self.set_slide_details(selection_mode, include_incremental, options_list)

    def set_slide_details(self, selection_mode, include_incremental, options_list):
        # set options
        items_from_list = [x[0] for x in options_list]
        selected_options = []
        # print('options_list ',options_list)
        for option, flag, argument_value in options_list:
            if flag:
                selected_options.append(option)
        self.value_choice.SetItems(items_from_list)
        self.value_choice.SetCheckedStrings(selected_options)
        # set selection mode
        select_mode_selected_index = self.select_mode_choice.FindString(selection_mode)
        self.select_mode_choice.SetSelection(select_mode_selected_index)
        # set incremental choice
        self.incremental_checkbox.SetValue(include_incremental)

    def handle_incremental_checkbox_check(self, event):
        slide_list_ctrl = self.slide_list.GetList()
        slide_selected = slide_list_ctrl.GetString(slide_list_ctrl.GetSelection())
        selection_mode, include_incremental, options_list, osw_list = self.all_slide_details[slide_selected]
        self.all_slide_details[slide_selected] = [selection_mode, self.incremental_checkbox.GetValue(), options_list, osw_list]

    def handle_select_mode_choice_select(self, event):
        slide_list_ctrl = self.slide_list.GetList()
        slide_selected = slide_list_ctrl.GetString(slide_list_ctrl.GetSelection())
        selection_mode, include_incremental, options_list, osw_list = self.all_slide_details[slide_selected]
        self.all_slide_details[slide_selected] = [self.select_mode_choice.GetString(self.select_mode_choice.GetSelection()), include_incremental, options_list, osw_list]

    def handle_value_choice_check(self, event):
        #print(self.value_choice.IsChecked(event.GetInt()))
        value_options = []
        for index in range(self.value_choice.GetCount()):
            #print(self.value_choice.GetString(index),self.value_choice.IsChecked(index))
            value_options.append([self.value_choice.GetString(index),self.value_choice.IsChecked(index)])
        slide_list_ctrl = self.slide_list.GetList()
        slide_selected = slide_list_ctrl.GetString(slide_list_ctrl.GetSelection())
        selection_mode, include_incremental, old_options_list, osw_list = self.all_slide_details[slide_selected]
        # print('old_options_list', old_options_list)
        # print('value_options', value_options)
        option_argument_dictionary = {k:v for (k, _, v) in old_options_list}
        # print('option_argument_dictionary', option_argument_dictionary)
        new_options_list = [[choice, check_status, option_argument_dictionary[choice]] for choice, check_status in value_options ]
        # print('new_options_list', new_options_list)
        self.all_slide_details[slide_selected] = [selection_mode, include_incremental, new_options_list, osw_list]

    def build_menu(self):
        menu_bar = wx.MenuBar()

        file_menu = wx.Menu()
        menu_file_new = file_menu.Append(101, "&New", "Create a new Corrie file")
        menu_file_open = file_menu.Append(102, "&Open...", "Open an existing Corrie file")
        self.Bind(wx.EVT_MENU, self.handle_file_open, menu_file_open)
        file_menu.AppendSeparator()
        menu_file_save = file_menu.Append(103, "&Save\tCtrl-S", "Save file to a same file name")
        self.Bind(wx.EVT_MENU, self.handle_file_save, menu_file_save)
        menu_file_save_as = file_menu.Append(104, "Save &As...", "Save file to a new file name")
        self.Bind(wx.EVT_MENU, self.handle_file_save_as, menu_file_save_as)
        file_menu.AppendSeparator()
        menu_file_close = file_menu.Append(105, "&Close", "Close the file")
        file_menu.AppendSeparator()
        menu_file_exit = file_menu.Append(106, "E&xit", "Exit the application")
        self.Bind(wx.EVT_MENU, self.handle_quit, menu_file_exit)
        menu_bar.Append(file_menu, "&File")

        option_menu = wx.Menu()
        menu_option_general = option_menu.Append(201, "&General Options...", "General settings for this file.")
        self.Bind(wx.EVT_MENU, self.handle_menu_option_general, menu_option_general)
        menu_option_regen_output = option_menu.Append(202, "Regen Output")
        self.Bind(wx.EVT_MENU, self.handle_menu_option_regen_output, menu_option_regen_output)
        menu_bar.Append(option_menu, "&Option")

        help_menu = wx.Menu()
        menu_help_topic = help_menu.Append(301, "&Topic...", "Get help.")
        menu_help_about = help_menu.Append(302, "&About...", "About Corrie.")
        menu_bar.Append(help_menu, "&Help")

        self.SetMenuBar(menu_bar)

    def handle_quit(self, e):
        self.Close()

    def handle_menu_option_general(self, event):
        dialog_general_options = general_options.GeneralOptionsDialog(None)
        dialog_general_options.set_parameters(self.general_options_values)
        return_value = dialog_general_options.ShowModal()
        if return_value == dialog_general_options.CLOSE_SIGNAL_CANCEL:
            return
        else: #ok pressed
            self.general_options_values = dialog_general_options.general_options_dict
        dialog_general_options.Destroy()

    def populate_general_options(self):
        columns_of_values_dict = {'Source Energy Use Intensity':True,
                                  'Site Energy Use Intensity':True,
                                  'Total Source Energy':True,
                                  'Total Site Energy':True,
                                  'Total CO2':True,
                                  'Cooling Energy':True,
                                  'Heating Energy':True,
                                  'Lighting Energy':False,
                                  'Plug Energy':False,
                                  'Total Electricity Usage':True,
                                  'Total Natural Gas Usage':True}

        options_selected = {'Output Metric':'Annual CO2',
                            'Units':'Inch-Pound',
                            'Chart Type':'Vertical Column',
                            'Chart Sort Options':'Ascending',
                            'Show Cumulative Chart Slide':False,
                            'Show End Use Pie Chart Slide':True,
                            'Show End Use Monthly Chart Slide':False,
                            'Number of Rows Per Slide': '15',
                            'Tab Name':'CorrieResults',
                            'Columns of Values':columns_of_values_dict}
        return options_selected

    def construct_save_data(self):
        save_data = {}
        save_data['building'] = self.building_choice.GetString(self.building_choice.GetSelection())
        save_data['frontFaces'] = self.front_faces_choice.GetString(self.front_faces_choice.GetSelection())
        save_data['baselineCode'] = self.baseline_code_choice.GetString(self.baseline_code_choice.GetSelection())
        #save_data['width'] = self.width_field.GetValue()
        #save_data['depth'] = self.depth_field.GetValue()
        save_data['powerpointPath'] = self.powerpoint_filepick.GetPath()
        save_data['excelPath'] = self.excel_filepick.GetPath()
        save_data['weatherPath'] = self.weather_filepick.GetPath()
        occ_area_save_data = {}
        for (label, text_control) in self.occ_areas_text_controls:
            if label.GetLabel():
                occ_area_save_data[label.GetLabel()] = text_control.GetValue()
        save_data['occupancyAreas'] = occ_area_save_data
        save_data['slideDetails'] = self.all_slide_details
        slide_list_ctrl = self.slide_list.GetList()
        slide_names_in_order = []
        for index in range(slide_list_ctrl.GetCount()):
            slide_names_in_order.append([slide_list_ctrl.GetString(index),slide_list_ctrl.IsChecked(index)])
        save_data['slideOrder'] = slide_names_in_order
        save_data['generalOptions'] = self.general_options_values
        #print(json.dumps(save_data, indent=4))
        return save_data

    def handle_file_save(self, event):
        #print("handle_file_save entered")
        save_data = self.construct_save_data()
        with open(self.current_file_name, 'w') as corrie_file:
            json.dump(save_data, corrie_file, indent=4)

    def handle_file_save_as(self, event):
        with wx.FileDialog(self, "Save Corrie File", wildcard="Corrie files (*.corrie)|*.corrie",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind
            self.current_file_name = fileDialog.GetPath()
            self.set_window_title_with_filename(self.current_file_name)
            save_data = self.construct_save_data()
            with open(self.current_file_name, 'w') as corrie_file:
                json.dump(save_data, corrie_file, indent=4)

    def set_window_title_with_filename(self, filename):
        self.SetTitle("Corrie" + '   -   ' + filename)

    def handle_file_open(self, event):
        #if self.contentNotSaved:
        #    if wx.MessageBox("Current content has not been saved! Proceed?", "Please confirm",
        #                     wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
        #        return
        #
        with wx.FileDialog(self, "Open Corrie File", wildcard="Corrie files (*.corrie)|*.corrie",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind
            path_name = fileDialog.GetPath()
            with open(path_name, 'r') as corrie_file:
                load_data = json.load(corrie_file)
                self.read_load_data(load_data)
                self.current_file_name = path_name
                self.set_window_title_with_filename(self.current_file_name)

    def read_load_data(self, load_data):
        print(json.dumps(load_data, indent=4))
        self.building_choice.SetSelection(self.building_choice.FindString(load_data['building']))
        self.front_faces_choice.SetSelection(self.front_faces_choice.FindString(load_data['frontFaces']))
        self.baseline_code_choice.SetSelection(self.baseline_code_choice.FindString(load_data['baselineCode']))
        #self.width_field.SetValue(load_data['width'])
        #self.depth_field.SetValue(load_data['depth'])
        self.powerpoint_filepick.SetPath(load_data['powerpointPath'])
        self.excel_filepick.SetPath(load_data['excelPath'])
        self.weather_filepick.SetPath(load_data['weatherPath'])
        occupancy_area_data = load_data['occupancyAreas']
        self.update_occ_areas(occupancy_area_data)
        self.all_slide_details = load_data['slideDetails']
        slide_list_ctrl = self.slide_list.GetList()
        slide_list_ctrl.Clear()
        slide_names_in_order = load_data['slideOrder']
        for index, (slide_name, slide_checked) in enumerate(slide_names_in_order):
            slide_list_ctrl.Append(slide_name)
            slide_list_ctrl.Check(index, slide_checked)
        slide_list_ctrl.SetSelection(0)
        self.refresh_slide_list_details()
        self.general_options_values = load_data['generalOptions']

    def handle_run_simulation_button(self, event):
        print('handle_run_simulation_button')
        self.status_bar.SetStatusText('handle_run_simulation_button')
        current_save_data = self.construct_save_data()
        self.run_simulation.saved_data = current_save_data
        self.run_simulation.set_current_file_name(self.current_file_name)
        self.run_simulation.run_simulations()
        print('All simulation complete.')
        self.status_bar.SetStatusText('All simulation complete.')
        results = self.run_simulation.collect_results()
        self.run_simulation.populate_powerpoint()

    def print_standard_paths(self):
        sp = wx.StandardPaths.Get()
        print("AppDocumentsDir", sp.AppDocumentsDir)
        print("ConfigDir", sp.ConfigDir)
        print("DataDir", sp.DataDir)
        print("DocumentsDir", sp.DocumentsDir)
        print("ExecutablePath", sp.ExecutablePath)
        print("InstallPrefix", sp.InstallPrefix)
        print("LocalDataDir", sp.LocalDataDir)
        print("PluginsDir", sp.PluginsDir)
        print("ResourcesDir", sp.ResourcesDir)
        print("TempDir", sp.TempDir)
        print("UserConfigDir", sp.UserConfigDir)
        print("UserDataDir", sp.UserDataDir)
        print("UserLocalDataDir", sp.UserLocalDataDir)
        print("current working directory", os.getcwd())
        print("__file__", os.path.realpath(__file__))

    def handle_building_choice_select(self, event):
        building_selected = self.building_choice.GetString(self.building_choice.GetSelection())
        # print(self.building_dict[building_selected].building_type)
        self.baseline_code_choice.Clear()
        codes_with_ashrae = ['ASHRAE ' + code for code in self.building_dict[building_selected].codes_available]
        self.baseline_code_choice.AppendItems(codes_with_ashrae)
        self.baseline_code_choice.SetSelection(0)
        _, text_control = self.occ_areas_text_controls[0] #get the current text control so can use existing value of the area
        occupany_areas = {}
        occupany_areas[self.building_dict[building_selected].display_string] = text_control.GetValue()
        for other_building in self.building_dict[building_selected].other_buildings_available:
            occupany_areas[other_building] = 0
        self.update_occ_areas(occupany_areas)

    def listener_update_statusbar(self, message):
        self.status_bar.SetStatusText(message)

    def handle_menu_option_regen_output(self, event):
        print('handle_menu_option_regen_output')
        self.status_bar.SetStatusText('handle_menu_option_regen_output')
        current_save_data = self.construct_save_data()
        self.run_simulation.saved_data = current_save_data
        self.run_simulation.set_current_file_name(self.current_file_name)
        results = self.run_simulation.collect_results()
        print('results: ', results)
        self.run_simulation.populate_powerpoint()


