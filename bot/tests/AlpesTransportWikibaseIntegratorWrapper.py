"""
This module is a wrapper for the WikibaseIntegrator library.
It is used to create items and properties in Wikibase in a higher level way, by
making abstraction of the WikibaseIntegrator library.
"""
from wikibaseintegrator import wbi_login, WikibaseIntegrator, entities, wbi_config
from wikibaseintegrator.entities.item import ItemEntity
from wikibaseintegrator.models.labels import Labels as newLabel
from wikibaseintegrator.models.descriptions import Descriptions as newDescription
from wikibaseintegrator.wbi_helpers import search_entities
from wikibaseintegrator import models
from wikibaseintegrator.wbi_enums import WikibaseDatatype
import wikibaseintegrator

# Global Configuration of the url of the wikibase :
from wikibaseintegrator.wbi_config import config as wbi_config


class AlpesTransportWiki:
    default_language = "fr"

    def __init__(self, wikibase_url, wikibase_user, wikibase_password):
        """
        Create a bot connected instance of the WikibaseIntegrator library.
        """
        # set the global setting as th url used
        wbi_config["MEDIAWIKI_API_URL"] = wikibase_url
        # wbi_config["SPARQL_ENDPOINT_URL"] = "http://localhost:8834/proxy/wdqs/bigdata/namespace/wdq/sparql"
        # wbi_config["WIKIBASE_URL"] = "http://wikibase.svc"

        # Login to the wikibase
        self.wikibase_url = wikibase_url
        self.wikibase_user = wikibase_user
        self.wikibase_password = wikibase_password
        self.wikibase_login = wbi_login.Login(
            user=self.wikibase_user,
            password=self.wikibase_password,
            mediawiki_api_url=self.wikibase_url,
        )
        # Create a connection
        self.wikibase_connection = WikibaseIntegrator(
            login=self.wikibase_login, is_bot=True
        )

    def create_item(self, item_label, item_description=None, language=default_language):
        """
        Create an item in the wikibase.
        """
        if language is None:
            language = self.default_language

        label = newLabel()
        label.set(language=language, value=item_label)

        # TODO: add description

        item = entities.item.ItemEntity(
            labels=label
        )  # , id="Q59" here set an existing id to update the item
        item.write(login=self.wikibase_login, is_bot=True)
        return item

    def create_property(
        self,
        property_label,
        property_description=None,
        datatype=WikibaseDatatype.STRING,
        language=None,
    ):
        """
        Create a property in the wikibase.
        """
        if language is None:
            language = self.default_language

        label = newLabel()
        label.set(language=language, value=property_label)

        # TODO: add description

        # doesn't work well when is different than string, thus we use a string of the item id for the items
        property = entities.property.PropertyEntity(
            labels=label, datatype=datatype  # WikibaseDatatype.STRING
        )
        property.write(login=self.wikibase_login, is_bot=True)
        return property

    def create_statement(self, item_id, property_id, statement_value, language=None):
        """
        Create a statement in the wikibase.
        """
        if language is None:
            language = self.default_language

        # création du statement
        statement = wikibaseintegrator.datatypes.ExternalID(
            value=statement_value, prop_nr=property_id
        )
        data = [statement]

        # récupération de l'item
        item = self.wikibase_connection.item.get(entity_id=item_id)
        print("Get item result: ", item)

        item.claims.add(data)
        item.write(login=self.wikibase_login, is_bot=True)

    def create_multiple_statements(
        self, item_id, property_id_list, statement_values_list, language=None
    ):
        """
        Create multiple statements in the wikibase for the given item.
        """
        if language is None:
            language = self.default_language

        # création des statements
        data = []
        for property_id, statement_value in zip(
            property_id_list, statement_values_list
        ):
            statement = wikibaseintegrator.datatypes.ExternalID(
                value=statement_value, prop_nr=property_id
            )
            data += [statement]

        # récupération de l'item
        item = self.wikibase_connection.item.get(entity_id=item_id)
        print("Get item result: ", item)
        # attachement des statements créés à  l'item
        item.claims.add(data)
        # enregistrement des modifications dans la wikibase
        item.write(login=self.wikibase_login, is_bot=True)

    def get_item_by_id(self, item_id):
        """
        Get an item by its id.
        """
        return self.wikibase_connection.item.get(entity_id=item_id)

    def __get_entity_id_by_name(self, entity_label, entity_type, language=None):
        """
        Get an entity by its label.
        """
        if language is None:
            language = self.default_language

        print("searching for entity: ", entity_label, " of type: ", entity_type)
        entity = search_entities(
            search_string=entity_label,
            language=language,
            search_type=entity_type,  # also lexeme, property, sense, mediainfo
            dict_result=False,  # return a dict instead of a list
            allow_anonymous=True,
            is_bot=True,
        )

        return entity

    def get_property_id_by_name(self, property_label, language=None):
        """
        Get a property by its label.
        """
        return self.__get_entity_id_by_name(property_label, "property", language)

    def get_item_id_by_name(self, item_label, language=None):
        """
        Get an item by its label.
        """
        return self.__get_entity_id_by_name(item_label, "item", language)

    def is_property_exists(self, property_label, language=None):
        """
        Check if a property exists.
        """
        return len(self.get_property_id_by_name(property_label, language)) > 0

    def is_item_exists(self, item_label, language=None):
        """
        Check if an item exists.
        """
        return len(self.get_item_id_by_name(item_label, language)) > 0

    def create_property_if_not_exist(
        self,
        property_label,
        property_description=None,
        datatype=WikibaseDatatype.STRING,
        language=None,
    ):
        """
        First test if the property already exist, if not create it.
        """
        if self.is_property_exists(property_label, language):
            return self.get_property_id_by_name(property_label, language)

        print("Creating property: ", property_label)
        id = self.create_property(
            property_label, property_description, datatype, language
        )
        return id
