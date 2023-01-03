"""Generate code reference using `mkdocs-gen-files` and `mkdocs-literate-nav`.

This script is run when mkdocs builds the documentation, and automatically creates
stubs of all (sub)modules within the project using the project's folder structure.
"""

from pathlib import Path

import mkdocs_gen_files

PACKAGE_IMPORT_NAME = "exe_kg_lib"

nav = mkdocs_gen_files.Nav()
nav[PACKAGE_IMPORT_NAME] = "index.md"

excludes = mkdocs_gen_files.config["plugins"]["gen-files"].config["exclude"]

for path in sorted(Path(PACKAGE_IMPORT_NAME).glob("**/*.py")):
    relative_path = path.relative_to(PACKAGE_IMPORT_NAME)
    module_path = relative_path.with_suffix("")
    doc_path = relative_path.with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    if any([exclude in str(full_doc_path) for exclude in excludes]):
        continue

    parts = module_path.parts
    nav[parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as file:
        print("::: " + ".".join([PACKAGE_IMPORT_NAME] + list(parts)), file=file)

    mkdocs_gen_files.set_edit_path(full_doc_path, Path("..") / path)

with mkdocs_gen_files.open("reference/code-nav.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
