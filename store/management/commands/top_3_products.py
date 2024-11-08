from django.core.management.base import BaseCommand
from django.db.models import Count
from store.models import Product


class Command(BaseCommand):
    help = 'Finds the top 3 most popular products from users\' carts'

    def handle(self, *args, **kwargs):
        top_products = Product.objects.annotate(
            user_count=Count('item')
        ).order_by(
            '-user_count'
        )[:3]

        if top_products:
            self.stdout.write(self.style.SUCCESS("Top 3 most popular products:"))
            for product in top_products:
                # Applying success style to the text
                self.stdout.write(self.style.SUCCESS(f"{product.name} - added to {product.user_count} users' carts"))
        else:
            self.stdout.write(self.style.ERROR("No products found in carts."))
