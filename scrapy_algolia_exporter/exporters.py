"""This module contains the ``AlgoliaItemExporter``"""

from algoliasearch import algoliasearch


class AlgoliaItemExporter:
    """Export the scraped items to the Algolia API"""

    algolia_index = None
    next_items = None
    exported_items_nbr = None

    def __init__(self,
                 algolia_api_id,
                 algolia_api_key,
                 algolia_index_name,
                 algolia_item_bulk_nbr=100):

        self.algolia_api_id = algolia_api_id
        self.algolia_api_key = algolia_api_key
        self.algolia_index_name = algolia_index_name
        self.algolia_item_bulk_nbr = algolia_item_bulk_nbr

    def start_exporting(self):
        """Initialize the Algolia API Client"""

        client = algoliasearch.Client(
            self.algolia_api_id,
            self.algolia_api_key
        )
        self.algolia_index = client.init_index(self.algolia_index_name)

        self.next_items = []
        self.exported_items_nbr = 0

    def _export_items(self, items):
        """Export the given items to the current Algolia index"""

        self.algolia_index.add_objects(items)
        self.next_items = []

    def finish_exporting(self):
        """Export the last items from the queue, if any"""

        if self.next_items:
            self._export_items(self.next_items)

    def export_item(self, item):
        """Add the given item to the queue, if the queue if full, upload the items"""

        self.next_items.append(item)

        if len(self.next_items) == self.algolia_item_bulk_nbr:
            self._export_items(self.next_items)




