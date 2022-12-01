# -*- coding: utf-8 -*-
"""
Created on Wed May 11 15:21:19 2022

@author: Zhuoxun
"""

from rdflib import Graph
import os


# dir_working = r'../../../../Downloads/exeKG'
# os.chdir(dir_working)

g = Graph()
namespaceDict = {}
# itemDict = {}
taskTypeDict = {}
methodTypeDict = {}
dataEntityDict = {}


def readOntology(url):
    g.parse("kg/" + url)
    namespaceDict = g.namespace_manager.__dict__["_NamespaceManager__trie"].copy()
    for key in namespaceDict:
        if key == "http://www.w3.org/XML/1998/namespace":
            namespaceDict[key] = "xml:"
        elif key == "http://www.w3.org/1999/02/22-rdf-syntax-ns#":
            namespaceDict[key] = "rdf:"
        elif key == "http://www.w3.org/2000/01/rdf-schema#":
            namespaceDict[key] = "rdfs:"
        elif key == "http://www.w3.org/2001/XMLSchema#":
            namespaceDict[key] = "xsd:"
        elif key == "http://www.w3.org/2002/07/owl#":
            namespaceDict[key] = "owl:"
        else:
            namespaceDict[key] = key.split("/")[-1].replace("#", ":")
    return namespaceDict


def pipelineCreation():
    # userPipeline = input("Pipeline name: ")
    userPipeline = "test"
    pipelineName = userPipeline + "Pipeline"
    outputFile = "kg/" + pipelineName + ".ttl"
    f = open(outputFile, "w")
    # f.write(":{} rdf:type {} ".format(pipelineName, ":Pipeline ;"))
    # addNextTask(f, 0)
    addTask(f, pipelineName, "Pipeline")
    # addItem(f, pipelineName, ':Task')
    addMethod(f, methodTypeDict)
    addDataEntity(f, dataEntityDict)

    f.close()


