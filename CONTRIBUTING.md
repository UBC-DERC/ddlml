# Contributing to `ddlml`

We want to make contributing to this project as easy and transparent as possible. We also want to support broader community adoption of this tool, and transparent adoption of the data standards.

## Coding Practice

This project uses `uv` as a package manager and to manage virtual environments. To use development tools including `ruff` and `ty`, you first need to install and synchronize the project. First check that you have [`uv` installed](https://docs.astral.sh/uv/getting-started/installation/).

```bash
uv sync
```

We use a `ruff` and `ty` pre-commit hook (see [`.pre-commit-config.yaml`](.pre-commit-config.yaml)) to ensure code quality and standardization. To enable this hook when you are developing code, use the following commands:

```bash
uv run pre-commit install
uv run pre-commit run --all-files   # one-time pass over the existing code
```

The `pre-commit` hook will run both `ruff` and `ty`.

## Pull Requests

We actively welcome your pull requests.

### For new validation or class structures

1. Create a GitHub issue proposing a change to a class definition within the data model (you can stop here if you'd like).
2. Fork the repo and create your branch from `main`.
3. Modify the code as needed and add new tests to ensure your code runs as expected.
4. If you've added an example, it should be validated. You can do this by running:
     `ddlml ./examples/... -o new_test.yaml --docs ./docs`
     (once you've followed the installation guidelines).
5. Verify that there are no issues in your doc build. You can check the preview locally by entering your virtual environment and running `mkdocs serve`.
6. *Make sure that you are testing against an updated data model*
   * Run `pytest` with the `UPDATE_GOLDEN=1` environment variable: `UPDATE_GOLDEN=1 uv run pytest`.
7. If your change alters the document format, it needs a new *specification* version; see [Specification versions](#specification-versions) below.
8. Address any feedback in code review promptly.

## For bug fixes

1. Create a GitHub issue identifying a bug (you can stop here if you'd like).
2. Fork the repo and create your branch from `main`.
3. Install `uv` and run `uv sync`
4. Make your code change and ensure `ruff`, `ty` and `pytest` checks run cleanly.
5. Address any feedback in code review promptly.

## For "Best Practices" Documentation

1. Create a GitHub issue identifying a documentation deficiency (you can stop here if you'd like).
2. Fork the repo and create your branch from `main`.
3. Install `uv` and run `uv sync`
4. Edit documentation in the `docs` and check that it is showing up properly by running `uv run mkdocs serve`.
5. Address any feedback in code review promptly.

## Versioning and Releases

`ddlml` has two version numbers, and they change independently:

| | Example | Where it lives | Changes when |
| --- | --- | --- | --- |
| **Specification version** | `2026.11.12` | `ddlml_version:` in every model file; `SUPPORTED_DDLML_VERSIONS` in `object_classes.py`; the heading in `SPECIFICATION.md` | The document format changes (a field is added, renamed or removed, or a rule changes). |
| **Package version** | `2026.12.0b1` | `version` in `pyproject.toml`; the git tag; PyPI | Any release of the Python package. |

A package release does not need a new specification version, and a specification change is shipped in the next package release.

### Specification versions

Specification versions use the date the format was frozen, as `YYYY.M.D` without zero padding (e.g. `2026.11.12`). To introduce one:

1. Add the new version to `SUPPORTED_DDLML_VERSIONS` in [`object_classes.py`](src/ddlml/object_classes.py). The last entry is the current version. Remove a version only when support for it ends, and record that in the CHANGELOG.
2. Update the `## Version` heading and date in [`SPECIFICATION.md`](docs/specifications/SPECIFICATION.md).
3. Update `ddlml_version:` in every example entry file under `examples/`, then regenerate the outputs and golden files (`UPDATE_GOLDEN=1 uv run pytest`).
4. Describe the change, and how to migrate existing models, in the CHANGELOG.

The tests in `tests/test_versions_work.py` fail if the specification heading or an example file does not match the current version.

### Package versions

Package versions follow [PEP 440](https://peps.python.org/pep-0440/) with a calendar scheme, `YYYY.M.MICRO`, plus an optional pre-release (`a`, `b`, `rc`) and an optional `.devN` suffix. The month is not zero-padded, because PyPI would normalise `2026.01.0` to `2026.1.0`.

| Version | Meaning |
| --- | --- |
| `2026.12.0.dev1`, `2026.12.0b1.dev1` | Development build, published to TestPyPI only |
| `2026.12.0b1` | Beta |
| `2026.12.0rc1` | Release candidate |
| `2026.12.0` | Release |
| `2026.12.1` | Hotfix to the `2026.12` release |

A valid package version matches:

```regex
^\d{4}\.(?:[1-9]|1[0-2])\.(?:0|[1-9]\d*)(?:(?:a|b|rc)(?:0|[1-9]\d*))?(?:\.dev(?:0|[1-9]\d*))?$
```

Git tags are the package version with a `v` prefix (e.g. `v2026.12.0b1`). Configure git-flow to add it:

```bash
git config gitflow.prefix.versiontag v
```

### Branches and merging

We use [git-flow](https://github.com/petervanderdoes/gitflow-avh): `main` holds released code, `develop` holds the next release, and work happens on `feature/…`, `release/…` and `hotfix/…` branches.

- **Feature branches** start from `develop`, and their pull requests target `develop`. These may be squash-merged.
- **Release and hotfix branches** must be merged with merge commits, never squashed. `git flow release finish` and `git flow hotfix finish` do this, and merge the branch into both `main` and `develop`. If a release goes through a GitHub pull request into `main`, use **Create a merge commit**. A squash merge gives `main` commits that `develop` does not have, and the two branches drift apart.

### Making a release

Using the beta as an example:

1. Start the release from `develop`:

    ```bash
    git flow release start 2026.12.0b1
    ```

2. Set `version = "2026.12.0b1"` in `pyproject.toml`, then run `uv lock` so the lockfile matches.
3. In `CHANGELOG.md`, rename the `[Unreleased]` heading to `[2026.12.0b1] - YYYY-MM-DD`, and start a new, empty `[Unreleased]` section above it. Changes are recorded under `[Unreleased]` as they are merged, so the list should already be complete.
4. Check that everything passes: `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, `uv run ty check` and `uv run mkdocs build --strict`.
5. Finish the release. This merges into `main` and `develop` and creates the tag `v2026.12.0b1`:

    ```bash
    git flow release finish 2026.12.0b1
    ```

6. Push both branches and the new tag. Push the tag by name rather than with `--tags`, so no stray local tags are published:

    ```bash
    git push origin main develop v2026.12.0b1
    ```

Hotfixes follow the same steps, starting from `main` with `git flow hotfix start 2026.12.1` and ending with `git flow hotfix finish 2026.12.1`.

## Issues

We use [GitHub issues](https://github.com/UBC-DERC/ddlml) to track public bugs. Please ensure your description is
clear and has sufficient instructions to be able to reproduce the issue.

## License

By contributing to this project's code, documentation and examples you agree that your contributions will be licensed under the [LICENSE file](LICENSE.md) in the root directory of this source tree.
