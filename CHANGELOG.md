# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Calendar Versioning](https://calver.org/) following [PEP 440](https://peps.python.org/pep-0440/) (all version numbers should resolve using `^\d{4}\.(?:[1-9]|1[0-2])\.(?:0|[1-9]\d*)(?:(?:a|b|rc)(?:0|[1-9]\d*))?(?:\.dev(?:0|[1-9]\d*))?$`).

This supports the following PEP440 styles:

* 2026.12.1
* 2027.1.0.dev3
* 2028.1.0a1

NOTE: Some earlier versions of this software (in the changelogs and git-tags) may show non compliant CALVER versioning. We maintain them for transparency.

## [Unreleased]

Planned as `2026.12.0b1`, the first beta on PyPI. Specification version `2026.11.12`.

### Migrating from `2026-11-alpha`

Existing models need three changes before they validate:

1. Rename the top-level key `ddaml_version` to `ddlml_version`.
2. Set it to `2026.11.12`, the only supported specification version.
3. In `info.license`, rename `full_name` to `name` and `licenseId` to `identifier`.
   Give either `identifier` or `url`, not both.

Code that imports the package changes from `data_model` to `ddlml` (for example
`from ddlml.object_classes import DDL_Dict`), and the command changes from `data-model`
to `ddlml`.

### Added

- **Specification version check.** `SUPPORTED_DDLML_VERSIONS` lists the specification
  versions this release accepts (currently only `2026.11.12`), and
  `CURRENT_DDLML_VERSION` is the newest. A document with any other `ddlml_version` is
  rejected with a message listing the supported versions. The JSON Schema lists them as
  an `enum`, so editors flag an unsupported version.
- `info.description`: an optional longer description of the model, which may use
  CommonMark.
- A clear error for documents that still use the old `ddaml_version` key.
- The CLI reports a missing entry file or invalid YAML on stderr with exit code 1, instead
  of a traceback.
- **Specification:** an example for every object (in collapsible blocks), a section on
  `x-` extensions, and a "File References (`$ref`)" section describing how references
  resolve and the current limits.
- `CONTRIBUTING.md`: how specification and package versions differ, the steps for a new
  specification version, the PEP 440 version scheme, git-flow branch and merge rules, and
  the release steps.
- Tests:
  - every example entry file and the specification heading use the current
    specification version;
  - unsupported versions and the old `ddaml_version` key are rejected;
  - `x-` keys pass through the CLI to the output;
  - the `simple_example` quick start builds;
  - a missing entry file and invalid YAML exit cleanly.

### Changed

- **Breaking: renamed from `data_model` / DDAML to `ddlml`.** "DDAML" is already the name
  of another markup language. This covers:
  - the package on PyPI (`data-model` → `ddlml`) and the import (`data_model` → `ddlml`);
  - the command (`data-model` → `ddlml`);
  - the document key (`ddaml_version` → `ddlml_version`);
  - the models (`ddaml_dict` → `ddlml_dict`, `ddaml_info` → `ddlml_info`);
  - the repository, documentation site and JSON Schema URL, now
    `https://github.com/UBC-DERC/ddlml` and `https://ubc-derc.github.io/ddlml/schema.json`.
- **Breaking:** the license fields now follow the OpenAPI License Object: `full_name` →
  `name`, `licenseId` → `identifier`. `identifier` and `url` are mutually exclusive, and one
  of them is required. The default license is `name: Default Copyright Applies`,
  `identifier: LicenseRef-Proprietary`.
- **Breaking:** `ddlml_version` must be a supported specification version (see Added).
  Before, any string was accepted.
