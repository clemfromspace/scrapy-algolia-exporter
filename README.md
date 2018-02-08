[![PyPI](https://img.shields.io/pypi/v/scrapy_algolia_exporter.svg)](https://pypi.python.org/pypi/scrapy_algolia_exporter) [![Build Status](https://travis-ci.org/clemfromspace/scrapy-algolia-exporter.svg?branch=master)](https://travis-ci.org/clemfromspace/scrapy-algolia-exporter)

## Scrapy Algolia Exporter

Directly populate a given **Algolia** index from a scrapy spider.

### Usage

:warning: **Your crawled items must contains a unique `ObjectID` key.** :warning:

Add the mandatory scrapy settings to configure the **Algolia** API:

```python
ALGOLIA_API_ID='my_algolia_api_id'
ALGOLIA_API_KEY='my_algolia_api_key'
ALGOLIA_INDEX_NAME='my_algolia_index_name'
```

Add the `AlgoliaItemPipeline` in the `ITEM_PIPELINES` scrapy setting:

```python
ITEM_PIPELINES = {
   'scrapy_algolia_exporter.pipelines.AlgoliaItemPipeline': 10
}
```


The `ALGOLIA_ITEM_BULK_NBR` setting control how many items will be send to Algolia at the same time.
If not provided, the items will be send by group of `100`.

### Install
```
pip install scrapy_algolia_exporter
```






