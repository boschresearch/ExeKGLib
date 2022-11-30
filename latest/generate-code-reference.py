# Copyright (c) 2022 Robert Bosch GmbH and its subsidiaries. All rights reserved.

"""Generate code reference using `mkdocs-gen-files` and `mkdocs-literate-nav`.

This script is run when mkdocs builds the documentation, and automatically creates
stubs of all (sub)modules within the project using the project's folder structure.
"""

from pathlib import Path

import mkdocs_gen_files

PACKAGE_IMPORT_NAME = "executable_ml_kgs"

nav = mkdocs_gen_files.Nav()
nav[PACKAGE_IMPORT_NAME] = "index.md"

for path in sorted(Path(PACKAGE_IMPORT_NAME).glob("**/*.py")):
    relative_path = path.relative_to(PACKAGE_IMPORT_NAME)
    module_path = relative_path.with_suffix("")
    doc_path = relative_path.with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = module_path.parts
    if "__init__" in parts:
        continue
    nav[parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as file:
        print("::: " + ".".join([PACKAGE_IMPORT_NAME] + list(parts)), file=file)

    mkdocs_gen_files.set_edit_path(full_doc_path, Path("..") / path)

with mkdocs_gen_files.open("reference/code-nav.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
