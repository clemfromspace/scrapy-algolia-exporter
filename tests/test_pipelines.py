"""This module contains the ``pipelines`` related test cases"""

from unittest import TestCase
from unittest.mock import Mock

from scrapy.exceptions import NotConfigured
from scrapy.crawler import Crawler

from scrapy_algolia_exporter.pipelines import AlgoliaItemPipeline


class AlgoliaItemPipelineTestCase(TestCase):
    """Test case for the ``AlgoliaItemPipeline``"""

    def setUp(self):
        """Create a fake scrapy ``Crawler``"""

        self.crawler = Crawler(
            spidercls=Mock(),
            settings={
                'ALGOLIA_API_ID': 'api_id',
                'ALGOLIA_API_KEY': 'api_key',
                'ALGOLIA_INDEX_NAME': 'index_name'
            }
        )

    def test_from_crawler_should_initialize_the_pipeline(self):
        """Test that the ``from_crawler`` method should correctly initialize the pipeline"""

        pipeline = AlgoliaItemPipeline.from_crawler(crawler=self.crawler)

        self.assertEqual(pipeline.algolia_api_id, 'api_id')
        self.assertEqual(pipeline.algolia_api_key, 'api_key')
        self.assertEqual(pipeline.algolia_index_name, 'index_name')

    def test_missing_mandatory_settings_should_raise_an_exception(self):
        """Test that the ``from_crawler`` method should correctly initialize the pipeline"""

        with self.assertRaises(NotConfigured):
            AlgoliaItemPipeline.from_crawler(
                crawler=Crawler(
                    spidercls=Mock(),
                    settings={
                        'ALGOLIA_API_KEY': 'api_key',
                        'ALGOLIA_INDEX_NAME': 'index_name'
                    }
                )
            )
