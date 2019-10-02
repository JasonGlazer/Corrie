import os

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches


class UpdatePresentation(object):

    def __init__(self, saved_data, collected_results, current_corrie_file_name):
        self.saved_data = saved_data
        self.collected_results = collected_results
        self.current_corrie_file_name = current_corrie_file_name

    def test1(self):
        # create presentation with 1 slide ------
        prs = Presentation()
        slide = prs.slides.add_slide(prs.slide_layouts[5])

        # define chart data ---------------------
        chart_data = CategoryChartData()
        chart_data.categories = ['East', 'West', 'Midwest']
        chart_data.add_series('Series 1', (19.2, 21.4, 16.7))

        # add chart to slide --------------------
        x, y, cx, cy = Inches(2), Inches(2), Inches(6), Inches(4.5)
        slide.shapes.add_chart(
            XL_CHART_TYPE.BAR_CLUSTERED, x, y, cx, cy, chart_data
        )

        pptx_file = self.saved_data['powerpointPath']
        prs.save(pptx_file)

    def create_slides(self):
        prs = Presentation()

        for slide_name in self.collected_results:

            category_list = []
            series_data = []
            slide_results = self.collected_results[slide_name]
            for option_name in slide_results:
                category_list.append(option_name)
                option_results = slide_results[option_name]
                series_data.append(option_results['net_site_energy'])
            # define chart data ---------------------
            if series_data:
                slide = prs.slides.add_slide(prs.slide_layouts[5])

                chart_data = CategoryChartData()
                chart_data.categories = category_list
                print('chart_data.categories: ', chart_data.categories)
                print('tuple(series_data): ', tuple(series_data))
                chart_data.add_series('Series 1', tuple(series_data))

                # add chart to slide --------------------
                x, y, cx, cy = Inches(2), Inches(2), Inches(6), Inches(4.5)
                slide.shapes.add_chart(
                    XL_CHART_TYPE.BAR_CLUSTERED, x, y, cx, cy, chart_data
                )
                print('created slide named: ',slide_name)

        pptx_file = self.saved_data['powerpointPath']
        prs.save(pptx_file)
