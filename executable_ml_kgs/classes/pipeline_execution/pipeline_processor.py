import pandas as pd

from utils import parse_namespace


class PipelineProcessor:
    def __init__(self):
        self.raw_data = None
        self.extra_data_list = {}
        print("PipelineProcessor initialized")

    def load_graph(self, kg_path=r"KG/exeKGOntology.ttl"):
        """load the KG from .ttl file into the object"""
        self.graph.parse(kg_path)

    def load_data(self, raw_path=r"data/a.csv"):
        """load the raw csv data
        Args:
            raw_path: csv file path
        """
        self.raw_data = pd.read_csv(raw_path, delimiter=",", encoding="ISO-8859-1")

    def parse_namespace(self):
        self.dict_namespace = parse_namespace(self.graph)

    def select_program(self, program, name: str = "WeldingProgramNumber"):
        # program must be int to be compared with excel data
        return self.raw_data[name] == int(program) if (program and name) else [True] * len(self.raw_data)

    def welding_program_filter(self, input, filter_value: int = 1, filter_name: str = "WeldingProgramNumber"):
        """currently only used for distinguishing filtering different program numbers"""
        # if(filter_value and filter_name):
        #     #input = self.raw_data[data_source]
        #     filter_rows = self.raw_data[filter_name]==filter_value

        #     # optionally add new column to the data base while keep the same column and index
        #     # self.raw_data[data_source + '_' + str(filter_name) + '_' + str(filter_value)] = np.NaN
        #     # self.raw_data.loc[filter_rows, data_source + '_' + str(filter_name) + '_' + str(filter_value)] = input[filter_rows]
        #     # return self.raw_data[data_source + '_' + str(filter_name) + '_' + str(filter_value)][filter_rows]
        #     return input[filter_rows]

        # else:
        #     return input
        # print('input = ', input)
        # print('select_program = ',self.select_program(filter_value, filter_name) )
        return input[self.select_program(filter_value, filter_name)]
