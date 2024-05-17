<!-- markdownlint-disable MD046 -->

# Adding a new ML-related task and method

## A) Adding semantic components to a bottom-level KG schema and SHACL shapes graph
While extending an [existing bottom-level KG schema](https://github.com/boschresearch/ExeKGLib#kg-schemata), naming conventions should be followed and can be inferred by the below template snippets. The placeholders used are specified below each snippet.

🗒️ **Note**: For the sake of example, in this guide we use the namespace prefix of the Machine Learning KG schema (`ml`).

To add the required semantic components:

1. Clone the [repo with the KG schemata](https://github.com/nsai-uio/ExeKGOntology).
2. Open `{prefix}_exeKGOntology.ttl` after replacing `{prefix}` with the namespace prefix of the desired bottom-level KG schema. `ml` for Machine Learning, `stats` for Statistics and `visu` for Visualization.
3. [❗ **This step is optional**: Perform only if the new method cannot be "thematically associated" with an existing sub-class of `ds:AtomicTask`]

    For **creating a new task**, there are 2 cases:

    - ✳️**Case 1**: If the new task can "thematically belong" under an existing task class that is a sub-class of `ds:Task`.
    - ✳️**Case 2**: If the new task **cannot** "thematically belong" under an existing task class that is a sub-class of `ds:Task` and needs to be standalone.

    The steps to create the task are the following and **some parts vary depending on the applicable case**:

    1. Add a new sub-class of [ds:AtomicTask](https://nsai-uio.github.io/ExeKGOntology/OnToology/ds_exeKGOntology.ttl/documentation/index-en.html#https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/ds_exeKGOntology.ttl#AtomicTask).
        ```turtle
        ml:{NewTask}
            a               owl:Class ;
            rdfs:subClassOf ml:{UpperTaskClass},    # this relationship is ONLY for *Case 1*
                            ds:AtomicTask .
        ```
        **In the above template**:
        - 🗒️ **Note**: If ✳️**Case 2** applies, then the relationship `rdfs:subClassOf ml:{UpperTaskClass}` is not needed.
        - `{NewTask}` should be replaced with the new task's **unique** name in **camel-case**.
        - `{UpperTaskClass}` should be replaced with an existing task class under which the new task belongs. That task class must be a sub-class of `ds:Task`. Available task classes can be found in the [bottom-level KG schemata](https://github.com/boschresearch/ExeKGLib#kg-schemata). <br>✍️ For **example**, if the new task is a specific type of classification, then the `{UpperTaskClass}` should be replaced with `Classification`.
    2. Add a new property that will connect the new task with the new method.
        ```turtle
        ml:has{NewTask}Method
            a                  owl:ObjectProperty ;
            rdfs:subPropertyOf ml:{UpperTaskToMethodProperty} ;
            rdfs:domain        ml:{NewTask} ;
            rdfs:range         ml:{NewMethod}Method .
        ```
        **In the above template**:
        - `{NewTask}` should be replaced with the new task's name from Step 3.a.
        - `{UpperTaskToMethodProperty}` should be replaced with an existing task-to-method property under which the new property belongs. Available task-to-method properties can be found in the [bottom-level KG schemata](https://github.com/boschresearch/ExeKGLib#kg-schemata).
        - `{NewMethod}` should be replaced with the new method's **unique** name in **camel-case** (see **next Steps** for how to **create a new method**). <br>✍️ For **example**, if the new task belongs under the `ml:Classification` task which belongs under the `ml:Train` task, then `{UpperTaskToMethodProperty}` should be `hasTrainMethod`.

    3. Add a new SHACL shape for task-to-method link in `ml_shacl_shapes.ttl` or in `generated_schemata/generated_ml_shacl_shapes.ttl` (replace `ml` with the chosen schema's namespace prefix).
        ```turtle
        :{NewTask}TaskMethodShape
            a              sh:NodeShape ;
            sh:targetClass ml:{NewTask} ;
            sh:property [
                sh:path ml:has{NewTask}Method ;
                sh:minCount 1 ;
                sh:maxCount 1 ;
                sh:or (
                    [ sh:class ml:{NewMethod} ]
                ) ;
                sh:message "Tasks of type {NewTask} must be connected with exactly one compatible atomic method." ;
            ] .
        ```
        **In the above template**:
        - If needed, the constraints (e.g. `sh:minCount 1`) should be modified/removed and more should be added.
        - `{NewTask}` should be replaced with the new task's name from Step 3.a.
        - `{NewMethod}` should be replaced with the new method's name (see **next Steps** for how to **create a new method**).

    4. [🗒️ **Note**: Perform this step only if ✳️**Case 2** applies. For existing tasks, the inputs and outputs for each task are defined in the [bottom-level KG schemata](https://github.com/boschresearch/ExeKGLib#kg-schemata) as inputs and outputs of the top-level task classes. <br>✍️ For **example**, any task that belongs under the `ml:Train` task, will receive two inputs `ml:DataInTrainX` and `ml:DataInTrainY`, and produce an output `ml:DataOutTrainModel`.]

        Add the input and output as sub-classes of [ds:DataEntity](https://nsai-uio.github.io/ExeKGOntology/OnToology/ds_exeKGOntology.ttl/documentation/index-en.html#https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/ds_exeKGOntology.ttl#DataEntity) and link them to the new task.
        ```turtle
        ml:{Input1}
            a               owl:Class ;
            rdfs:subClassOf ds:DataEntity,
                            {Input1DataStructures} .

        ...

        ml:{InputN}
            a               owl:Class ;
            rdfs:subClassOf ds:DataEntity,
                            {InputNDataStructures} .

        ml:{Output1}
            a               owl:Class ;
            rdfs:subClassOf ds:DataEntity,
                            {Output1DataStructures} .

        ...

        ml:{OutputN}
            a               owl:Class ;
            rdfs:subClassOf ds:DataEntity,
                            {OutputNDataStructures} .

        ml:has{NewTask}Input
            a                  owl:ObjectProperty ;
            rdfs:subPropertyOf ds:hasInput ;
            rdfs:domain        ml:{NewTask} ;
            rdfs:range         ml:{Input1},
                               ...
                               ml:{InputN} .

        ml:has{NewTask}Output
            a                  owl:ObjectProperty ;
            rdfs:subPropertyOf ds:hasOutput ;
            rdfs:domain        ml:{NewTask} ;
            rdfs:range         ml:{Output1},
                               ...
                               ml:{OutputN} .
        ```
        **In the above template**:

        - `{NewTask}` should be replaced with the new task's name from Step 3.a.
        - `{Input1}`, ..., `{InputN}` and `{Output1}`, ..., `{OutputN}` should be replaced with **unique** input and output names in **camel-case**, respectively.
        - `{Input1DataStructures}`, ..., `{InputNDataStructures}` and `{Output1DataStructures}`, ..., `{OutputNDataStructures}` should be replaced with (lists of) names of sub-classes of [ds:DataStructure](https://nsai-uio.github.io/ExeKGOntology/OnToology/ds_exeKGOntology.ttl/documentation/index-en.html#https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/ds_exeKGOntology.ttl#DataStructure) (i.e. `ds:Vector`, `ds:Matrix` etc.). Available data structure classes can be found in the [**top-level** KG schema](https://github.com/boschresearch/ExeKGLib#kg-schemata).

    5. [🗒️ **Note**: Perform this step only if ✳️**Case 2** applies. For existing tasks, the input and output SHACL shapes for each task are defined in the bottom-level SHACL shape graphs (e.g. `ml_shacl_shapes.ttl`) as input and output SHACL shapes of the top-level task classes. <br>✍️ For **example**, for any task that belongs under the `ml:Train` task, the corresponding shape is `:TrainTaskInputOutputShape`]

        Add a new SHACL shape in `ml_shacl_shapes.ttl` (replace `ml` with the chosen schema's namespace prefix).
        ```turtle
        :{NewTask}TaskInputOutputShape
            a              sh:NodeShape ;
            sh:targetClass ml:{NewTask} ;

            # input
            sh:property [
                sh:path ml:has{NewTask}Input ;
                sh:qualifiedMinCount 1 ;
                sh:qualifiedMaxCount 1 ;
                sh:qualifiedValueShape [
                    sh:class ml:{Input1} ;
                ] ;
                sh:message "Tasks of type {NewTask} must be connected with exactly one input of type {Input1}." ;
            ] ;

            ...

            sh:property [
                sh:path ml:has{NewTask}Input ;
                sh:qualifiedMinCount 1 ;
                sh:qualifiedMaxCount 1 ;
                sh:qualifiedValueShape [
                    sh:class ml:{InputN} ;
                ] ;
                sh:message "Tasks of type {NewTask} must be connected with exactly one input of type {InputN}." ;
            ] ;

            # output
            sh:property [
                sh:path ml:has{NewTask}Output ;
                sh:qualifiedMinCount 1 ;
                sh:qualifiedMaxCount 1 ;
                sh:qualifiedValueShape [
                    sh:class ml:{Output1} ;
                ] ;
                sh:message "Tasks of type {NewTask} must be connected with exactly one input of type {Output1}." ;
            ] ;

            ...

            sh:property [
                sh:path ml:has{NewTask}Output ;
                sh:qualifiedMinCount 1 ;
                sh:qualifiedMaxCount 1 ;
                sh:qualifiedValueShape [
                    sh:class ml:{OutputN} ;
                ] ;
                sh:message "Tasks of type {NewTask} must be connected with exactly one input of type {OutputN}." ;
            ] .
        ```
        **In the above template**:

        - If needed, the constraints (e.g. `sh:qualifiedMinCount 1`) should be modified/removed and more should be added.
        - `{NewTask}` should be replaced with the new task's name from Step 3.a.
        - `{Input1}`, ..., `{InputN}` and `{Output1}`, ..., `{OutputN}` should be replaced with the input and output names from Step 3.e.

4. In `ml_exeKGOntology.ttl` or in `generated_schemata/generated_ml_ontologies_combined.ttl`, add a new sub-class of [ds:AtomicMethod](https://nsai-uio.github.io/ExeKGOntology/OnToology/ds_exeKGOntology.ttl/documentation/index-en.html#https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/ds_exeKGOntology.ttl#AtomicMethod) together with its Python module hierarchy (replace `ml` with the chosen schema's namespace prefix).
    ```turtle
    ml:{NewMethod}Method
        a               owl:Class ;
        rdfs:subClassOf ml:{UpperMethodClass},
                        ml:{Module1},
                        ds:AtomicMethod .

    ml:{Module1}
        a               owl:Class ;
        rdfs:subClassOf ml:{Module2} .

    ml:{Module2}
        a               owl:Class ;
        rdfs:subClassOf ml:{Module3} .

    ...

    ml:{ModuleN}
        a               owl:Class ;
        rdfs:subClassOf ds:Module .
    ```
    **In the above template**:
    - `{NewMethod}` should be replaced with the new method's **unique** name in **camel-case**.
    - `{UpperMethodClass}` should be replaced with an existing method class under which the new method belongs. That method class must be a sub-class of `ds:Method`. Available method classes can be found in the [bottom-level KG schemata](https://github.com/boschresearch/ExeKGLib#kg-schemata). <br>✍️ For **example**, if the new method is linked to the `ml:BinaryClassification` task which belongs under the `ml:Train` task, then `{UpperMethodClass}` should be replaced with `TrainMethod`.
    - The hierarchy of modules shown above is: `{Module1}` -> `{Module2}` -> `{Module3}` -> ... -> `{ModuleN}`. This represents a hierarchy of Python modules with their names in **camel-case**. <br>✍️ For **example**, if the implementation of the new method is in the Python module `example_module2.example_module1.example_new_method`, then `{Module1}` is replaced by `ExampleModule1`, `{Module2}` is replaced by `ExampleModule2`, and `{NewMethod}` is replaced by `ExampleNewMethod`.

5. [🗒️ **Note**: If the optional Step 3 was performed, this step can be skipped]

    To link the method to an existing task:

    1. Find the definition of property `ml:has{TaskClass}Method` in `generated_schemata/generated_ml_ontologies_combined.ttl` (replace `ml` with the chosen schema's namespace prefix). Here, `{TaskClass}` should be replaced with an existing task class that the new method solves. That task class must be a sub-class of `ds:AtomicTask`. <br>✍️ For **example**, if the new method performs binary classification then `{TaskClass}` should be replaced with `BinaryClassification`.
    2. In the set of existing values of `rdfs:range` property, add `ml:{NewMethod}Method`. Here, `{NewMethod}` should be replaced with the new method's name from Step 4.
    3. Find the definition of SHACL shape `:{TaskClass}TaskMethodShape` in `generated_schemata/generated_ml_shacl_shapes.ttl` (replace `ml` with the chosen schema's namespace prefix). Here, `{TaskClass}` should be replaced with an existing task class that the new method solves. <br>✍️ For **example**, if the new method performs binary classification then `{TaskClass}` should be replaced with `BinaryClassification`.
    4. In the set of existing values of `sh:or` that is under `sh:property`, add `[ sh:class ml:{NewMethod}Method ]`. Here, `{NewMethod}` should be replaced with the new method's name from Step 4.

6. Add the desired parameters as data properties for the new method.
    ```turtle
    ml:hasParam{NewParam1}
        a                  owl:DatatypeProperty ;
        rdfs:domain        ml:{NewMethod}Method ;
        rdfs:range         {Range1} ;
        rdfs:subPropertyOf ds:hasParameter .

    ml:hasParam{NewParam2}
        a                  owl:DatatypeProperty ;
        rdfs:domain        ml:{NewMethod}Method ;
        rdfs:range         {Range2} ;
        rdfs:subPropertyOf ds:hasParameter .
    ```
    **In the above template**:
    - `{NewParam1}` and `{NewParam2}` should be replaced with **unique** parameter names in **camel-case**.
    - `{NewMethod}` should be replaced with the new method's name from Step 4.
    - `{Range1}` and `{Range2}` should be replaced with the desired literal value ranges (e.g. `xsd:float`).

7. Add a new SHACL shape for method-to-parameter link(s) either in `ml_shacl_shapes.ttl` or in `generated_schemata/generated_ml_shacl_shapes.ttl` (replace `ml` with the chosen schema's namespace prefix).
    ```turtle
    :{NewMethod}ParameterShape
        a              sh:NodeShape ;
        sh:targetClass ml:{NewMethod} ;
        sh:property [
            sh:path ml:hasParam{NewParam1} ;
            sh:maxCount 1 ;
            sh:or (
                [ sh:datatype {NewParam1Type1} ]
                ...
                [ sh:datatype {NewParam1TypeN} ]
            ) ;
            sh:message "Method {NewMethod} must have at most one compatible value for parameter hasParam{NewParam1}." ;
        ] ;

        ...

        sh:property [
            sh:path ml:hasParam{NewParamN} ;
            sh:maxCount 1 ;
            sh:or (
                [ sh:datatype {NewParamNType1} ]
                ...
                [ sh:datatype {NewParamNTypeN} ]
            ) ;
            sh:message "Method {NewMethod} must have at most one compatible value for parameter hasParam{NewParamN}." ;
        ] .
    ```
    **In the above template**:
    - If needed, the constraints (e.g. `sh:maxCount 1`) should be modified/removed and more should be added.
    - `{NewMethod}` should be replaced with the new method's name from Step 4.
    - `{NewParam1}`, ..., `{NewParamN}` should be replaced with the new parameters' names from Step 6.
    - `{NewParam1Type1}`, ..., `{NewParamNTypeN}` should be replaced with compatible literal types for the new parameter(s).

8.  Modify `config.py` in `exe_kg_lib` package to update the value of `KG_SCHEMAS_DIR` to point to the cloned repo's directory from Step 1.

## B) Modifying the relevant Python code
🗒️ **Note**: While modifying the code, consider refering to the conventions mentioned in the [tasks package's documentation](../tasks-package-documentation).

To modify the relevant Python code:

1. Find the **relevant sub-class** of `exe_kg_lib.classes.task.Task` in the **corresponding file** of the `exe_kg_lib.classes.tasks` package.
    - The **corresponding file** depends on the KG schema that was extended in [Section A of this guide](#a-adding-semantic-components-to-a-bottom-level-kg-schema-and-shacl-shapes-graph). <br>✍️ For **example**, if the Machine Learning schema was extended, then the **corresponding file** is `ml_tasks.py`.
    - The **relevant sub-class** depends on the task to which the new method was linked in Step 3.b or Step 5 of [Section A of this guide](#a-adding-semantic-components-to-a-bottom-level-kg-schema-and-shacl-shapes-graph). <br>✍️ For **example**, if the new method is linked to the `ml:BinaryClassification` task which belongs under the `ml:Train` task, then the **relevant sub-class** is `exe_kg_lib.classes.tasks.ml_tasks.Train`.<br>
    [🗒️ **Note**: If ✳️**Case 2 from Step 3** applies, then the **relevant sub-class** refers to a new Python class that needs to be created in a similar way like existing classes in `exe_kg_lib.classes.tasks` package.]
2. Modify the code of `run_method()` in the **relevant sub-class** to call the Python module that implements the new method (see Step 4 in [Section A of this guide](#a-adding-semantic-components-to-a-bottom-level-kg-schema-and-shacl-shapes-graph)).
