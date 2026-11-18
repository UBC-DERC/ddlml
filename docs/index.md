# The DDL Markup Language

DDLML was developed as part of an ongoing project to help improve data governance within the
Dairy Education and Research Center (DERC) at the University of British Columbia. Data collection
at DERC includes information and knowledge from ongoing farm operations, but also from research
projects with specific data needs.

Our goal with this project was to develop a toolkit to support data governance across a wide
range of technical skill levels by providing clear data model documentation using YAML. This toolkit includes
a Python-based package that validates the YAML, ensuring cross-table references are correct, and supports
the use of indexing and constraints.

**The current package only supports Postgres flavor DDL.**

The DDLML specification borrows heavily from the [OpenAPI specification](https://spec.openapis.org/oas/)
for project metadata and file reference structuring.

## Contents

<div class="grid cards" markdown>

-   :material-clipboard-list:{ .lg .middle } __[Package Documentation](api/index.md)__

    ---

    Package documentation for the ddlml Python package..

-   :material-sitemap:{ .lg .middle } __[DDLML Specification](specifications/SPECIFICATION.md)__
  
    ---

    Full specifications for the DDLML YAML format.

-   :material-lightbulb:{ .lg .middle } __[Resources and Concepts](resources.md)__

    ---

    Tools for project management, and database-related concepts to support efficient management.

-   :material-database-check:{ .lg .middle } __[Example Documentation](database/index.md)__

    ---

    Documentation for the sample database, including table overviews, definitions and links.

</div>
