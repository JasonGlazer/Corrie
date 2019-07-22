import wx


class GeneralOptionsDialog(wx.Dialog):
    CLOSE_SIGNAL_OK = 0
    CLOSE_SIGNAL_CANCEL = 1

    def __init__(self, *args, **kwargs):
        super(GeneralOptionsDialog, self).__init__(*args, **kwargs)
        self.initialize_ui()

    def initialize_ui(self):
        pnl = wx.Panel(self)
        dialog_vbox = wx.BoxSizer(wx.VERTICAL)

        output_metric_hbox = wx.BoxSizer(wx.HORIZONTAL)
        output_metric_label = wx.StaticText(pnl, label='Output Metric')
        output_metric_options = ['Source Energy Use Intensity', 'Site Energy Use Intensity','Annual CO2']
        output_metric_choice = wx.Choice(pnl, choices=output_metric_options)
        output_metric_choice.SetSelection(0)

        output_metric_hbox.Add(output_metric_label, 0, wx.ALL, 5)
        output_metric_hbox.Add(output_metric_choice, 1, wx.ALL, 5)
        dialog_vbox.Add(output_metric_hbox, 0, wx.ALL, 5)

        units_hbox = wx.BoxSizer(wx.HORIZONTAL)
        units_label = wx.StaticText(pnl, label='Units')
        units_options = ['Inch-Pound', "SI (Metric)"]
        units_choice = wx.Choice(pnl, choices=units_options)
        units_choice.SetSelection(0)
        units_hbox.Add(units_label, 0, wx.ALL, 5)
        units_hbox.Add(units_choice, 1, wx.ALL, 5)
        dialog_vbox.Add(units_hbox, 0, wx.ALL, 5)

        show_cumulative_checkbox = wx.CheckBox(pnl, label='Show Cumulative Chart Slide')
        dialog_vbox.Add(show_cumulative_checkbox, 0, wx.ALL, 5)

        show_end_use_pie_checkbox = wx.CheckBox(pnl, label='Show End Use Pie Chart Slide')
        dialog_vbox.Add(show_end_use_pie_checkbox, 0, wx.ALL, 5)

        show_end_use_monthly_checkbox = wx.CheckBox(pnl, label='Show End Use Monthly Chart Slide')
        dialog_vbox.Add(show_end_use_monthly_checkbox, 0, wx.ALL, 5)

        excel_box = wx.StaticBox(pnl, -1, "Excel")
        top_border, other_border = excel_box.GetBordersForSizer()
        excel_sizer = wx.BoxSizer(wx.VERTICAL)
        excel_sizer.AddSpacer(top_border)

        num_rows_hbox = wx.BoxSizer(wx.HORIZONTAL)
        num_rows_label = wx.StaticText(excel_box, label='Number of Rows Per "Slide"')
        num_rows_options = ['10','15','20','25','30','35','40','45','50']
        num_rows_choice = wx.Choice(excel_box, choices=num_rows_options)
        num_rows_choice.SetSelection(0)
        num_rows_hbox.Add(num_rows_label, 0, wx.ALL, 5)
        num_rows_hbox.Add(num_rows_choice, 1, wx.ALL, 5)
        excel_sizer.Add(num_rows_hbox, 0, wx.ALL, 5)

        tab_name_hbox = wx.BoxSizer(wx.HORIZONTAL)
        tab_name_label = wx.StaticText(excel_box, label='Tab Name')
        tab_name_field = wx.TextCtrl(excel_box, value='CorrieResults')
        tab_name_hbox.Add(tab_name_label, 0, wx.ALL, 5)
        tab_name_hbox.Add(tab_name_field, 1, wx.ALL, 5)
        excel_sizer.Add(tab_name_hbox, 0, wx.ALL, 5)

        columns_of_values = wx.StaticText(excel_box, label='Columns of Values')
        excel_sizer.Add(columns_of_values, 0, wx.ALL, 5)

        slide_list_text = ['Source Energy Use Intensity', 'Site Energy Use Intensity', 'Total Source Energy',
                           'Total Site Energy', 'Total CO2', 'Cooling Energy', 'Heating Energy', 'Lighting Energy',
                           'Plug Energy', 'Total Electricity Usage', 'Total Natural Gas Usage']
        slide_list = wx.CheckListBox(excel_box, 1, (80, 50), wx.DefaultSize, slide_list_text)
        excel_sizer.Add(slide_list, 1, wx.ALL, 10)

        excel_box.SetSizer(excel_sizer)
        dialog_vbox.Add(excel_box, 0, wx.ALL, 5)

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

