import wx


class SlideOptionsDialog(wx.Dialog):
    CLOSE_SIGNAL_OK = 0
    CLOSE_SIGNAL_CANCEL = 1

    def __init__(self, *args, **kwargs):
        super(SlideOptionsDialog, self).__init__(*args, **kwargs)
        self.initialize_ui()

    def initialize_ui(self):
        pnl = wx.Panel(self)
        dialog_vbox = wx.BoxSizer(wx.VERTICAL)

        title_hbox = wx.BoxSizer(wx.HORIZONTAL)
        title_label = wx.StaticText(pnl, label='Title In Presentation')
        title_field = wx.TextCtrl(pnl, value='Aspect Ratio')
        title_hbox.Add(title_label, 0, wx.ALL, 5)
        title_hbox.Add(title_field, 1, wx.ALL, 5)
        dialog_vbox.Add(title_hbox, 0, wx.ALL, 5)

        chart_type_hbox = wx.BoxSizer(wx.HORIZONTAL)
        chart_type_label = wx.StaticText(pnl, label='Chart Type')
        chart_type_options = ['Horizontal Bar', 'Vertical Column', 'Vertical Line']
        chart_type_choice = wx.Choice(pnl, choices=chart_type_options)
        chart_type_choice.SetSelection(0)
        chart_type_hbox.Add(chart_type_label, 0, wx.ALL, 5)
        chart_type_hbox.Add(chart_type_choice, 1, wx.ALL, 5)
        dialog_vbox.Add(chart_type_hbox, 0, wx.ALL, 5)

        sort_option_hbox = wx.BoxSizer(wx.HORIZONTAL)
        sort_option_label = wx.StaticText(pnl, label='Sort Options')
        sort_option_options = ['No Sort', 'Ascending', 'Decending']
        sort_option_choice = wx.Choice(pnl, choices=sort_option_options)
        sort_option_choice.SetSelection(0)
        sort_option_hbox.Add(sort_option_label, 0, wx.ALL, 5)
        sort_option_hbox.Add(sort_option_choice, 1, wx.ALL, 5)
        dialog_vbox.Add(sort_option_hbox, 0, wx.ALL, 5)

        select_mode_hbox = wx.BoxSizer(wx.HORIZONTAL)
        select_mode_label = wx.StaticText(pnl, label='Selection Mode')
        select_mode_options = ['Automatic', 'Exclude Best Option', 'Exclude Two Best Options', 'Exclude Three Best Options']
        select_mode_choice = wx.Choice(pnl, choices=select_mode_options)
        select_mode_choice.SetSelection(0)
        select_mode_hbox.Add(select_mode_label, 0, wx.ALL, 5)
        select_mode_hbox.Add(select_mode_choice, 1, wx.ALL, 5)
        dialog_vbox.Add(select_mode_hbox, 0, wx.ALL, 5)

        incremental_checkbox = wx.CheckBox(pnl, label='Include in Incremental Improvements')
        dialog_vbox.Add(incremental_checkbox, 0, wx.ALL, 5)

        parameter_value_label = wx.StaticText(pnl, label="Parameter Values")
        dialog_vbox.Add(parameter_value_label, 0, wx.ALL, 5)

        value_options = ['0.6','0.8','1.0','1.2','1.4','1.6','1.8','2.0']
        value_choice = wx.CheckListBox(pnl, 1, (80, 50), wx.DefaultSize, value_options)
        value_choice.SetSelection(0)
        dialog_vbox.Add(value_choice, 0, wx.ALL, 5)

        ok_cancel_hbox = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(pnl, 1, "OK", size=(60, 30))
        cancel_button = wx.Button(pnl, 1, "Cancel", size=(60, 30))
        ok_cancel_hbox.Add(ok_button, 0, wx.ALL, 5)
        ok_cancel_hbox.Add(cancel_button, 0, wx.ALL, 5)
        dialog_vbox.Add(ok_cancel_hbox, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        pnl.SetSizer(dialog_vbox)
        pnl.Fit()
        self.Fit()
        self.SetTitle("Slide Options")

