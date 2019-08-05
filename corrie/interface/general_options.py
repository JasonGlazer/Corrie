import wx


class GeneralOptionsDialog(wx.Dialog):
    CLOSE_SIGNAL_OK = 0
    CLOSE_SIGNAL_CANCEL = 1

    general_options_dict = None

    output_metric_choice = None
    units_choice = None
    chart_type_choice = None
    sort_option_choice = None
    show_cumulative_checkbox = None
    show_end_use_pie_checkbox = None
    show_end_use_monthly_checkbox = None
    num_rows_choice = None
    tab_name_field = None
    columns_of_values_list =  None

    def __init__(self, *args, **kwargs):
        super(GeneralOptionsDialog, self).__init__(*args, **kwargs)
        self.initialize_ui()

    def initialize_ui(self):
        pnl = wx.Panel(self)
        dialog_vbox = wx.BoxSizer(wx.VERTICAL)

        top_hbox = wx.BoxSizer(wx.HORIZONTAL)
        misc_option_vbox = wx.BoxSizer(wx.VERTICAL)

        output_metric_hbox = wx.BoxSizer(wx.HORIZONTAL)
        output_metric_label = wx.StaticText(pnl, label='Output Metric')
        output_metric_options = ['Source Energy Use Intensity', 'Site Energy Use Intensity','Annual CO2']
        self.output_metric_choice = wx.Choice(pnl, choices=output_metric_options)

        output_metric_hbox.Add(output_metric_label, 0, wx.ALL, 5)
        output_metric_hbox.Add(self.output_metric_choice, 1, wx.ALL, 5)
        misc_option_vbox.Add(output_metric_hbox, 0, wx.ALL, 5)

        units_hbox = wx.BoxSizer(wx.HORIZONTAL)
        units_label = wx.StaticText(pnl, label='Units')
        units_options = ['Inch-Pound', "SI (Metric)"]
        self.units_choice = wx.Choice(pnl, choices=units_options)
        units_hbox.Add(units_label, 0, wx.ALL, 5)
        units_hbox.Add(self.units_choice, 1, wx.ALL, 5)
        misc_option_vbox.Add(units_hbox, 0, wx.ALL, 5)

        chart_type_hbox = wx.BoxSizer(wx.HORIZONTAL)
        chart_type_label = wx.StaticText(pnl, label='Chart Type')
        chart_type_options = ['Horizontal Bar', 'Vertical Column', 'Vertical Line']
        self.chart_type_choice = wx.Choice(pnl, choices=chart_type_options)
        chart_type_hbox.Add(chart_type_label, 0, wx.ALL, 5)
        chart_type_hbox.Add(self.chart_type_choice, 1, wx.ALL, 5)
        misc_option_vbox.Add(chart_type_hbox, 0, wx.ALL, 5)

        sort_option_hbox = wx.BoxSizer(wx.HORIZONTAL)
        sort_option_label = wx.StaticText(pnl, label='Chart Sort Options')
        sort_option_options = ['No Sort', 'Ascending', 'Decending']
        self.sort_option_choice = wx.Choice(pnl, choices=sort_option_options)
        sort_option_hbox.Add(sort_option_label, 0, wx.ALL, 5)
        sort_option_hbox.Add(self.sort_option_choice, 1, wx.ALL, 5)
        misc_option_vbox.Add(sort_option_hbox, 0, wx.ALL, 5)

        self.show_cumulative_checkbox = wx.CheckBox(pnl, label='Show Cumulative Chart Slide')
        misc_option_vbox.Add(self.show_cumulative_checkbox, 0, wx.ALL, 5)

        self.show_end_use_pie_checkbox = wx.CheckBox(pnl, label='Show End Use Pie Chart Slide')
        misc_option_vbox.Add(self.show_end_use_pie_checkbox, 0, wx.ALL, 5)

        self.show_end_use_monthly_checkbox = wx.CheckBox(pnl, label='Show End Use Monthly Chart Slide')
        misc_option_vbox.Add(self.show_end_use_monthly_checkbox, 0, wx.ALL, 5)
        top_hbox.Add(misc_option_vbox, 0, wx.ALL, 5)

        excel_box = wx.StaticBox(pnl, -1, "Excel")
        top_border, other_border = excel_box.GetBordersForSizer()
        excel_sizer = wx.BoxSizer(wx.VERTICAL)
        excel_sizer.AddSpacer(top_border)

        num_rows_hbox = wx.BoxSizer(wx.HORIZONTAL)
        num_rows_label = wx.StaticText(excel_box, label='Number of Rows Per "Slide"')
        num_rows_options = ['10','15','20','25','30','35','40','45','50']
        self.num_rows_choice = wx.Choice(excel_box, choices=num_rows_options)
        num_rows_hbox.Add(num_rows_label, 0, wx.ALL, 5)
        num_rows_hbox.Add(self.num_rows_choice, 1, wx.ALL, 5)
        excel_sizer.Add(num_rows_hbox, 0, wx.ALL, 5)

        tab_name_hbox = wx.BoxSizer(wx.HORIZONTAL)
        tab_name_label = wx.StaticText(excel_box, label='Tab Name')
        self.tab_name_field = wx.TextCtrl(excel_box)
        tab_name_hbox.Add(tab_name_label, 0, wx.ALL, 5)
        tab_name_hbox.Add(self.tab_name_field, 1, wx.ALL, 5)
        excel_sizer.Add(self.tab_name_field, 0, wx.ALL, 5)

        columns_of_values = wx.StaticText(excel_box, label='Columns of Values')
        excel_sizer.Add(columns_of_values, 0, wx.ALL, 5)

        columns_of_values_list = ['-' for x in range(8)]
        self.columns_of_values_list = wx.CheckListBox(excel_box, 1, (80, 50), wx.DefaultSize, columns_of_values_list)
        excel_sizer.Add(self.columns_of_values_list, 1, wx.ALL | wx.EXPAND, 10)

        excel_box.SetSizer(excel_sizer)
        top_hbox.Add(excel_box, 0, wx.ALL, 5)
        dialog_vbox.Add(top_hbox, 0, wx.ALL , 5)

        ok_cancel_hbox = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(pnl, 1, "OK", size=(60, 30))
        cancel_button = wx.Button(pnl, 1, "Cancel", size=(60, 30))
        ok_cancel_hbox.Add(ok_button, 0, wx.ALL, 5)
        ok_cancel_hbox.Add(cancel_button, 0, wx.ALL, 5)
        dialog_vbox.Add(ok_cancel_hbox, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        pnl.SetSizer(dialog_vbox)
        pnl.Fit()
        self.Fit()
        self.SetTitle("General Options")

    def set_parameters(self,general_options_dict):
        self.general_options_dict = general_options_dict

        selected_index = self.output_metric_choice.FindString(self.general_options_dict['Output Metric'])
        self.output_metric_choice.SetSelection(selected_index)

        selected_index = self.chart_type_choice.FindString(self.general_options_dict['Chart Type'])
        self.chart_type_choice.SetSelection(selected_index)

        selected_index = self.units_choice.FindString(self.general_options_dict['Units'])
        self.units_choice.SetSelection(selected_index)

        selected_index = self.sort_option_choice.FindString(self.general_options_dict['Chart Sort Options'])
        self.sort_option_choice.SetSelection(selected_index)

        self.show_cumulative_checkbox.SetValue(self.general_options_dict['Show Cumulative Chart Slide'])
        self.show_end_use_pie_checkbox.SetValue(self.general_options_dict['Show End Use Pie Chart Slide'])
        self.show_end_use_monthly_checkbox.SetValue(self.general_options_dict['Show End Use Monthly Chart Slide'])

        selected_index = self.num_rows_choice.FindString(self.general_options_dict['Number of Rows Per Slide'])
        self.num_rows_choice.SetSelection(selected_index)

        self.tab_name_field.SetValue(self.general_options_dict['Tab Name'])

        columns_of_values_dict = self.general_options_dict['Columns of Values']
        list_of_columns = list(columns_of_values_dict.keys())
        self.columns_of_values_list.Set(list_of_columns)
        for column_item in list_of_columns:
            index = self.columns_of_values_list.FindString(column_item)
            self.columns_of_values_list.Check(index, columns_of_values_dict[column_item])
