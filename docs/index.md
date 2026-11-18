# The DDL Markdown Language

DDLML was developed as part of an ongoing project to help improve data governance within the
Dairy Education and Research Center (DERC) at the University of British Columbia. Data collection
at DERC includes information and knowledge from ongoing farm operations, but also from research
projects with specific data needs.

Our goal with this project was to develop a toolkit to supports data governance across a wide
range of techincal skill levels by providing clear data model documentation using YAML. This toolkit includes
a Python-based package that validates the YAML, ensuring cross-table references are correct, and supports
the use of indexing and constraints.

**The current package only supports Postgres flavor DDL.**

The DDLML specification borrows heavily from the [OpenAPI specification](https://spec.openapis.org/oas/)
for project metadata and file reference structuring.

## Contents

<div class="grid cards" markdown>

-   :material-clipboard-list:{ .lg .middle } __[Package Documentation](api/index.md)__

    ---

    Project overview, outcomes and success metrics.

-   :material-sitemap:{ .lg .middle } __[DDLML Specification](specifications/SPECIFICATION.md)__
  
    ---

    How this project is governed and managed from a personel perspective.

-   :material-lightbulb:{ .lg .middle } __[Resources and Concepts](resources.md)__

    ---

    Tools for project management, and database-related concepts to support efficient management.

-   :material-database-check:{ .lg .middle } __[Example Documentation](database/index.md)__

    ---

    Documentation for the sample database, including table overviews, definitions and links.

</div>


## Project layout

```bash
    main.py    # The main production script to turn the 
               # various YAML files into code.
    src/
        ddlml/  # The folder for the `ddlml` python package.
    docs/            # Documentation pages.
    assets/          # Images and supporting data for documentation and testing.
    tests/           # PyTest testing modules
    data_definition/ # Folder with composite YAML files for database definitions.
    validation.yaml  # Supporting file to define valid fields for db elements.
    pyproject.toml   # Package infrastructure.
    mkdocs.yaml      # Documentation metadata.
```
