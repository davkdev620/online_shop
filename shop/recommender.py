import redis
from django.conf import settings
from .models import Product

"""
The system selects relevant items for a user based on
their behavior and the knowledge it has about them. It will suggest products
based on historical sales, thus identifying products that are usually bought together.
Product detail page: You will display a list of products that are usually
bought with the given product. This will be displayed as users who bought
this also bought X, Y, Z.
Cart detail page: Based on the products users add to the cart, it will suggest products that are usually 
bought together with these ones. In this case, the score you calculate to obtain related products has to be aggregated.
"""

# Connect to redis db.
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT, db=settings.REDIS_DB)


class Recommender(object):

    def get_product_key(self, id):
        return f'product:{id}:purchased_with'

    def products_bought(self, products):
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                # Get the other products bought with each product.
                if product_id != with_id:
                    # Increment score for product purchased together.
                    r.zincrby(self.get_product_key(product_id), 1, with_id)

    def suggest_products_for(self, products, max_results=6):
        product_ids = [p.id for p in products]
        if len(products) == 1:
            # Only 1 product.
            suggestions = r.zrange(self.get_product_key(product_ids[0]),
                                   0, -1, desc=True)[:max_results]
        else:
            # Generate a temporary key.
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = f'tmp_{flat_ids}'
            # Multiple products, combine scores of all products.
            # Store the resulting sorted set in a temporary key
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)
            # Remove ids for the products the recommendation is for
            r.zrem(tmp_key, *product_ids)
            # Get the product ids by their score, descendant sort.
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            # Remove the temporary key.
            r.delete(tmp_key)
        suggested_products_ids = [int(id) for id in suggestions]

        # Get suggested products and sort by order of appearance.
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))
