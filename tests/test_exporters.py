"""This module contains the ``exporters`` related test cases"""

from unittest import TestCase
from unittest.mock import call, patch

from scrapy_algolia_exporter.exporters import AlgoliaItemExporter


class AlgoliaItemExporterTestCase(TestCase):
    """Test case for the ``AlgoliaItemExporter``"""

    def setUp(self):
        """Initialize the ``AlgoliaItemExporter``"""

        self.algolia_item_exporter = AlgoliaItemExporter(
            algolia_api_id='api_id',
            algolia_api_key='api_key',
            algolia_index_name='index_name'
        )

    def test_start_exporting_should_initialize_the_algolia_client(self):
        """Test that the ``start_exporting`` method should initialize the Algolia client"""

        with patch('algoliasearch.algoliasearch.Client') as mocked_algolia_client:
            self.algolia_item_exporter.start_exporting()

        mocked_algolia_client.assert_has_calls(
            [
                call('api_id', 'api_key'),
                call().init_index('index_name')
            ]
        )
        self.assertEqual(self.algolia_item_exporter.next_items, [])
        self.assertEqual(self.algolia_item_exporter.exported_items_nbr, 0)

    def test_export_item_should_add_the_items_to_the_stack(self):
        """Test that the ``export_item`` method should add the item to the queue"""

        with patch('algoliasearch.algoliasearch.Client'):
            self.algolia_item_exporter.start_exporting()

        # At first, we don't have any items in the queue
        self.assertEqual(self.algolia_item_exporter.next_items, [])

        # Export an item
        self.algolia_item_exporter.export_item({'id': 1})

        # We should have a new item in the queue
        self.assertEqual(self.algolia_item_exporter.next_items, [{'id': 1}])

    def test_export_item_should_call_add_objects_if_algolia_item_bulk_nbr_is_reached(self):
        """Test that the ``export_item`` method should call ``add_objects`` if ``algolia_item_bulk_nbr`` is reached"""

        with patch('algoliasearch.algoliasearch.Client'):
            self.algolia_item_exporter.start_exporting()

        # Add 100 items
        items = [
            {'id': i}
            for i in range(1, 102)
        ]
        with patch.object(self.algolia_item_exporter.algolia_index, 'add_objects') as mocked:
            for item in items:
                self.algolia_item_exporter.export_item(item)

        # The ``_export_items`` was called only once
        mocked.assert_called_once_with(items[:100])

        # The ``next_items`` must contains only 1 item
        self.assertEqual(self.algolia_item_exporter.next_items, [{'id': 101}])
