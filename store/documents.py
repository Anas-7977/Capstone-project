from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import *
import json

@registry.register_document
class ProductDocument(Document):
    name = fields.TextField(fields={"keyword": {"type": "keyword", "ignore_above": 256}})
    description = fields.TextField(fields={"keyword": {"type": "keyword", "ignore_above": 256}})
    price = fields.FloatField()
    created_at = fields.DateField()
    updated_at = fields.DateField()
    sku = fields.LongField()  # SKU for unique identification

    # Foreign Key to Category
    category = fields.Text(attr='category__name')

    # Optional attributes
    brand = fields.TextField()
    weight = fields.FloatField()

    # Product Image
    image_url = fields.KeywordField()

    def prepare_sku(self, instance):
        return instance.sku
    
    def prepare_name(self, instance):
        return instance.name
    
    def prepare_price(self, instance):
        return instance.description
    
    def prepare_brand(self, instance):
        return instance.brand   
    
    def prepare_weight(self, instance):
        return instance.weight
    

    class Index:
        name = 'products'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 2
        }

    class Django:
        model = Product
        queryset_pagination = 1000

    class Meta:
        parallel_indexing = True
        related_models = [Product]
        queryset_pagination = 1000


    @classmethod
    def generate_id(cls, object_instance):
        """
        The default behavior is to use the Django object's pk (id) as the
        elasticsearch index id (_id). If needed, this method can be overloaded
        to change this default behavior.
        """
        return object_instance.sku
