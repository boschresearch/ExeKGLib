from rdflib import Graph, URIRef, RDF, Namespace, Literal

g = Graph(bind_namespaces="rdflib")
g1 = Graph(bind_namespaces="rdflib")
exekg_namespace = Namespace("http://www.semanticweb.org/zhuoxun/ontologies/exeKG#")
g.bind("exeKG", exekg_namespace)
namespaceDict = {}
taskTypeDict = {}
methodTypeDict = {}
dataEntityDict = {}


def readOntology(url):
    g1.parse("kg/" + url)
    namespaceDict = g1.namespace_manager.__dict__["_NamespaceManager__trie"].copy()
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
    userPipeline = "test"
    pipelineName = userPipeline + "Pipeline"
    outputFile = "kg/" + pipelineName + ".ttl"
    addTask(pipelineName, "Pipeline")
    addMethod(methodTypeDict)
    addDataEntity(dataEntityDict)

    with open(outputFile, "w") as f:
        f.write((g1 + g).serialize())


def addTask(itemName, itemType):
    new_item_name = URIRef(exekg_namespace + itemName)
    new_item_type = URIRef(exekg_namespace + itemType)
    g.add((new_item_name, RDF.type, new_item_type))
    if itemType == "Pipeline":
        prompt = "Enter inputs of the pipeline, enter 'quit' to stop input: "
        inputStr = input(prompt)
        if inputStr != "quit":
            dataEntityDict[inputStr] = {
                "DataStructure": "Array",
                "DataSemantics": "?",
            }  # TODO: input system
            inputInstance = URIRef(exekg_namespace + inputStr)
            g.add((new_item_name, exekg_namespace.hasInput, inputInstance))
        while inputStr != "quit":
            inputStr = input(prompt)
            if inputStr != "quit":
                dataEntityDict[inputStr] = {
                    "DataStructure": "Array",
                    "DataSemantics": "?",
                }  # TODO: input system
                inputInstance = URIRef(exekg_namespace + inputStr)
                g.add((new_item_name, exekg_namespace.hasInput, inputInstance))

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
            nextTaskInstance = URIRef(exekg_namespace + nextTaskName)
            g.add((new_item_name, exekg_namespace.hasStartTask, nextTaskInstance))
        if nextTaskFlag == 1:
            nextTaskType = "StatisticTask"
            nextTaskName = nameTaskWithType(nextTaskType, taskTypeDict)
            nextTaskInstance = URIRef(exekg_namespace + nextTaskName)
            g.add((new_item_name, exekg_namespace.hasStartTask, nextTaskInstance))
        if nextTaskFlag == 2:
            nextTaskType = "MLTask"
            nextTaskName = nameTaskWithType(nextTaskType, taskTypeDict)
            nextTaskInstance = URIRef(exekg_namespace + nextTaskName)
            g.add((new_item_name, exekg_namespace.hasStartTask, nextTaskInstance))

        addTask(nextTaskName, nextTaskType)
    else:
        # Method
        method_propertyQuery = (
            "\nSELECT ?p ?m WHERE {?p rdfs:domain exeKG:" + itemType + " . "
            "?p rdfs:range ?m . "
            "?m rdfs:subClassOf exeKG:AtomicMethod . }"
        )  # method property
        i = 0
        methodList = []
        print("Please enter available Method for {}:".format(itemType))
        for pair in list(g1.query(method_propertyQuery)):
            tmpMethod = pair[1].split("#")[1]
            print("\t{}. {}".format(str(i), tmpMethod))
            methodList.append(tmpMethod)
            i += 1
        methodID = int(input())
        methodType = methodList[methodID]
        methodName = nameMethodWithType(methodType, methodTypeDict)
        hasMethodInstance = URIRef(pair[0])
        methodInstance = URIRef(pair[1] + methodName)
        g.add((new_item_name, hasMethodInstance, methodInstance))

        # data
        # pick data from dataEntityDict, according to allowedDataStructure of methodType

        # DatatypeProperty
        methodDatatypePropertyQuery = (
            "\nSELECT ?p ?r WHERE {?p rdfs:domain exeKG:" + methodType + " . "
            "?p rdfs:range ?r . "
            "?p rdf:type owl:DatatypeProperty . }"
        )
        propertyList = list(g1.query(methodDatatypePropertyQuery))
        if propertyList:
            print("Please enter requested properties for {}:".format(methodType))
            for pair in propertyList:
                propertyInstance = URIRef(pair[0])
                range = pair[1].split("#")[1]
                rangeInstance = URIRef(pair[1])

                inputProperty = Literal(
                    input("\t{} in range({}): ".format(pair[0].split("#")[1], range)),
                    datatype=rangeInstance,
                )
                g.add((new_item_name, propertyInstance, inputProperty))

        # Next Task
        nextTaskQuery = "\nSELECT ?t WHERE {?t rdfs:subClassOf exeKG:AtomicTask . }"
        i = 0
        atomicTaskList = []
        print("Please enter the next Task:")
        for t in list(g1.query(nextTaskQuery)):
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
            taskInstance = URIRef(taskNamespace + taskName)
            g.add((new_item_name, exekg_namespace.hasNextTask, taskInstance))
            addTask(taskName, taskType)


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


def addMethod(methodTypeDict):
    for methodType in methodTypeDict.keys():
        methodInstance = URIRef(
            exekg_namespace + nameMethodWithType(methodType, methodTypeDict)
        )
        methodType = URIRef(exekg_namespace + methodType)
        g.add((methodInstance, RDF.type, methodType))


def addDataEntity(dataEntityDict):  # TODO
    for dataEntity in dataEntityDict.keys():
        dataEntityInstance = URIRef(exekg_namespace + dataEntity)
        g.add((dataEntityInstance, RDF.type, exekg_namespace.DataEntity))
        dataStructureType = URIRef(
            exekg_namespace + dataEntityDict[dataEntity]["DataStructure"]
        )
        g.add((dataEntityInstance, exekg_namespace.hasDataStructure, dataStructureType))
        dataSemanticsType = URIRef(
            exekg_namespace + dataEntityDict[dataEntity]["DataSemantics"]
        )
        g.add((dataEntityInstance, exekg_namespace.hasDataSemantics, dataSemanticsType))


if __name__ == "__main__":
    url = "exeKGOntology.ttl"
    namespaceDict = readOntology(url)
    pipelineCreation()
