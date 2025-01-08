import mongoengine as me


# Initialize the mongo client 
def init_db(app) -> None:
    db_config = app.config["MONGODB_SETTINGS"]
    try:
        me.connect(db_config["db"],
                   host=db_config["host"],
                   port=db_config["port"])
        print("Connected to DB successfully.")
    except Exception as exc:
        print("Error connecting to DB: ", exc)


def set_fields(doc: me.Document, in_fields: dict, exclude_fields: list[str]) -> me.Document:
    """
    doc: Document to set fields
    in_fields: Fields to set in the document
    exclude_fields: Fields to exclude from the document. Excludes id by default.
    """

    # Default exclude id
    if exclude_fields is None:
        exclude_fields = ["id"]
    else:
        exclude_fields.append("id")

    doc_fields = list(set(doc._fields.keys()) - set(exclude_fields))

    # Iterate, raise exception if field not in document
    for field in in_fields:
        if field not in doc_fields:
            raise me.errors.FieldDoesNotExist(f"Field '{field}' is not valid")

        setattr(doc, field, in_fields[field])

    return doc