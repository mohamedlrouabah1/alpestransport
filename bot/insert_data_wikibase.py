"""
Parse le format de données intermédiaire établie dans lequel sont transformer
toutes les données provenant de nos sources.
"""
from wikibaseintegrator.wbi_enums import WikibaseDatatype
from wikibaseintegrator import datatypes


# Better name ??? parse_intermediate_format ?
# the dictionary need to start by an a key "entity" with value 'item'
def insert_data_from_intermediate_format(data, AlpesTransport_wikibase, DEBUGG=False):
    """
    Insert data from the intermediate format into the wikibase.
    Return the id of the entity created or updated. (item or property)
    """
    # we look if it already exists
    id_item = AlpesTransport_wikibase.get_item_id_by_name(data["label"])

    if len(id_item) == 0:
        id_item = AlpesTransport_wikibase.create_item(data["label"]).id
        if DEBUGG:
            print("Item with label ", data["label"], " created with id ", id_item)
    else:
        id_item = id_item[0]
        if DEBUGG:
            print(
                "Item with label ", data["label"], " already exists with id ", id_item
            )

    if DEBUGG:
        i = 0  # to keep track of the number of loop iteration

    # Then we create statements associated with its properties
    for prop in data["property"]:
        # debug message, to remove later
        if DEBUGG:
            print("property ", i, " / ", len(data["property"]))
            i += 1

        # we look if it already exists
        id_prop = AlpesTransport_wikibase.get_property_id_by_name(
            prop["label"], language="fr"
        )

        if len(id_prop) == 0:
            try:
                # we create it
                prop_type = (
                    WikibaseDatatype.ITEM
                    if prop["type"] == "listItem"
                    else WikibaseDatatype.STRING
                )
                id_prop = AlpesTransport_wikibase.create_property(
                    prop["label"], datatype=prop_type
                ).id
                if DEBUGG:
                    print(
                        "Create property id  ",
                        id_prop[0],
                        " for property ",
                        prop["label"],
                    )
            except:
                if DEBUGG:
                    print("Error while creating property ", prop["label"])
                continue
        else:
            id_prop = id_prop[0]
            if DEBUGG:
                print("Get property id  ", id_prop, " for property ", prop["label"])

        # TODO: For cleaning code, if it is a string or an item, i.e contains one property, we need to embedded it into and array to be able to iterate over it and not over its keys
        if prop["type"] == "listItem" or prop["type"] == "item":
            if DEBUGG:
                print("Create statment for item", id_item, " and property ", id_prop)

            statements_values = []
            items = prop["value"] if prop["type"] == "listItem" else [prop["value"]]

            for item in items:
                if DEBUGG:
                    print("Recursive call for item ", item["label"])

                # we create it or edit it and add its statements
                id_item_prop = insert_data_from_intermediate_format(
                    item, AlpesTransport_wikibase
                )

                # we add the statement to the list
                statements_values.append(
                    AlpesTransport_wikibase.get_item_by_id(id_item_prop).id
                    # item["label"], # generate error wikibaseintegrator.wbi_exceptions.ModificationFailed: 'Bad value type string, expected wikibase-entityid'
                )

            # we create statements
            if DEBUGG:
                print(
                    "Create multiple statements for item",
                    id_item,
                    " and property ",
                    id_prop,
                    "values: ",
                    statements_values,
                )

            AlpesTransport_wikibase.create_multiple_statements(
                id_item,
                [id_prop for i in range(len(statements_values))],
                statements_values,
            )

        # elif prop["type"] == "string": # decomment here if you want to add more property type
        else:
            # we create the statement
            if DEBUGG:
                print(
                    "Create statment for item",
                    id_item,
                    " and property ",
                    id_prop,
                    " with value ",
                    prop["value"],
                )
            AlpesTransport_wikibase.create_statement(id_item, id_prop, prop["value"])

    if DEBUGG:
        print("Function insert_data_from_intermediate_format return ", id_item)

    return id_item
