from spyre import  server
import pandas as pd
from urllib.request import urlopen
import matplotlib.pyplot as plt
import numpy as np


class StockExample(server.App):
    title = "Значения"

    inputs = [{   "type":'dropdown',
                  "label": 'Индекс',
                  "options" : [ {"label": "VCI", "value":"VCI"},
                                {"label": "TCI", "value":"TCI"},
                                {"label": "VHI", "value":"VHI"},],
                  "key": 'index',
                  "action_id": "update_data"},

              {"type": 'dropdown',
               "label": 'Область',
               "options": [{"label": "Винницкая", "value": "1"},
                           {"label": "Волынская", "value": "2"},
                           {"label": "Днепропетровская", "value": "3"},
                           {"label": "Донецкая", "value": "4"},
                           {"label": "Житомирская", "value": "5"},
                           {"label": "Закарпатская", "value": "6"},
                           {"label": "Запорожская", "value": "7"},
                           {"label": "Ивано-Франковская", "value": "8"},
                           {"label": "Киевская", "value": "9"},
                           {"label": "Кировоградская", "value": "10"},
                           {"label": "Луганская", "value": "11"},
                           {"label": "Львовская", "value": "12"},
                           {"label": "Николаевская", "value": "13"},
                           {"label": "Одесская", "value": "14"},
                           {"label": "Полтавская", "value": "15"},
                           {"label": "Ровниская", "value": "16"},
                           {"label": "Сумская", "value": "17"},
                           {"label": "Тернопольская", "value": "18"},
                           {"label": "Харьковская", "value": "19"},
                           {"label": "Херсонская", "value": "20"},
                           {"label": "Хмельницкая", "value": "21"},
                           {"label": "Черкасская", "value": "22"},
                           {"label": "Черновецкая", "value": "23"},
                           {"label": "Черниговская", "value": "24"},
                           {"label": "АР Крым", "value": "25"}],
               "key": 'region',
               "action_id": "update_data"},

              {"input_type": "text",
               "variable_name": "year",
               "label": "Год",
               "value": 1981,
               "key": 'year',
               "action_id": "update_data"},

              {"type": 'slider',
               "label": 'Первая неделя',
               "min": 1, "max": 52, "value": 35,
               "key": 'first',
               "action_id": 'update_data'},

              {"type": 'slider',
               "label": 'Последняя неделя',
               "min": 1, "max": 52, "value": 35,
               "key": 'last',
               "action_id": 'update_data'}]


    controls = [{"type": "hidden",
                 "id": "update_data"}]

    tabs = ["Таблица","График"]

    outputs = [{"type": "table",
                "id": "table_id",
                "control_id": "update_data",
                "tab": "Таблица"},
               {"type": "plot",
                "id": "plot",
                "control_id": "update_data",
                "tab": "График"}]

    def getData(self, params):
        print("............")
        index = params['index']
        region = params['region']
        year = params['year']
        first = params['first']
        last = params['last']

        path = (r"files/%s.csv" % region)
        print(path)
        df = pd.read_csv(path)
        df1 = df[(df['Год'] == int(year)) & (df['Неделя'] >= int(first)) & (df['Неделя'] <= int(last))]
        df1 = df1[['Неделя', index]]
        return df1

    def getPlot(self, params):
        index = params['index']
        region = params['region']
        year = params['year']
        first = params['first']
        last = params['last']
        df = self.getData(params).set_index('Неделя')
        plt_obj = df.plot()
        plt_obj.set_ylabel(r"%s" % index)
        plt_obj.set_title('Значения {index} for {year} from {first} to {last} weeks'.format(index=index,
                                                                                         year=int(year),
                                                                                         first=int(first),
                                                                                         last=int(last)))

        fig = plt_obj.get_figure()
        return fig



app = StockExample()
app.launch(port=5555)
