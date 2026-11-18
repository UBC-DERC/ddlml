# DDLML Specification

Date: November 16, 2026

This document serves to define the specifications for the DDLML (Data Definition Language Markup Language) format that will be used to generate valid (Postgres) data definition language (DDL) structure through the [`ddlml`](https://github.com/UBC-DERC/ddlml) and the [`ddl_builder`](https://github.com/UBC-DERC/ddl_builder) Python packages. The goal is to develop a human readable document format that can be processed by a Python script and transformed into usable SQL to work within a system in which atomic features of databases are required, but schema or data model specifications may change over time.

This format will attempt to mirror other existing schema, and is strongly influenced by [OpenAPI](https://spec.openapis.org/oas/latest.html).

## Version 2026.11.12

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in [RFC2119](https://www.rfc-editor.org/info/rfc2119/).

### Introduction

This documentation is intended to support a data model that allows users to read, build documentation, and iterate over data models for (Postgres) databases over time as part of a workflow that allows lay partners and technical experts to work together to develop and define appropriate data models for complex systems. The tool was originally developed as part of work at the University of British Columbia's Dairy Education and Research Center, where multiple existing systems, proprietary data models, and a history of academic research resulted in a large number of heterogenous datasets that needed to be aligned to support longitudinal data analysis.

The models and systems established as part of DDLML allow system developers to consult with domain experts, technicians, researchers and other invested groups, without the need for deep understanding of underlying database principles. It allows for integrated development of indices, constraints and references, and can support the implementation of best-practices early on in the database design process.

### Versioning System

Versioning will use a [CalVer](https://calver.org/) system, using a YYYY.M.D.MICRO format without padding. Breaking changes will be documented in the CHANGELOG, and end-of-support will be documented in the specifications and in the README.

## File References (`$ref`)

A `$ref` replaces an entry with the contents of another file or folder, so a
model can be split across files and shared definitions (such as `datecreated`)
written once.

| Field name | Type | Description |
| --- | --- | --- |
| $ref | str | REQUIRED. A path to a YAML file or a folder of YAML files, relative to the file that contains the `$ref`. |

A `$ref` tag is intended to hold only one object, not a list. In the current implementation only the first list element will be retained.

A file referenced by `$ref` cannot itself begin with a `$ref` tag.

### Where `$ref` may be used

The `$ref` tag may be used for entries in `schemas`, `tables` and `columns`. At present a `$ref` can only be used if the parent object (`schema`) also uses a `$ref` object.  In part this is intended to help support the development of smaller, modular `yaml` structures, but may be problematic. Our goal is to address this limitation in the future.

The current implementation assumes that any reference from `tables` must point to a directory (rather than a single file).

### Resolving paths

- The `$ref` is relative to the folder of the file containing the `$ref`, not the entry file or the working directory. Absolute paths are used as-is.
- A folder loads every `*.yml` / `*.yaml` file in it, in alphabetical order.
- A file loads its contents.
- A missing target is an error.

### Keys beside a `$ref`

Keys with a `$ref` will be ignored. This is currently a limitation, for example, with external references, the meaning of a particular column or field will change depending on if it is a PRIMARY KEY or FOREIGN KEY. At present we do not support the differentiation of ontology references outside the `$ref` tag.

### `$ref` Example

Here is an example table with the `$ref` tag. Note that for this to work properly within a full database object the table itself must have been linked through a `$ref` tag.

??? example "DDLML Table Example with $ref tag"
    ```yaml hl_lines="14"
    - name: cows
      type: BASE TABLE
      schema: dairy
      comment: >-
        The primary table for cow-related identification. This table should tie to any information about cows,
        their locations, movement, treatments and, ultimately, datasets produced using the cows as primary data
        elements.
      x-reference:
      - ontology: DCPO
        term: dcpo:bovine
        url: https://agroportal.eu/ontologies/DCPO/Bovine
        relation: broadMatch
      columns:
        - $ref: columns/cadid.yaml
        - name: cowschemeid
          type: text
          comment: >-
            We clearly identify the scheme from which the cow ID is coming from. It is implied
            that this is the Canadian data scheme, but if this data is used in synthesis work
            it is important to identify the source.
    ```

### Differences from OpenAPI

No `#/…` fragments (JSON Pointer) and no URLs; local paths only.

## Objects and Fields

### Fixed Fields

| Field name | Type | Description |
| --- | --- | --- |
| ddlml_version | str | REQUIRED. This string MUST be the CalVer version number of the ddlml specification. This field allows other tooling to understand the structure and specification of the ddlml file. The version number must be one of the supported versions. |
| info | [Info object](#info) | REQUIRED. This object is used to provide additional metadata about the purpose of the ddlml document and data model. |
| database | [Database object](#database) | REQUIRED. The database definition. |

#### Header Example

The `ddlml_version` must be an accepted version of the ddlml specification. This example is the [`simple_example`](https://github.com/UBC-DERC/ddlml/blob/main/examples/simple_example/database.yaml) included with this project.

??? example "DDLML Example"
    ```yaml
    ddlml_version: 2026.11.12
    info:
      title: Simple Example
      summary: A data model for a very simple explanation
      version: "1.0.0"
      license:
        name: CC0-1.0
        url: https://creativecommons.org/publicdomain/zero/1.0/
      contacts:
        - name: Simple Example Team
          email: simple@example.com
    database:
      name: simplemodel
      schemas:
        - name: public
          comment: |
            The public (default) schema.
    ```

### Info

These fields are similar to the fields defined in the [OpenAPI v3.2.1 Specification](https://spec.openapis.org/oas/v3.2.1.html). They are used to support metadata propagation for specific data models, and to identify the rights owner, and data or object discovery.

| Field name | Type | Description |
| --- | --- | --- |
| title | str | REQUIRED. The title of the data model (different from the database name). This is a formal title for the document. |
| summary | str | A short summary of the data model. |
| description | str | A longer description of the data model that can use [CommonMark](https://commonmark.org/) syntax for rich text representation. Defaults to `None`. |
| contacts | [Contact Object](#contacts) | The contact information for the metadata and data model maintainer. |
| license | [License Object](#license) | The license information for the data model and structured repository associated with it. |
| version | str | REQUIRED. The version of the DDLML document (which is distinct from the DDLML Specification version). |

#### Info Example

Here is a simple example of an info block for a project building an open data resource to manage zebrafish genetics data. Note that version number "0.1" is quoted, so that the YAML parser will read it as a string.

??? example "DDLML example"
    ```yaml
    title: zebrafishdb
    summary: A public database for managing information about zebrafish genetics
    contacts:
      - name: Oksana Honchar
        url: https://example.com/oksanahonchar
        email: oksana@example.com
      - name: Chidi Anagonye
        url: https://example.com/chidi
        email: chidi@example.com
    license:
      name: MIT License
      url: https://example.com/LICENSE.md
    version: "0.1"
    ```

### Contacts

Support for contact information. Drawn from the OpenAPI standard [Contact Object](https://swagger.io/specification/v3.2/#contact-object).

| Field name | Type | Description |
| --- | --- | --- |
| name | str | REQUIRED. The identifying name of the contact person/organization. |
| url | str | The URI for the contact information. This MUST be in the form of a URI. |
| email | str | The email address of the contact person/organization. This MUST be in the form of an email address. |

#### Contacts Example

Here is an example of a one person contact object, with no email or url:

??? example "DDLML Example"
    ```yaml
    contacts:
      - name: Oksana Honchar
    ```

Here is an example of a two person contact object, with emails and urls:

??? example "DDLML Example"
    ```yaml
    contacts:
      - name: Oksana Honchar
        url: https://example.com/oksanahonchar
        email: oksana@example.com
      - name: Chidi Anagonye
        url: https://example.com/chidi
        email: chidi@example.com
    ```

### License

A field to support the discovery and application of licensing to any data model created using a DDLML form/format, drawn from the OpenAPI [License Object](https://swagger.io/specification/v3.2/#license-object)

| Field name | Type | Description |
| --- | --- | --- |
| name | str | REQUIRED. The license name used for the data model. |
| identifier | str | An [SPDX-Licenses](https://spdx.org/licenses/) expression. The identifier field is mutually exclusive of the url field. |
| url | str | A URI for the license used for the data model. This MUST be in the form of a URI. The url field is mutually exclusive of the identifier field. |

#### License Examples

Here is an example of a license defined by a license file at a URL the user manages (you could replace the URL with your own License file):

??? example "DDLML Local-ish MIT License Example"
    ```yaml
    license:
      name: MIT License
      url: https://example.com/LICENSE.md
    ```

Here the license is defined by the [SPDX License](https://spdx.org/licenses/) naming convention:

??? example "DDLML SPDX Example"
    ```yaml
    license:
      name: Creative Commons v1.0
      identifier: CC-BY-1.0
    ```

### Database

| Field name | Type | Description |
| --- | --- | --- |
| encoding | str | Character set encoding for the database. One of the valid Postgres [supported character sets](https://www.postgresql.org/docs/current/multibyte.html) |
| locale | str | Currently locale is used to encode for all locales (see options for [locale in Postgres](https://www.postgresql.org/docs/current/locale.html)). |
| name | str | REQUIRED. The name for the database on the server. To be used in `CREATE DATABASE`. |
| owner | str | By default this is empty and the user is assumed to be `postgres`. |
| comment | str | A comment at the database level. |
| extensions | list[str] | A valid set of [Postgres extensions](https://gist.github.com/joelonsql/e5aa27f8cc9bd22b8999b7de8aee9d47) that can be installed from the commandline. |
| schemas | [Schema Objects](#schemas) | An optional field. We can generate a database with no schema. Postgresql will still create a `public` schema. |

#### Database Example

A database object may be very simple. In initial development it may be enough to generate a database with a schema and no tables. Note that this is an example of the `database` object only.

??? example "DDLML Example"
    ```yaml
    database:
      name: dairydb
      schemas:
        - name: dairy
      extensions:
        - postgis
        - pg_stat_monitor
        - pg_trgm
      owner: postgres
      comment: A database for management of dairy data.
      locale: en_CA
      encoding: UTF8
    ```

### Schemas

The schema is a conceptual grouping of tables, either around a particular data source, permission set or conceptual model.

| Field name | Type | Description |
| --- | --- | --- |
| name | str | REQUIRED. A valid schema name. |
| comment | str | A comment to apply to the schema. The default value is "No comment provided." |
| tables | [Table objects](#table) | A valid structured [Table object](#table) |

#### Schema Example

A schema can contain zero or more tables.

??? example "DDLML Example"
    ```yaml
    schemas:
    - name: firstschema
      comment: This is a schema with no tables.
    - name: secondschema
      comment: This schema has a table.
      tables:
      - name: onlytable
        type: BASE TABLE
        comment: The only table in the secondschema schema.
        columns:
        - name: onecolumn
          type: nchar(1)
    ```

### Table

| Field name | Type | Description |
| --- | --- | --- |
| name | str | REQUIRED. The name given to the table. It MUST conform to existing naming conventions for the database target (currently only Postgres). |
| schema | str | The schema within which the table exists. This may be inherited, or explicitly defined. |
| type | str | The type of table (allowing extension to BASE TABLE, VIEW and other types of table structures within Postgres). |
| comment | str | A string comment to describe the table. Used as part of the `COMMENT` clause in SQL. Default is "No comment provided". |
| columns | [Column Object](#column) | Zero or more Column objects, in a list. |
| constraints | [Constraint Object](#constraint) | Zero or more constraint objects in a list. |
| indexes | [Index Object](#indexes) | Zero or more Index objects in a list |

#### Table Example

Here we define a table with two columns, `cadid` and `cowschemeid`. The `cadid` column is a `$ref` reference, which means the full definition is in the file `columns/cadid.yaml`, where the path is relative to the calling file (not the root of the DDLML definition).

??? example "DDLML Table Example with $ref tag"
    ```yaml hl_lines="14"
    - name: cows
      type: BASE TABLE
      schema: dairy
      comment: >-
        The primary table for cow-related identification. This table should tie to any information about cows,
        their locations, movement, treatments and, ultimately, datasets produced using the cows as primary data
        elements.
      x-reference:
      - ontology: DCPO
        term: dcpo:bovine
        url: https://agroportal.eu/ontologies/DCPO/Bovine
        relation: broadMatch
      columns:
        - $ref: columns/cadid.yaml
        - name: cowschemeid
          type: text
          comment: >-
            We clearly identify the scheme from which the cow ID is coming from. It is implied
            that this is the Canadian data scheme, but if this data is used in synthesis work
            it is important to identify the source.
    ```

### Column

| Field name | Type | Description |
| --- | --- | --- |
| name | str | REQUIRED. The formal column name. Should conform to Postgres standard. |
| type | str | REQUIRED. Column type. MUST conform to an allowed [Postgres data type](https://www.postgresql.org/docs/current/datatype.html) or a type supported by an existing Postgres extension. Validation occurs during conversion to DDL in the `ddl_builder` Python package. |
| comment | str | As opposed to the [Table Object](#table) comments, the column comments default to "No comment provided." |
| nullable | bool | Is the field nullable? Defaults to `True` |
| default | str | Defines a default value, the field is submitted as a string, but will be transformed based on the `type` defined above. |

#### Column Example

Here we show the example file for `cadid.yaml` referenced above in the [table example](#table-example):

??? example "DDLML Column Example"
    ```yaml
    - name: cadid
      type: text
      comment: This is the unique identifier given to the cow by the Canadian Government that conforms to ISO 11784
    ```

We can look at a more complete example of a column definition, for `datecreated`, which can be used across multiple tables, and has references to PROV-O and `schema` standards:

??? example "DDLML datecreated Example"
    ```yaml
    - name: datecreated
      comment: >-
        The date this entry was created. This field is used for the purposes of tracking changes across the database, and supporting
        reproducibility of data and data models, by allowing users to "roll back" or search for the impacts of new changes or data additions.
      type: timestamptz
      default: current_timestamp
      nullable: false
      x-reference:
      - ontology: PROV
        term: PROV:generatedAtTime
        url: http://www.w3.org/ns/prov#generatedAtTime
        relation: exactMatch
      - ontology: schema
        term: schema:dateCreated
        url: https://schema.org/dateCreated
        relation: exactMatch
    ```

### Indexes

| Field name | Type | Description |
| --- | --- | --- |
| name | str | REQUIRED. Valid name for the index. |
| type | str | A valid [Postgres index type](https://www.postgresql.org/docs/current/indexes-types.html) or an index supported by a listed extension. |
| comment | str | Valid comment explaining the use of the index. Defaults to "No comment provided." |
| ddl | str | The DDL for defining the index. Optional, for information only. An earlier version of the DDL Builder used this to build the index literally. In the case of conflict between DDL and the structured data, the structured data will be used. |
| columns | list[str] | A list of column names to which the index is applied. |

#### Index Example

We can place any number of indices on a column, or set of columns. Here we create a table with a hash index on `buildingid`, a value we expect to repeat frequently:

??? example "DDLML HASH Index Example"
    ```yaml hl_lines="16-22"
    - name: instrumentinstance
      comment: A particular instrument, with a particular location.
      type: BASE TABLE
      columns:
        - $ref: columns/instrumentinstanceid.yaml
        - $ref: columns/instrumentid.yaml
        - $ref: columns/buildingid.yaml
        - name: location
          type: geography
          comment: The geographical location of the instrument, represented as a point.
        - name: locationdescription
          type: text
          comment: A description of the instrument placement.
        - $ref: columns/datecreated.yaml
        - $ref: columns/datemodified.yaml
      indexes:
      - name: instrumentsinbuilding_idx
        type: hash
        comment: Using a hash index to speed up instrument searches by building.
        ddl: "CREATE INDEX instrumentsinbuilding_idx ON instrumentinstance USING HASH(buildingid);"
        columns:
        - buildingid
      constraints:
      - name: instrumentinstanceid_pk
        type: PRIMARY KEY
        ddl: PRIMARY KEY (instrumentinstanceid)
        columns:
        - instrumentinstanceid
      - name: instrumentinbuilding_fk
        type: FOREIGN KEY
        columns:
        - buildingid
        comment: A foreign key to point to the building id.
        ddl: FOREIGN KEY (buildingid) REFERENCES buildings(buildingid) ON UPDATE CASCADE ON DELETE CASCADE
        references:
          table: buildings
          columns:
          - buildingid
          on_update: CASCADE
          on_delete: CASCADE
      - name: instrumentid_fk
        type: FOREIGN KEY
        columns:
        - instrumentid
        comment: A foreign key to point to the instrument id.
        ddl: FOREIGN KEY (instrumentid) REFERENCES instruments(instrumentid) ON UPDATE CASCADE ON DELETE CASCADE
        references:
          table: instruments
          columns:
          - instrumentid
          on_update: CASCADE
          on_delete: CASCADE
    ```

We could add a spatial index on the `location` column in the previous example using a GIST index, supported by [PostGIS](https://postgis.net/workshops/postgis-intro/indexing.html):

??? example "DDLML GIST Index Example"
    ```yaml
    indexes:
    - name: instrumentlocation_idx
      type: GIST
      comment: Spatial index on the instrument location.
      ddl: CREATE INDEX instrumentlocation_idx ON instrumentinstance USING GIST(location)
      columns:
      - location
    ```

### Constraint

| Field name | Type | Description |
| --- | --- | --- |
| name | str | REQUIRED. A valid name for the constraint |
| type | ConstraintType | REQUIRED. One of the set of constraint types. One of: "CHECK", "UNIQUE", "UNIQUE NULLS NOT DISTINCT", "PRIMARY KEY", "FOREIGN KEY", "EXCLUDE" |
| comment | str | An explanation for the constraint. Defaults to "No comment provided." |
| ddl | str | This will be phased out, but in early development we were including an explicit call to the DDL. In the case of conflict between DDL and the structured [reference_dict](#reference), the reference will be used (not the DDL). |
| columns | list[str] | REQUIRED. A list of columns (1 - n) within the table that the constraint is referencing. |
| references | [reference_dict](#reference) | A reference to another table (only valid when the constraint is a `FOREIGN KEY`) and columns that are referenced by the constraint. Defaults to `None`. The number of columns in the reference list must match the number of columns in the `columns` entry. |

#### Constraint Example

We may want to use an internal foreign key within our table, in this case we define a `FOREIGN KEY`, assign it to a column, and ensure our `references` point to the same table:

??? example "DDLML FOREIGN KEY Constraint Example"
    ```yaml
    constraints:
    - name: damidvalid
      comment: A constraint to ensure that the dam ID is a valid ID based on the Canadian government ID scheme.
      type: FOREIGN KEY
      columns:
      - damid
      references:
        table: cows
        columns:
        - cadid
        on_update: CASCADE
        on_delete: CASCADE
    ```

We can apply a CHECK constraint (for example, where we expect a certain string format). In this case, there is no need for a `references` block, because we are applying the CHECK directly to the specified column.

??? example "DDLML CHECK Constraint Example"
    ```yaml
    constraints:
    - name: isocadid
      comment: >-
        The cadid must follow the ISO 11784 standard, with '124' leading for Canada and the trailing numbers
        ranging from 000000001 to 299999999.
      type: CHECK
      ddl: CHECK (cadid ~* '^124000[0-2][0-9]{8}$')
      columns:
      - cadid
    ```

### Reference

| Field name | Type | Description |
| --- | --- | --- |
| schema | str | Name of a valid schema within the database. Defaults to the parent schema. |
| table | str | REQUIRED. Name of a valid table within the database. |
| columns | list[str] | REQUIRED. One or more columns within the table being referenced. |
| on_update | OnChangeType | Action `ON UPDATE` (default is empty, interpreted by Postgres as `NO ACTION`). An enum representing the valid `ON UPDATE` actions [within Postgres](https://www.postgresql.org/docs/current/ddl-constraints.html). One of: "NO ACTION", "RESTRICT", "CASCADE", "SET NULL", "SET DEFAULT" |
| on_delete | OnChangeType | Action `ON DELETE` (default is empty, interpreted by Postgres as `NO ACTION`). One of: "NO ACTION", "RESTRICT", "CASCADE", "SET NULL", "SET DEFAULT" |

#### Reference Example

For a table with an internal foreign key constraint we may want to reference our own table in the reference block for the constraint:

??? example "DDLML Example"
    ```yaml hl_lines="6-11"
    - name: damidvalid
      comment: A constraint to ensure that the dam ID is a valid ID based on the Canadian government ID scheme.
      type: FOREIGN KEY
      columns:
      - damid
      references:
        table: cows
        columns:
        - cadid
        on_update: CASCADE
        on_delete: CASCADE
    ```

## Specification Extensions

In the case where additional metadata helps explain an object, or works to enrich the object for future work, then the `^x-` extensions are intended to support this information collection and management within the DDLML specification.

| Field Pattern | Type | Description |
| ------------- | ---- | ----------- |
| `^x-` | Any | An extension for [Tables](#table), [Columns](#column) and [Schema](#schemas) only. These extensions may include additional objects named with the `x-` preface. For example `x-references`. These objects are exported to the final object, but are generally used to support metadata for the objects, and are not explicitly used for data management or DDL construction. |

There is currently no mechanism to validate these extensions, but they are passed through to the validated output.

### Extension Examples

One of the first uses we've found for the extensions is linking to external ontologies. For example, using
the extension to link to a [schema.org/identifier](https://schema.org/identifier) definition:

??? example "DDLML Example"
    ```yaml
    x-reference:
      - ontology: schema.org
        term: schema:identifier
        relation: broadMatch
        url: https://schema.org/identifier
    ```
