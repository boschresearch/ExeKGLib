## Documentation of `exe_kg_lib.classes.tasks` package

[//]: # (--8<-- [start:content])
### Overview

This package contains classes that correspond to entities of type `owl:class` that are `rdfs:subClassOf AtomicTask` in
the KG.

They implement the abstract `run_method()` like so:

1. The input is taken either from outputs of previously executed Tasks (parameter: `other_task_output_dict`) or a
   dataframe (parameter: `input_data`).
2. An algorithm is executed using the input.

   There are two conventions:
    - The algorithm is related to ML, Statistics or Visualization, depending on
      the Python file's prefix.
    - The algorithm's implementation is placed in `utils.task_utils` package in the Python file with the corresponding prefix.
3. The output is returned as a dictionary with pairs of output name and value.

### Naming conventions

- Each class name is a concatenation of 2 strings:
    1. The name of an `owl:class` that is `rdfs:subClassOf AtomicTask`.
    2. The name of an `owl:class` that is `rdfs:subClassOf AtomicMethod` and is associated with the above `owl:class` via a property that is `rdfs:subPropertyOf hasMethod`.

    For example, the below KG property associates `CanvasMethod` with `CanvasTask`. So, the corresponding class name will be `CanvasTaskCanvasMethod`.
    ```turtle
    visu:hasCanvasMethod
        a                  owl:ObjectProperty ;
        rdfs:domain        visu:CanvasTask ;
        rdfs:range         visu:CanvasMethod ;
        rdfs:subPropertyOf ds:hasMethod .
    ```

- The class fields that contain `_` are the snake-case conversions of the equivalent camel-case property names in the
  KG.

  e.g. `has_split_ratio` field corresponds to `hasSplitRatio` property in the KG.

The above conventions are necessary for automatically mapping KG tasks with methods and properties to Python objects while parsing the KG.

[//]: # (--8<-- [end:content])
