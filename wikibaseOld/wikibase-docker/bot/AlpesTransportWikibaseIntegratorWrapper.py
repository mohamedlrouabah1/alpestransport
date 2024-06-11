"""
This module is a wrapper for the WikibaseIntegrator library.
It is used to create items and properties in Wikibase in a higher level way, by
making abstraction of the WikibaseIntegrator library.
"""

from wikibaseintegrator import wbi_login, WikibaseIntegrator, entities, wbi_config
from wikibaseintegrator.entities.item import ItemEntity
from wikibaseintegrator.models.labels import Labels as newLabel
from wikibaseintegrator.models.descriptions import Descriptions as newDescription

# Global Configuration of the url of the wikibase :
from wikibaseintegrator.wbi_config import config as wbi_config
wbi_config['MEDIAWIKI_API_URL'] = "http://localhost:8383/api.php"
wbi_config['SPARQL_ENDPOINT_URL'] = 'http://localhost:8282/proxy/wdqs/bigdata/namespace/wdq/sparql'
wbi_config['WIKIBASE_URL'] = 'http://wikibase.svc'

class  AlpesTransportWiki:

    default_language = "fr"

    def __init__(self, wikibase_url, wikibase_user, wikibase_password):
        """
        Create a bot connected instance of the WikibaseIntegrator library.
        """

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
        self.wikibase_connection = WikibaseIntegrator(login=self.wikibase_login, is_bot=True)


    # TODO: merge these function with a bool param to avoid code redundancy.

    def create_item(self, item_label, item_description=None, language=default_language):
        """
        Create an item in the wikibase.
        """
        if language is None:
            language = self.default_language

        label = newLabel()
        label.set(language=language, value=item_label)

        # TODO: add description

        item = entities.item.ItemEntity(labels=label)
        item.write(login=self.wikibase_login, is_bot=True)
        return item

    def create_property(self, property_label, property_description=None, datatype="String", language=None):
        """
        Create a property in the wikibase.
        """
        if language is None:
            language = self.default_language

        label = newLabel()
        label.set(language=language, value=property_label)

        # TODO: add description

        property = entities.property.PropertyEntity(labels=label, datatype="string")
        property.write(login=self.wikibase_login, is_bot=True)
        return property