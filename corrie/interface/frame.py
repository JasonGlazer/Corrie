import wx
import json

from corrie.interface import general_options
from corrie.interface import slide_options

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
        self.SetSize(800, 660)

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

        occ_area_box = wx.StaticBox(pnl, -1, "Occupancy Areas (square feet)")

        top_border, other_border = occ_area_box.GetBordersForSizer()
        occ_area_sizer = wx.FlexGridSizer(cols=2, vgap=5, hgap=5)
        occ_area_sizer.AddGrowableCol(0)
        occ_area_sizer.AddGrowableCol(1)
        occ_area_sizer.AddSpacer(top_border)
        occ_area_sizer.AddSpacer(top_border)

        occ_areas = {'Office': 1000, 'Retail': 2000, 'Storage': 1200, 'Dining': 0,
                     'other1': 0, 'other2': 0, 'other3': 0, 'other4': 0}

        self.occ_areas_text_controls = {}
        for name, area in occ_areas.items():
            label = wx.StaticText(occ_area_box, -1, name)
            self.occ_areas_text_controls[name] = wx.TextCtrl(occ_area_box, -1, str(area), size=(50, -1))
            occ_area_sizer.Add(label, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.TOP | wx.BOTTOM, 5)
            occ_area_sizer.Add(self.occ_areas_text_controls[name], 0, wx.TOP, 5)

        occ_area_sizer.AddSpacer(top_border)
        occ_area_sizer.AddSpacer(top_border)
        occ_area_box.SetSizer(occ_area_sizer)

        slides_box = wx.StaticBox(pnl, -1, "Slides")
        top_border, other_border = occ_area_box.GetBordersForSizer()
        slides_sizer = wx.BoxSizer(wx.VERTICAL)

        slide_list_text = ['Aspect Ratio', 'Number of Stories', 'Orientation', 'Wall Insulation', 'Roof Insulation',
                           'Window to wall ratio', 'Fenestration Options', 'Window Overhang', 'Lighting Power Density']
        slide_list_order = [0,1,2,3,4,5,6,7,8]
        slides_sizer.AddSpacer(top_border)
        #self.slide_list = wx.CheckListBox(slides_box, 1, (80, 50), wx.DefaultSize, slide_list_text)
        self.slide_list = wx.RearrangeCtrl(slides_box, 1, (80, 50), wx.DefaultSize, items=slide_list_text, order=slide_list_order)
        slides_sizer.Add(self.slide_list, 1, wx.ALL | wx.EXPAND, 10)
        slides_sizer.AddStretchSpacer(1)

        up_down_option_sizer = wx.BoxSizer(wx.HORIZONTAL)
        #slide_up_button = wx.Button(slides_box, 1, "Up", (20, 20))
        #slide_down_button = wx.Button(slides_box, 1, "Down", (20, 20))
        slide_option_button = wx.Button(slides_box, 1, "Option..", (20, 20))

        #up_down_option_sizer.Add(slide_up_button, 0, wx.ALL, 5)
        #up_down_option_sizer.Add(slide_down_button, 0, wx.ALL, 5)
        up_down_option_sizer.Add(slide_option_button, 0, wx.ALL, 5)

        slides_sizer.Add(up_down_option_sizer, 0, wx.ALL | wx.ALIGN_BOTTOM , 10)
        slides_box.SetSizer(slides_sizer)

        run_cancel_sizer = wx.BoxSizer(wx.VERTICAL)
        run_simulations_button = wx.Button(pnl, 1, "Run Simulations", size=(140, 30))
        cancel_simulations_button = wx.Button(pnl, 1, "Cancel Simulations", size=(140, 30))
        run_cancel_sizer.Add(run_simulations_button, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        run_cancel_sizer.Add(cancel_simulations_button, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        bottom_hbox = wx.BoxSizer(wx.HORIZONTAL)
        bottom_hbox.Add(occ_area_box, 1, wx.ALL|wx.EXPAND, 5)
        bottom_hbox.Add(slides_box, 2, wx.ALL|wx.EXPAND, 5)
        bottom_hbox.Add(run_cancel_sizer, 1, wx.ALL | wx.ALIGN_BOTTOM, 5)

        main_vbox = wx.BoxSizer(wx.VERTICAL)
        main_vbox.Add(building_hbox, 0, wx.EXPAND | wx.LEFT, border=20)
        main_vbox.Add(lot_hbox, 0, wx.EXPAND | wx.LEFT, border=20)
        main_vbox.Add(powerpoint_hbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)
        main_vbox.Add(excel_hbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)
        main_vbox.Add(weather_hbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)
        main_vbox.Add(bottom_hbox, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)

        pnl.SetSizer(main_vbox)

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
        self.Bind(wx.EVT_MENU, self.on_quit, menu_file_exit)
        menu_bar.Append(file_menu, "&File")

        option_menu = wx.Menu()
        menu_option_general = option_menu.Append(201, "&General Options...", "General settings for this file.")
        self.Bind(wx.EVT_MENU, self.handle_menu_option_general, menu_option_general)
        menu_option_slide = option_menu.Append(202, "&Slide Options...", "Settings for the selected slide.")
        self.Bind(wx.EVT_MENU, self.handle_slide_option_general, menu_option_slide)
        menu_bar.Append(option_menu, "&Option")

        help_menu = wx.Menu()
        menu_help_topic = help_menu.Append(301, "&Topic...", "Get help.")
        menu_help_about = help_menu.Append(302, "&About...", "About Corrie.")
        menu_bar.Append(help_menu, "&Help")

        self.SetMenuBar(menu_bar)

    def on_quit(self, e):
        print("on_quit")
        self.Close()

    def handle_menu_option_general(self, event):
        dialog_general_options = general_options.GeneralOptionsDialog(None)
        return_value = dialog_general_options.ShowModal()
        dialog_general_options.Destroy()

    def handle_slide_option_general(self, event):
        dialog_slide_options = slide_options.SlideOptionsDialog(None)
        return_value = dialog_slide_options.ShowModal()
        dialog_slide_options.Destroy()

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
        for index in range(self.slide_list.GetCount()):
            slide_list_save_data[index] = [self.slide_list.GetString(index), self.slide_list.IsChecked(index)]
        save_data['slideList'] = slide_list_save_data

        print(save_data)
        print(json.dumps(save_data, indent=4))
        pass

    def handle_file_save_as(self, event):
        pass

