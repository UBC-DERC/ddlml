"""Cross-reference validation for a fully assembled database model.

A constraint separates two clearly-named ideas:

* ``columns`` — the constraint's own/local columns, validated against the table
  that owns the constraint.
* ``references`` — an optional foreign target ``(schema, table, columns)``,
  carried only by REFERENCES constraints, whose ``columns`` are validated
  against the referenced table.

The schema of the *referring* table is implied by its membership in a
``schema_dict``. A foreign target may omit its ``schema``; it will be
filled from the owning schema during :func:`resolve_references`.

Checking runs across *all* references and collects every problem, so a single
run reports the complete list of unresolved references rather than stopping at
the first one.
"""

from .object_classes import ConstraintType, DDL_Dict

CONSTRAINT_KEYS = {
    ConstraintType.primary_key,
    ConstraintType.unique,
    ConstraintType.unique_nulls_not_distinct,
}


class ReferenceCheckError(Exception):
    """Raised when one or more references point at tables/columns that do not exist."""


def resolve_references(db: DDL_Dict) -> DDL_Dict:
    """Fill omitted ``references`` schema/table from the owning table's context.

    A reference with no ``schema`` defaults to the owning table's schema.
    Values that are already set are left as-is, so a name that
    simply does not resolve stays wrong and is caught by
    :func:`find_missing_references` rather than silently rewritten.

    Args:
        db (DDL_Dict): A fully loaded database model (mutated in place).

    Returns:
        DDL_Dict: The same model, for chaining.
    """
    for schema in db.schemas:
        for table in schema.tables:
            for constraint in table.constraints:
                ref = constraint.references
                if ref is None:
                    continue
                if ref.schema_ is None:
                    ref.schema_ = schema.name
    return db


def find_missing_references(db: DDL_Dict) -> list[str]:
    """Collect a message for every unresolved reference in the model.

    Resolves foreign-target defaults first, then checks that each constraint's
    local ``columns`` exist in its owning table and that each foreign target's
    ``(schema, table)`` and ``columns`` exist in the referenced table.

    Args:
        db (DDL_Dict): A fully loaded database model.

    Returns:
        list[str]: One human-readable message per problem. An empty list means
            every reference resolves.
    """
    resolve_references(db)

    # Get all the column names in each table.
    columns_by_table = {
        (schema.name, table.name): {col.name for col in table.columns}
        for schema in db.schemas
        for table in schema.tables
    }

    # Get all the constraints in an unordered set, so we can match from foreign keys.
    keys_by_table = {
        (schema.name, table.name): {
            frozenset(c.columns) for c in table.constraints if c.type in CONSTRAINT_KEYS
        }
        for schema in db.schemas
        for table in schema.tables
    }

    problems: list[str] = []
    for schema in db.schemas:
        for table in schema.tables:
            source = f"{schema.name}.{table.name}"
            owner_columns = columns_by_table[(schema.name, table.name)]
            for constraint in table.constraints:
                for col in constraint.columns:
                    if col not in owner_columns:
                        problems.append(
                            f"{source} constraint '{constraint.name}' uses column "
                            f"'{col}', which does not exist in {source}"
                        )
                ref = constraint.references
                if ref is None:
                    continue
                if ref.schema_ is None or ref.table is None:
                    continue
                target = (ref.schema_, ref.table)
                if target not in columns_by_table:
                    problems.append(
                        f"{source} constraint '{constraint.name}' references "
                        f"missing table '{ref.schema_}.{ref.table}'"
                    )
                    continue
                target_columns = columns_by_table[target]
                missing = [c for c in ref.columns if c not in target_columns]
                for col in missing:
                    problems.append(
                        f"{source} constraint '{constraint.name}' references "
                        f"column '{col}', which does not exist in "
                        f"'{ref.schema_}.{ref.table}'"
                    )
                if not missing and frozenset(ref.columns) not in keys_by_table[target]:
                    problems.append(
                        f"{source} constraint '{constraint.name}' references "
                        f"({', '.join(ref.columns)}) in '{ref.schema_}.{ref.table}', "
                        "which is not its PRIMARY KEY or a UNIQUE constraint"
                    )

    return problems


def check_references(db: DDL_Dict) -> DDL_Dict:
    """Validate every reference in *db*, raising once if any are unresolved.

    All problematic references are gathered and reported together so they can
    be fixed in a single pass.

    Args:
        db (DDL_Dict): A fully loaded database model.

    Returns:
        DDL_Dict: The unchanged model, allowing this to be chained.

    Raises:
        ReferenceCheckError: If one or more references cannot be resolved.
    """
    problems = find_missing_references(db)
    if problems:
        raise ReferenceCheckError(
            "Reference problems have been found:\n  - " + "\n  - ".join(problems)
        )
    return db
