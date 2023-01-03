<!-- markdownlint-disable MD046 -->

# Adding a new ML-related task and method

## Adding semantic components to a bottom-level KG schema
When extending an [existing bottom-level KG schema](https://github.com/boschresearch/ExeKGLib#bottom-level-kg-schemas), naming conventions should be followed and can be inferred by the below example code snippets. The placeholders used are specified below each snippet. For the sake of example, the namespace prefix of the ML KG schema (`ml`) is used in the following code snippets.

To add the required semantic components, the following steps should be followed:

1. Open the `.ttl` file of the desired bottom-level KG schema, found in the [relevant repo](https://github.com/nsai-uio/ExeKGOntology).
2. Add a new sub-class of [ds:AtomicTask](https://nsai-uio.github.io/ExeKGOntology/OnToology/ds_exeKGOntology.ttl/documentation/index-en.html#AtomicTask).

    ```turtle
    ml:NewTask
        rdf:type        owl:Class ;
        rdfs:subClassOf ds:AtomicTask .
    ```
    In the above example, `NewTask` should be replaced with the desired task name.
3. Add a new sub-class of [ds:AtomicMethod](https://nsai-uio.github.io/ExeKGOntology/OnToology/ds_exeKGOntology.ttl/documentation/index-en.html#AtomicMethod).

    ```turtle
    ml:NewMethod
        rdf:type        owl:Class ;
        rdfs:subClassOf ds:AtomicMethod .
    ```
    In the above example, `NewMethod` should be replaced with the desired method name.
4. Add a new sub-property of [ds:hasMethod](https://nsai-uio.github.io/ExeKGOntology/OnToology/ds_exeKGOntology.ttl/documentation/index-en.html#hasMethod).

    ```turtle
    ml:hasNewMethod
        rdf:type           owl:ObjectProperty ;
        rdfs:subPropertyOf ds:hasMethod ;
        rdfs:domain        ml:NewTask ;
        rdfs:range         ml:NewMethod .
    ```
    In the above example, `NewMethod` and `NewTask` should be replaced with the desired method and task names respectively.
5. Add and link the desired input and output entities for the new task.

    ```turtle
    ml:DataIn1NewTask
        rdf:type        owl:Class ;
        rdfs:subClassOf ds:DataEntity .
   
    ...
   
    ml:DataOut1NewTask
        rdf:type        owl:Class ;
        rdfs:subClassOf ds:DataEntity . 

    ...  
 
    ml:hasNewTaskInput
        rdf:type           owl:ObjectProperty ;
        rdfs:subPropertyOf ds:hasInput ;
        rdfs:domain        ml:NewTask ;
        rdfs:range         ml:DataIn1NewTask, ... .
   
    ml:hasNewTaskOutput
        rdf:type           owl:ObjectProperty ;
        rdfs:subPropertyOf ds:hasOutput ;
        rdfs:domain        ml:NewTask ;
        rdfs:range         ml:DataOut1NewTask, ... .
    ```
   In the above example, the occurences of number `1` in the input and output entity names should be replaced with the desired input and output names respectively. Also, `NewTask` should be replaced with the desired task name.
6. Add the desired data properties for the new method.

    ```turtle
    ml:hasNewProperty1
        rdf:type    owl:DatatypeProperty ;
        rdfs:domain ml:NewMethod ;
        rdfs:range  xsd:float .

    ml:hasNewProperty2
        rdf:type    owl:DatatypeProperty ;
        rdfs:domain ml:NewMethod ;
        rdfs:range  xsd:string .
    ```
    In the above example, `NewProperty1` and `NewProperty2` should be replaced with the desired property names.


## Adding a relevant Python class
To achieve this, a sub-class of `executable_ml_kgs.classes.task.Task` should be added to an existing module of `executable_ml_kgs.classes.tasks` package according to the conventions mentioned in the [package's documentation](../tasks-package-documentation).