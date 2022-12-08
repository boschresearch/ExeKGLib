import pandas as pd
from rdflib import Graph
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor

from utils import parse_entity
from classes.pipeline_execution.pipeline_processor import PipelineProcessor


class MLAnalyser(PipelineProcessor):
    def __init__(self, dir_out="./plots"):
        self.fig = None
        self.grid = None

        self.graph = Graph()
        self.raw_data = None
        self.dict_namespace = {}
        self.dir_out = dir_out
        self.program = None

        self.model = None
        self.extra_data_list = {}

    def LR_training(self, input_x: list, input_y: list, task_pos):
        reg = LinearRegression()
        reg.fit(input_x, input_y)
        self.model = reg
        predicted_y = reg.predict(input_x)
        # print('input_x = ', input_x)
        # print('predicted_y = ', len(predicted_y))
        # print('input_y = ', len(input_y))
        # plt.plot(predicted_y, label = 'predicted')
        # plt.plot(input_y, label = 'input')

        out_names = task_pos["exeKG:hasOutput"]
        for name in out_names:
            if "Predict" in name:
                self.extra_data_list[name] = predicted_y

        # plt.legend()
        # plt.show()
        print("LR training finished")

    def LR_testing(self, input_x: list, input_y: list, task_pos):
        reg = self.model
        assert not reg is None
        assert isinstance(reg, LinearRegression)
        predict_y = reg.predict(input_x)
        # plt.plot(input_y.index ,predict_y, label = 'predict')
        # plt.plot(input_y.index, input_y, label = 'input_y')

        out_names = task_pos["exeKG:hasOutput"]
        for name in out_names:
            if "Predict" in name:
                self.extra_data_list[name] = predict_y

        # print(self.extra_data_list)

        # plt.legend()
        # plt.show()

    def k_nearest_neighbor_train(self, input_x, input_y, task_pos, n_neighbors=3):
        print("n_neighbors = ", n_neighbors)
        knn = KNeighborsRegressor(n_neighbors=n_neighbors)
        knn.fit(input_x, input_y)

        self.model = knn
        predicted_y = knn.predict(input_x)

        out_names = task_pos["exeKG:hasOutput"]
        for name in out_names:
            if "Predict" in name:
                self.extra_data_list[name] = predicted_y

        print("KNN training finished")

    def k_nearest_neighbor_test(self, input_x, input_y, task_pos):
        knn = self.model
        assert isinstance(knn, KNeighborsRegressor)

        predicted_y = knn.predict(input_x)

        out_names = task_pos["exeKG:hasOutput"]
        for name in out_names:
            if "Predict" in name:
                self.extra_data_list[name] = predicted_y

        print("KNN testing finished")

    def mlp_train(self, input_x, input_y, task_pos, solver="adam"):
        mlp = MLPRegressor(solver=solver)
        mlp.fit(input_x, input_y)

        self.model = mlp
        predicted_y = mlp.predict(input_x)

        out_names = task_pos["exeKG:hasOutput"]
        for name in out_names:
            if "Predict" in name:
                self.extra_data_list[name] = predicted_y

        print("MLP training finished")

    def mlp_test(self, input_x, input_y, task_pos):
        mlp = self.model
        assert isinstance(mlp, MLPRegressor)

        predicted_y = mlp.predict(input_x)

        out_names = task_pos["exeKG:hasOutput"]
        for name in out_names:
            if "Predict" in name:
                self.extra_data_list[name] = predicted_y

        print("MLP testing finished")

    def ml_performance_calculation(self, task_pos):
        model = self.model
        inputs = task_pos["exeKG:hasInput"]

        real_train = 0
        real_test = 0
        predict_train = 0
        predict_test = 0

        print("inputs = ", inputs)
        for input in inputs:
            if "Train" in input and "Predict" in input:
                predict_train = self.extra_data_list[input]
            elif "Test" in input and "Predict" in input:
                predict_test = self.extra_data_list[input]
            elif "Train" in input and "Split" in input:
                real_train = self.extra_data_list[input]
                real_train = real_train[real_train.columns[-1]]
            elif "Test" in input and "Split" in input:
                real_test = self.extra_data_list[input]
                real_test = real_test[real_test.columns[-1]]

        # print(real_test)
        # print(predict_train)
        train_err = pd.DataFrame(real_train - predict_train)
        test_err = pd.DataFrame(real_test - predict_test)

        # print('train_err = ', train_err)
        # print('test_err = ', test_err)

        # plt.plot(train_err.index, train_err, label = 'train')
        # plt.plot(test_err.index, test_err, label = 'test')
        # plt.legend()
        # plt.show()

        outputs = task_pos["exeKG:hasOutput"]
        for output in outputs:
            if "Test" in output:
                self.extra_data_list[output] = test_err
            elif "Train" in output:
                self.extra_data_list[output] = train_err
            else:
                pass

        print("ml_performance_calculation finished")

    def execute_task(self, task_pos):
        """task of ML"""
        method = task_pos["exeKG:hasMethod"][0]

        input = task_pos["exeKG:hasInput"][0]
        temp = parse_entity(self.graph, input, self.dict_namespace)

        print("temp = ", temp)

        # print(self.extra_data_list)
        try:
            input_source = temp["exeKG:hasSource"][0]
            input_data = self.raw_data[input_source]
        except:
            input_data = self.extra_data_list[input]

        if "LRTrain" in method:
            x = input_data[input_data.columns[:-1]]
            y = input_data[input_data.columns[-1]]
            self.LR_training(x, y, task_pos)
        elif "LRTest" in method:
            x = input_data[input_data.columns[:-1]]
            y = input_data[input_data.columns[-1]]
            self.LR_testing(x, y, task_pos)
        elif "KNNTrain" in method:
            x = input_data[input_data.columns[:-1]]
            y = input_data[input_data.columns[-1]]
            self.k_nearest_neighbor_train(x, y, task_pos, num_exps)
        elif "KNNTest" in method:
            x = input_data[input_data.columns[:-1]]
            y = input_data[input_data.columns[-1]]
            self.k_nearest_neighbor_test(x, y, task_pos)
        elif "MLPTrain" in method:
            x = input_data[input_data.columns[:-1]]
            y = input_data[input_data.columns[-1]]
            self.mlp_train(x, y, task_pos, num_exps)
        elif "MLPTest" in method:
            x = input_data[input_data.columns[:-1]]
            y = input_data[input_data.columns[-1]]
            self.mlp_test(x, y, task_pos)
        elif "Performance" in method:
            self.ml_performance_calculation(task_pos)
        else:
            print("execute ML task")
