import wx
import json

from corrie.interface import general_options

# wx callbacks need an event argument even though we usually don't use it, so the next line disables that check
# noinspection PyUnusedLocal
class CorrieFrame(wx.Frame):
    OutputToolbarIconSize = (16, 15)
    current_file_name = r"c:\temp\test1.corrie"

    def __init__(self, *args, **kwargs):

        kwargs["style"] = wx.DEFAULT_FRAME_STYLE

        wx.Frame.__init__(self, *args, **kwargs)

        # Set the title!
        self.SetTitle("Corrie" + '   -   ' + self.current_file_name)
        self.SetSize(900, 700)

        # set the window exit
        self.Bind(wx.EVT_CLOSE, self.handle_frame_close)

        self.StatusBar = self.CreateStatusBar(1)

        self.building_choice = None
        self.front_faces_choice = None
        self.baseline_code_choice = None
        self.width_field = None
        self.depth_field = None
        self.powerpoint_filepick = None
        self.excel_filepick = None
        self.weather_filepick = None
        self.occ_areas_text_controls = None
        self.slide_list = None
        self.slide_details_box = None
        self.value_choice = None
        self.select_mode_choice = None
        self.incremental_checkbox = None


        self.all_slide_details = self.populate_all_slide_details()

        self.build_menu()
        self.gui_build()
        self.Refresh()

    def handle_frame_close(self, event):
        self.Destroy()

    def gui_build(self):
        pnl = wx.Panel(self)

        building_label = wx.StaticText(pnl, label='Building')
        building_options = ['Office - Rectangle', 'Retail - Rectangle', 'School - U Shaped', 'School - E Shaped']
        self.building_choice = wx.Choice(pnl, choices=building_options)
        self.building_choice.SetSelection(0)

        front_faces_label = wx.StaticText(pnl, label='Front Faces')
        front_faces_option = ['North', 'North East', 'East', 'South East', 'South', 'South West', 'West', 'North West']
        self.front_faces_choice = wx.Choice(pnl, choices=front_faces_option)
        self.front_faces_choice.SetSelection(0)

        baseline_code_label = wx.StaticText(pnl, label='Baseline Code')
        baseline_code_option = ['ASHRAE 90.1-2004', 'ASHRAE 90.1-2007', 'ASHRAE 90.1-2010', 'ASHRAE 90.1-2013',
                                'ASHRAE 90.1-2016']
        self.baseline_code_choice = wx.Choice(pnl, choices=baseline_code_option)
        self.baseline_code_choice.SetSelection(0)

        building_hbox = wx.BoxSizer(wx.HORIZONTAL)
        building_hbox.Add(building_label, 0, wx.ALL, 10)
        building_hbox.Add(self.building_choice, 1, wx.ALL | wx.EXPAND, 10)
        building_hbox.Add(front_faces_label, 0, wx.ALL, 10)
        building_hbox.Add(self.front_faces_choice, 1, wx.ALL | wx.EXPAND, 10)
        building_hbox.Add(baseline_code_label, 0, wx.ALL, 10)
        building_hbox.Add(self.baseline_code_choice, 1, wx.ALL | wx.EXPAND, 10)

        lot_boundaries_label = wx.StaticText(pnl, label='Lot Boundaries (feet)')
        width_label = wx.StaticText(pnl, label='Width')
        self.width_field = wx.TextCtrl(pnl, value="500")
        depth_label = wx.StaticText(pnl, label='Depth')
        self.depth_field = wx.TextCtrl(pnl, value="500")

        lot_hbox = wx.BoxSizer(wx.HORIZONTAL)
        lot_hbox.Add(lot_boundaries_label, 0, wx.ALL, 10)
        lot_hbox.Add(width_label, 0, wx.ALL, 10)
        lot_hbox.Add(self.width_field, 1, wx.ALL | wx.EXPAND, 10)
        lot_hbox.Add(depth_label, 0, wx.ALL, 10)
        lot_hbox.Add(self.depth_field, 1, wx.ALL | wx.EXPAND, 10)

        powerpoint_label = wx.StaticText(pnl, label='PowerPoint File', size=(90, -1))
        self.powerpoint_filepick = wx.FilePickerCtrl(pnl, style=wx.FLP_USE_TEXTCTRL)

        powerpoint_hbox = wx.BoxSizer(wx.HORIZONTAL)
        powerpoint_hbox.Add(powerpoint_label, 0, wx.ALL, 10)
        powerpoint_hbox.Add(self.powerpoint_filepick, 1, wx.ALL | wx.EXPAND, 10)

        excel_label = wx.StaticText(pnl, label='Excel File', size=(90, -1))
        self.excel_filepick = wx.FilePickerCtrl(pnl, style=wx.FLP_USE_TEXTCTRL)

        excel_hbox = wx.BoxSizer(wx.HORIZONTAL)
        excel_hbox.Add(excel_label, 0, wx.ALL, 10)
        excel_hbox.Add(self.excel_filepick, 1, wx.ALL | wx.EXPAND, 10)

        weather_label = wx.StaticText(pnl, label='Weather File', size=(90, -1))
        self.weather_filepick = wx.FilePickerCtrl(pnl, style=wx.FLP_USE_TEXTCTRL)

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

        occ_areas = {'Office': 1000, 'Retail': 2000, 'Storage': 1200, 'Dining': 0,
                     'other1': 0, 'other2': 0, 'other3': 0, 'other4': 0}

        self.occ_areas_text_controls = {}
        for name, area in occ_areas.items():
            label = wx.StaticText(pnl, -1, name)
            self.occ_areas_text_controls[name] = wx.TextCtrl(pnl, -1, str(area), size=(50, -1))
            occ_area_sizer.Add(label, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.TOP | wx.BOTTOM, 5)
            occ_area_sizer.Add(self.occ_areas_text_controls[name], 0, wx.TOP, 5)

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
        select_mode_hbox.Add(select_mode_label, 0, wx.ALL, 5)
        select_mode_hbox.Add(self.select_mode_choice, 1, wx.ALL, 5)
        slide_details_sizer.Add(select_mode_hbox, 0, wx.ALL, 5)

        option_simulated_label = wx.StaticText(self.slide_details_box, label="Options Simulated")
        slide_details_sizer.Add(option_simulated_label, 0, wx.ALL, 5)

        value_options = ['0.6','0.8','1.0','1.2','1.4','1.6','1.8','2.0']
        self.value_choice = wx.CheckListBox(self.slide_details_box, 1, size=wx.DefaultSize, choices=value_options)
        self.value_choice.SetSelection(0)
        slide_details_sizer.Add(self.value_choice, 1, wx.ALL | wx.EXPAND, 5)

        self.incremental_checkbox = wx.CheckBox(self.slide_details_box, label='Include in Incremental Improvements')
        self.incremental_checkbox.SetValue(True)
        slide_details_sizer.Add(self.incremental_checkbox, 0, wx.ALL, 5)
        self.slide_details_box.SetSizer(slide_details_sizer)

        run_simulations_button = wx.Button(pnl, 1, "Run Simulations", size=(140, 30))
        cancel_simulations_button = wx.Button(pnl, 1, "Cancel Simulations", size=(140, 30))

        run_cancel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        run_cancel_sizer.Add(run_simulations_button, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
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
        main_vbox.Add(lot_hbox, 0, wx.EXPAND | wx.LEFT, border=20)
        main_vbox.Add(powerpoint_hbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)
        main_vbox.Add(excel_hbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)
        main_vbox.Add(weather_hbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)
        main_vbox.Add(bottom_hbox, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)

        pnl.SetSizer(main_vbox)
        pnl.Fit()

    def populate_all_slide_details(self):
        all_slide_details = {}
        #aspect ratio
        aspect_ratio_options = []
        aspect_ratio_options.append(["width 1.0 : depth 3.0", True])
        aspect_ratio_options.append(["width 1.0 : depth 2.5", False])
        aspect_ratio_options.append(["width 1.0 : depth 2.0", True])
        aspect_ratio_options.append(["width 1.0 : depth 1.5", False])
        aspect_ratio_options.append(["width 1.0 : depth 1.0", True])
        aspect_ratio_options.append(["width 1.5 : depth 1.0", False])
        aspect_ratio_options.append(["width 2.0 : depth 1.0", True])
        aspect_ratio_options.append(["width 2.5 : depth 1.0", False])
        aspect_ratio_options.append(["width 3.0 : depth 1.0", True])
        all_slide_details['Aspect Ratio'] = ['Automatic',True, aspect_ratio_options]

        stories_options = []
        stories_options.append(["One Floor", True])
        stories_options.append(["One Floor with Basement", True])
        stories_options.append(["Two Floors", True])
        stories_options.append(["Two Floors with Basement", True])
        stories_options.append(["Three Floors", True])
        stories_options.append(["Three Floors with Basement", True])
        stories_options.append(["Four Floors", True])
        stories_options.append(["Four Floors with Basement", True])
        all_slide_details['Number of Stories'] = ['Exclude Best Option',False, stories_options]

        orientation_options = []
        orientation_options.append(["Entrance Faces North", True])
        orientation_options.append(["Entrance Faces North East", True])
        orientation_options.append(["Entrance Faces East", True])
        orientation_options.append(["Entrance Faces South East", True])
        orientation_options.append(["Entrance Faces South", True])
        orientation_options.append(["Entrance Faces South West", True])
        orientation_options.append(["Entrance Faces West", True])
        orientation_options.append(["Entrance Faces North West", True])
        all_slide_details['Orientation'] = ['Automatic',False, orientation_options]

        wall_insulation_options = []
        wall_insulation_options.append(["Additional R2", True])
        wall_insulation_options.append(["Additional R4", True])
        wall_insulation_options.append(["Additional R6", True])
        wall_insulation_options.append(["Additional R8", True])
        wall_insulation_options.append(["Additional R10", True])
        wall_insulation_options.append(["Additional R12", True])
        wall_insulation_options.append(["Reduced by R2", False])
        wall_insulation_options.append(["Reduced by R4", False])
        all_slide_details['Wall Insulation'] = ['Automatic',True, wall_insulation_options]

        roof_insulation_options = []
        roof_insulation_options.append(["Additional R2", True])
        roof_insulation_options.append(["Additional R4", True])
        roof_insulation_options.append(["Additional R6", True])
        roof_insulation_options.append(["Additional R8", True])
        roof_insulation_options.append(["Additional R10", True])
        roof_insulation_options.append(["Additional R12", True])
        roof_insulation_options.append(["Additional R14", True])
        roof_insulation_options.append(["Additional R16", True])
        roof_insulation_options.append(["Additional R18", True])
        roof_insulation_options.append(["Additional R20", True])
        roof_insulation_options.append(["Reduced by R2", False])
        roof_insulation_options.append(["Reduced by R4", False])
        roof_insulation_options.append(["Reduced by R6", False])
        all_slide_details['Roof Insulation'] = ['Automatic',True, roof_insulation_options]

        wwr_options = []
        wwr_options.append(["Increase 10%", False])
        wwr_options.append(["Increase 8%", False])
        wwr_options.append(["Increase 6%", False])
        wwr_options.append(["Increase 4%", False])
        wwr_options.append(["Increase 2%", False])
        wwr_options.append(["Decrease 2%", True])
        wwr_options.append(["Decrease 4%", True])
        wwr_options.append(["Decrease 6%", True])
        wwr_options.append(["Decrease 8%", True])
        wwr_options.append(["Decrease 10%", True])
        wwr_options.append(["Decrease 12%", True])
        wwr_options.append(["Decrease 14%", True])
        wwr_options.append(["Decrease 16%", True])
        wwr_options.append(["Decrease 18%", True])
        wwr_options.append(["Decrease 20%", True])
        all_slide_details['Window to wall ratio'] = ['Automatic',True, wwr_options]

        fenestration_options = []
        # from CSBR-UMN (2013) - See MaxTech final report
        fenestration_options.append(["U-Factor=0.99 SHGC=0.72 Tvis=0.74", True])
        fenestration_options.append(["U-Factor=0.55 SHGC=0.61 Tvis=0.64", True])
        fenestration_options.append(["U-Factor=0.55 SHGC=0.45 Tvis=0.39", True])
        fenestration_options.append(["U-Factor=0.53 SHGC=0.18 Tvis=0.08", True])
        fenestration_options.append(["U-Factor=0.39 SHGC=0.27 Tvis=0.43", True])
        fenestration_options.append(["U-Factor=0.39 SHGC=0.23 Tvis=0.30", True])
        fenestration_options.append(["U-Factor=0.39 SHGC=0.35 Tvis=0.57", True])
        fenestration_options.append(["U-Factor=0.38 SHGC=0.26 Tvis=0.52", True])
        fenestration_options.append(["U-Factor=0.22 SHGC=0.28 Tvis=0.49", True])
        fenestration_options.append(["U-Factor=0.21 SHGC=0.19 Tvis=0.28", True])
        fenestration_options.append(["U-Factor=0.97 SHGC=0.44 Tvis=0.50", True])
        fenestration_options.append(["U-Factor=0.55 SHGC=0.48 Tvis=0.44", True])
        all_slide_details['Fenestration Options'] = ['Automatic',True, fenestration_options]

        overhang_options = []
        overhang_options.append(["Depth is 0.2 x Window Height", True])
        overhang_options.append(["Depth is 0.3 x Window Height", True])
        overhang_options.append(["Depth is 0.4 x Window Height", True])
        overhang_options.append(["Depth is 0.5 x Window Height", True])
        overhang_options.append(["Depth is 0.6 x Window Height", True])
        overhang_options.append(["Depth is 0.7 x Window Height", True])
        overhang_options.append(["Depth is 0.8 x Window Height", True])
        all_slide_details['Window Overhang'] = ['Automatic',True, overhang_options]

        lighting_options = []
        lighting_options.append(["Reduce 0.05 W/sqft", True])
        lighting_options.append(["Reduce 0.10 W/sqft", True])
        lighting_options.append(["Reduce 0.15 W/sqft", True])
        lighting_options.append(["Reduce 0.20 W/sqft", True])
        lighting_options.append(["Reduce 0.25 W/sqft", True])
        lighting_options.append(["Reduce 0.30 W/sqft", True])
        lighting_options.append(["Reduce 0.35 W/sqft", True])
        lighting_options.append(["Reduce 0.40 W/sqft", True])
        lighting_options.append(["Reduce 0.45 W/sqft", True])
        lighting_options.append(["Reduce 0.50 W/sqft", True])
        lighting_options.append(["Reduce 0.55 W/sqft", True])
        all_slide_details['Lighting Power Density'] = ['Automatic',True, lighting_options]
        return all_slide_details

    def handle_slide_list_ctrl_click(self, event):
        slide_list_ctrl = self.slide_list.GetList()
        #print("clicked on slide: " + slide_list_ctrl.GetString(slide_list_ctrl.GetSelection()))
        slide_selected = slide_list_ctrl.GetString(slide_list_ctrl.GetSelection())
        self.slide_details_box.SetLabel("Slide Details for: " + slide_selected)
        #print(self.all_slide_details[slide_selected])
        selection_mode, include_incremental, options_list = self.all_slide_details[slide_selected]
        self.set_slide_details(selection_mode, include_incremental, options_list)
        print(selection_mode)
        print(include_incremental)
        print(options_list)

    def set_slide_details(self, selection_mode, include_incremental, options_list):
        # set options
        items_from_list = [x[0] for x in options_list]
        selected_options = []
        for option, flag in options_list:
            if flag:
                selected_options.append(option)
        self.value_choice.SetItems(items_from_list)
        self.value_choice.SetCheckedStrings(selected_options)
        # set selection mode
        select_mode_selected_index = self.select_mode_choice.FindString(selection_mode)
        self.select_mode_choice.SetSelection(select_mode_selected_index)
        # set incremental choice
        self.incremental_checkbox.SetValue(include_incremental)

    def build_menu(self):
        menu_bar = wx.MenuBar()

        file_menu = wx.Menu()
        menu_file_new = file_menu.Append(101, "&New...", "Create a new Corrie file")
        menu_file_open = file_menu.Append(102, "&Open", "Open an existing Corrie file")
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
        return_value = dialog_general_options.ShowModal()
        dialog_general_options.Destroy()

    def handle_file_open(self, event):
        pass

    def handle_file_save(self, event):
        print("handle_file_save entered")
        save_data = {}
        save_data['building'] = self.building_choice.GetString(self.building_choice.GetSelection())
        save_data['frontFaces'] = self.front_faces_choice.GetString(self.front_faces_choice.GetSelection())
        save_data['baselineCode'] = self.baseline_code_choice.GetString(self.baseline_code_choice.GetSelection())
        save_data['width'] = self.width_field.GetValue()
        save_data['depth'] = self.depth_field.GetValue()
        save_data['powerpointPath'] = self.powerpoint_filepick.GetPath()
        save_data['excelPath'] = self.excel_filepick.GetPath()
        save_data['weatherPath'] = self.weather_filepick.GetPath()
        occ_area_save_data = {}
        for name, text_control in self.occ_areas_text_controls.items():
            occ_area_save_data[name] = text_control.GetValue()
        save_data['occupancyAreas'] = occ_area_save_data
        slide_list_save_data = {}
        slide_list_ctrl = self.slide_list.GetList()
        for index in range(slide_list_ctrl.GetCount()):
            slide_list_save_data[index] = [slide_list_ctrl.GetString(index), slide_list_ctrl.IsChecked(index)]
        save_data['slideList'] = slide_list_save_data

        print(save_data)
        print(json.dumps(save_data, indent=4))
        print(slide_list_ctrl.GetCurrentOrder())

    def handle_file_save_as(self, event):
        pass