- A contact may now omit `email`; before, a contact with no email failed validation.
- The CHANGELOG and git tags use [PEP 440](https://peps.python.org/pep-0440/) CalVer
  (e.g. `2026.12.0b1`, tagged `v2026.12.0b1`) instead of names like `2026-11-alpha`.
- `Dockerfile`: runs `ddlml` directly and passes arguments through
  (`docker run … ddlml <entry> --docs … --output …`), defaulting to `--help`. Before, it
  always printed help. It now uses a pinned `uv` (0.13.8) and installs without
  development dependencies.
- The specification: fixed the version heading and date, the extensions table, typos and
  links, and aligned the License, Contact and Info tables with the code.
- Example models, example outputs, the golden file and the generated docs regenerated for
  the new names, license fields and specification version.

### Removed

- Compiled `.pyc` files that had been committed.

### Dependencies

- Updated `pydantic` to 2.14.3 and `markdown` to 3.11.3, plus other lock-file updates.
- Updated GitHub Actions (`setup-uv` 10.3.3, `codeql-action` 4.39.3) via Dependabot.

### Contributors

- Simon Goring

## [2026-11-alpha]

### Added

- **DDAML specification** (`docs/specifications/SPECIFICATION.md`, v2026.10.26) defining the
  document structure, now linked from the docs navigation.
- **`ddaml_dict` root model** wrapping the database definition with document metadata:
  - `ddaml_version` (required): the CalVer version of the DDAML specification.
  - `info` block (`ddaml_info`) with `title`, `version`, `summary`, `license` and `contacts`.
  - `license_dict` (`full_name` plus `licenseId` and/or `url`) and `contact_dict`
    (`name`, `email`, `url`), with URL and email validation via the `validators` package.
- **`x-` extension keys** allowed on schemas, tables and columns (`extensible_dict`); any
  other unknown key is rejected.
- `on_update` / `on_delete` actions on foreign-key `references` blocks, using a single
  `OnChangeType` enum (`NO ACTION`, `RESTRICT`, `CASCADE`, `SET NULL`, `SET DEFAULT`).
- `EXCLUDE` constraint type.
- New constraint validators: every constraint must list columns; a `references` block must
  name a table and at least one column; foreign keys must reference the same number of
  columns they define.
- `data_model.json_schema` module (`build_schema()`, `write_schema()`); the schema now
  declares `$schema` (JSON Schema 2020-12) and `$id`.
- `.pre-commit-config.yaml` (ruff check/format and `ty`), with `pre-commit` added as a dev
  dependency.
- Tests for the `info` block, `x-` extensions, cross-references and the new validators.

### Changed

- **Breaking:** entry files must now contain a top-level `database:` block alongside
  `ddaml_version` and `info`; `load_database()` returns a `ddaml_dict` and raises
  `ModelValidationError` when the `database:` block is missing.
- **Breaking:** foreign-key `references` must name the target `table` explicitly. An omitted
  table no longer defaults to a self-reference (an omitted `schema` still defaults to the
  owning schema).
- Constraint `type` is now required (it can no longer be `None`).
- Reference actions are no longer written out as an explicit `NO ACTION` by default; when
  omitted, PostgreSQL's implicit `NO ACTION` applies.
- Index `ddl` is now optional.
- The CLI reports Pydantic `ValidationError`s to stderr with a non-zero exit code.
- **JSON Schema generation moved into the docs build**: a MkDocs hook
  (`hooks/json_schema.py`) generates `schema.json` from `ddaml_dict` (instead of `DDL_Dict`)
  on every `mkdocs build`/`serve`, so it is published on each push to `main` and resolves
  in local strict builds. The separate CI generation steps were removed and the download
  link restored.
- Package version set to `2026.10.0a1` (CalVer).
- Examples, the golden output and generated docs updated for the new structure.
- Docstrings cleaned up and code reformatted with `ruff format`; README and CONTRIBUTING
  updated (including the pre-commit workflow).

### Removed

- The unused `tests/samples/examples/` fixtures.
- The "All references resolve!" message printed by `check_references()`.
- `examples/**/output.yaml` is now git-ignored.

### Dependencies

- Updated `pydantic` to 2.14.1, `py-markdown-table` to 2.0.0 (major), `markdown` to 3.11.2,
  `ruff` to 0.17.2 and `ty` to 0.0.92, plus other lock-file updates.
- Added `validators` 0.36.0 (runtime) and `pre-commit` 4.7.0 (dev).
- Updated GitHub Actions (`setup-uv` 10.3.2, `upload-pages-artifact`, `codeql-action`
  4.39.1) via Dependabot.

### Contributors

- Simon Goring


## [2026-09-alpha]

### Added

- **JSON Schema publication**: Auto-generated from Pydantic models and published to docs site
  at `https://ubc-derc.github.io/ddlml/schema.json`.
- **Schema documentation page** (`docs/api/schema.md`) with VS Code integration guide for
  editor autocompletion and validation.
- **Pre-commit hook** for `ruff` and `ty` checks on `develop` and `main` branches (gitflow).
- **`ty` type checking** integrated into CI workflow.
- **Dependabot auto-merge workflow** for minor/patch updates with squash merge.
- **Dependabot grouping** for GitHub Actions updates (reduces PR noise).
- `resolve_ref()` utility function to handle `$ref` resolution with sibling key merging.

### Changed

- **Migrated from `ref:` to `$ref:`** for OpenAPI/JSON Schema consistency:
  - Updated `load_database.py`, `load_schema.py`, `load_tables.py` to use `$ref` key.
  - Migrated 90+ YAML files in `examples/` and `tests/samples/`.
  - Updated test fixtures in `test_cli.py` and `test_load_files.py`.
- Redesigned the reference model to align with updated design specifications.
- Updated constraints to use `ConstraintType.FOREIGN_KEY` with `references` block
  (replacing old `REFERENCES` string).
- Improved error messaging for invalid table definitions.
- Generated files (`docs/database/`, `docs/schema.json`) now excluded from version control.
- Refactored test suites for improved coverage of file loading and constraint handling.

### Fixed
- All 62 tests now passing (97.5% coverage) — resolved 6 failures related to `ref`/`$ref`
  migration and constraint type mismatches.

### Dependencies
- Updated `pydantic` to 2.13.5 via Dependabot.
- Updated `ruff` to 0.16.6 via Dependabot.
- Updated `ty` to 0.0.78 via Dependabot.
- Updated `uv-build`, `mkdocs-material`, and GitHub Actions (`deploy-pages`, `setup-uv`,
  `codeql-action`) via Dependabot.

### Contributors
- Simon Goring


## [2026-07-alpha]
### Added
- CLI creates a single YAML from a set of YAML files.
- Documentation with mkdocs.
- YAML schema validation using Pydantic-based classes for key structural elements.
- Test suite.

### Contributors to this Release
* Simon Goring
