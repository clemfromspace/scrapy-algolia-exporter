"""This module contains the ``AlgoliaItemPipeline``"""

from scrapy.exceptions import NotConfigured

from .exporters import AlgoliaItemExporter


class AlgoliaItemPipeline:
    """Export the scraped items to the Algolia API"""

    exporter = None

    def __init__(self,
                 algolia_api_id,
                 algolia_api_key,
                 algolia_index_name,
                 algolia_item_bulk_nbr):
        """Store the Algolia settings"""

        self.algolia_api_id = algolia_api_id
        self.algolia_api_key = algolia_api_key
        self.algolia_index_name = algolia_index_name
        self.algolia_item_bulk_nbr = algolia_item_bulk_nbr

    @classmethod
    def from_crawler(cls, crawler):
        """Get the settings and initialize"""

        algolia_api_id = crawler.settings['ALGOLIA_API_ID']
        algolia_api_key = crawler.settings['ALGOLIA_API_KEY']
        algolia_index_name = crawler.settings['ALGOLIA_INDEX_NAME']

        if not algolia_api_id or not algolia_api_key or not algolia_index_name:
            raise NotConfigured(
                'Missing configuration for the AlgoliaItemPipeline'
            )

        algolia_item_bulk_nbr = crawler.settings.get(
            'ALGOLIA_ITEM_BULK_NBR',
            100
        )

        return cls(
            algolia_api_id,
            algolia_api_key,
            algolia_index_name,
            algolia_item_bulk_nbr
        )

    def open_spider(self, spider):
        """Initialize the ``AlgoliaItemExporter``"""

        self.exporter = AlgoliaItemExporter(
            algolia_api_id=self.algolia_api_id,
            algolia_api_key=self.algolia_api_key,
            algolia_index_name=self.algolia_index_name,
            algolia_item_bulk_nbr=self.algolia_item_bulk_nbr
        )
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()

    def process_item(self, item, spider):
        """Export the item using the ``AlgoliaItemExporter``"""

        self.exporter.export_item(item)

        return item