def addTask(f, itemName, itemType):
    # obj = input("Please enter the next task:\n\t1: Visual Task\n\t2: Statistic Task\n\t3. ML Task\n\t4. End Pipeline.:\n")
    f.write("\n\nexeKG:{} rdf:type exeKG:{} ".format(itemName, itemType))
    if itemType == "Pipeline":
        prompt = "Enter inputs of the pipeline, enter 'quit' to stop input: "
        inputStr = input(prompt)
        if inputStr != "quit":
            dataEntityDict[inputStr] = {
                "DataStructure": "Array",
                "DataSemantics": "?",
            }  # TODO: input system
            f.write(";\n\t exeKG:hasInput exeKG:{} ".format(inputStr))
        while inputStr != "quit":
            inputStr = input(prompt)
            if inputStr != "quit":
                dataEntityDict[inputStr] = {
                    "DataStructure": "Array",
                    "DataSemantics": "?",
                }  # TODO: input system
                f.write(",\n\t\t\t exeKG:{} ".format(inputStr))

        nextTaskFlag = int(
            input(
                "Please enter the next task:\n\t0: Visual Task\n\t1: Statistic Task\n\t2. ML Task:\n"
            )
        )
        if (
            nextTaskFlag == 0
        ):  # TODO: only visualPipeline has initial Task(CanvasTask), maybe in ontology set a class as "initialTask"
            nextTaskType = "CanvasTask"
            nextTaskName = nameTaskWithType(nextTaskType, taskTypeDict)
            f.write(";\n\t exeKG:hasStartTask {} .".format("exeKG:" + nextTaskName))
        if nextTaskFlag == 1:
            nextTaskType = "StatisticTask"
            nextTaskName = nameTaskWithType(nextTaskType, taskTypeDict)
            f.write(";\n\t exeKG:hasStartTask {} .".format("exeKG:" + nextTaskName))
        if nextTaskFlag == 2:
            nextTaskType = "MLTask"
            nextTaskName = nameTaskWithType(nextTaskType, taskTypeDict)
            f.write(";\n\t exeKG:hasStartTask {} .\n".format("exeKG:" + nextTaskName))
        addTask(f, nextTaskName, nextTaskType)
    else:
        # Method
        method_propertyQuery = (
            "\nSELECT ?p ?m WHERE {?p rdfs:domain :" + itemType + " . "
            "?p rdfs:range ?m . "
            "?m rdfs:subClassOf :AtomicMethod . }"
        )  # method property
        i = 0
        methodList = []
        print("Please enter available Method for {}:".format(itemType))
        for pair in list(g.query(method_propertyQuery)):
            # method = namespaceDict[methodNamespace] + pair[1].split('#')[1]
            tmpMethod = pair[1].split("#")[1]
            print("\t{}. {}".format(str(i), tmpMethod))
            methodList.append(tmpMethod)
            i += 1
        methodID = int(input())
        methodType = methodList[methodID]
        methodName = nameMethodWithType(methodType, methodTypeDict)
        hasMethodPropertyNamespace = pair[0].split("#")[0] + "#"
        methodNamespace = pair[1].split("#")[0] + "#"
        hasMethodProperty = (
            namespaceDict[hasMethodPropertyNamespace] + pair[0].split("#")[1]
        )
        method = namespaceDict[methodNamespace] + methodName
        f.write(" ;\n\t {} {} ".format(hasMethodProperty, method))
        # data
        # pick data from dataEntityDict, according to allowedDataStructure of methodType

        # DatatypeProperty
        methodDatatypePropertyQuery = (
            "\nSELECT ?p ?r WHERE {?p rdfs:domain :" + methodType + " . "
            "?p rdfs:range ?r . "
            "?p rdf:type owl:DatatypeProperty . }"
        )  # datatype property
        propertyList = list(g.query(methodDatatypePropertyQuery))
        if propertyList:
            print("Please enter requested properties for {}:".format(methodType))
            for pair in propertyList:
                propertyNamespace = pair[0].split("#")[0] + "#"
                property = namespaceDict[propertyNamespace] + pair[0].split("#")[1]
                range = pair[1].split("#")[1]
                inputProperty = input(
                    "\t{} in range({}): ".format(pair[0].split("#")[1], range)
                )
                rangeNamespace = pair[1].split("#")[0] + "#"
                f.write(
                    ' ;\n\t {} "{}"^^{} '.format(
                        property, inputProperty, namespaceDict[rangeNamespace] + range
                    )
                )

        # Next Task
        nextTaskQuery = "\nSELECT ?t WHERE {?t rdfs:subClassOf :AtomicTask . }"
        i = 0
        atomicTaskList = []
        print("Please enter the next Task:")
        for t in list(g.query(nextTaskQuery)):
            # method = namespaceDict[methodNamespace] + pair[1].split('#')[1]
            tmpTask = t[0].split("#")[1]
            print("\t{}. {}".format(str(i), tmpTask))
            atomicTaskList.append(tmpTask)
            i += 1
        print("\t{}. End pipeline".format(str(-1)))
        taskID = int(input())
        if taskID != -1:
            taskType = atomicTaskList[taskID]
            taskName = nameTaskWithType(taskType, taskTypeDict)
            taskNamespace = t[0].split("#")[0] + "#"
            task = namespaceDict[taskNamespace] + taskName
            f.write(";\n\t exeKG:hasNextTask {} .".format(task))
            addTask(f, taskName, taskType)
        else:
            f.write(" .")

    # cquery = "\nSELECT ?s WHERE {?s rdfs:domain :" + itemType + ".}" # property
    # nextTaskFlag = 3
    # for e in list(g.query(cquery)):
    #     propName = e[0].split('#')[1]
    #     propNamespace = e[0].split('#')[0] + '#'
    #     prop = namespaceDict[propNamespace] + propName
    #     # prop = propName
    #     if propName.find('Method') != -1:  #hasVisual/ML/StatisticMethod
    #         print("Please enter available Method:")
    #         methodQuery = "\nSELECT ?s WHERE {?s rdfs:subClassOf :" + propName.strip('has') + ".}" # Visual/Stats/MLMethod
    #         i = 0
    #         methodList = []
    #         for m in list(g.query(methodQuery)):
    #             methodNamespace = m[0].split('#')[0] + '#'
    #             method = namespaceDict[methodNamespace] + m[0].split('#')[1]
    #             print("\t{}. {}".format(str(i), m[0].split('#')[1]))
    #             methodList.append(method)
    #             i+=1
    #         methodID = int(input())
    #         methodName = nameMethodWithType(methodList[methodID], methodTypeDict)
    #         f.write(" ;\n\t {} {} ".format(prop, methodName))
    #
    #     if propName == "hasStartTask" or propName == "hasNextTask":
    #         nextTaskFlag = int(input("Please enter the next task:\n\t0: Visual Task\n\t1: Statistic Task\n\t2. ML Task\n\t3. End Pipeline.:\n"))
    #         if nextTaskFlag == 0:
    #             nextTaskType = 'VisualTask'
    #             nextTaskName = nameTaskWithType(nextTaskType, taskTypeDict)
    #             f.write(";\n\t {} {} ".format(prop, 'exeKG:' + nextTaskName))
    #         if nextTaskFlag == 1:
    #             nextTaskType = 'StatisticTask'
    #             nextTaskName = nameTaskWithType(nextTaskType, taskTypeDict)
    #             f.write(";\n\t {} {} ".format(prop, 'exeKG:' + nextTaskName))
    #         if nextTaskFlag == 2:
    #             nextTaskType = 'MLTask'
    #             nextTaskName = nameTaskWithType(nextTaskType, taskTypeDict)
    #             f.write(";\n\t {} {} ".format(prop, 'exeKG:' + nextTaskName))
    #
    # f.write(".\n")
    # if nextTaskFlag != 3:
    #     print(nextTaskName, nextTaskType)
    #     addTask(f, nextTaskName, nextTaskType)


def nameTaskWithType(itemType, itemTypeDict):
    if itemType not in itemTypeDict:
        itemTypeDict[itemType] = 1
    else:
        itemTypeDict[itemType] += 1
    itemName = itemType + str(itemTypeDict[itemType])
    return itemName


def nameMethodWithType(methodType, methodTypeDict):
    if methodType not in methodTypeDict:
        methodTypeDict[methodType] = 0
    methodName = methodType + "0"
    return methodName


def addMethod(f, methodTypeDict):
    for methodType in methodTypeDict.keys():
        f.write("\n\nexeKG:{} rdf:type exeKG:{} .".format(methodType + "0", methodType))


def addDataEntity(f, dataEntityDict):  # TODO
    for dataEntity in dataEntityDict.keys():
        f.write("\n\nexeKG:{} rdf:type exeKG:DataEntity ;".format(dataEntity))
        f.write(
            "\n\t exeKG:hasDataStructure exeKG:{} ;".format(
                dataEntityDict[dataEntity]["DataStructure"]
            )
        )
        f.write(
            '\n\t exeKG:hasDataSemantics "{}" .'.format(
                dataEntityDict[dataEntity]["DataSemantics"]
            )
        )


if __name__ == "__main__":
    url = "exeKGOntology.ttl"
    namespaceDict = readOntology(url)
    pipelineCreation()
