from django.db import models
from django.db.models import Q, When, Case, IntegerField


class CategoryManager(models.Manager):
    def get_main_categories_with_subcategories(self):
        all_categories = self.prefetch_related('product_set').annotate(
            is_main_category=Case(
                When(parent=None, then=0),  # მთავარი კატეგორიას მივანიჭოთ 0
                default=1,  # ქვეკატეგორიას მივანიჭოთ 1
                output_field=IntegerField(),
            )
        ).order_by('is_main_category', 'name')  # დავალაგოთ ისე რომ მთავარი კატეგორიები პირველი გამოჩნდეს

        category_lookup = {category.id: category for category in all_categories}

        main_categories = {}  # მთავარი კატეგორიები როგორც key და მათში შესაბამისი ქვეკატეგორიები როგორც value
        for category in all_categories:
            if category.is_main_category == 0:
                main_categories[category] = []
            else:
                break  # რადგანაც მთავარი კატეგორიები თავშია შესაბამისად შევწეროთ ციკლი როდესაც ქვეკატეგორია მოიძებნება
                
        added_subcategories = set()

        # ციკლი მანამ სანამ ყველა ქვეკატეგორია დაემატება მთავარ კატეგორიებში
        # len(main_categories.keys()) - მთავარი კატეგორიების რაოდენობა
        # len(added_subcategories) - დაემატებული ქვეკატეგორიების რაოდენობა
        # NOTE: while ციკლი დატრიალდება მანამ სანამ არ ჩავა იერარქიის ბოლო დონეზე
        while len(added_subcategories) + len(main_categories.keys()) < len(all_categories):
            for key, value in main_categories.items():
                # თავიდან დავიწყოთ ციკლი იმ ქვეკატეგორიების რომელიც არ არის დამატებული
                for category in [cat for cat in all_categories if cat.id not in added_subcategories]:
                    if category not in main_categories.keys() and (
                            category_lookup[category.parent_id] == key or
                            category_lookup[category.parent_id] in value
                    ):
                        value.append(category)
                        added_subcategories.add(category.id)

        return {
            'category_dict': main_categories,
            'all_categories': all_categories
        }
    
    def with_product_count(self):
        response = self.get_main_categories_with_subcategories()
        cat_dict = response['category_dict']
        main_categories = cat_dict.keys()

        results = []
        for main_category in main_categories:
            # ეს იქნება იმ პროდუქტების ID რომლებსაც კატეგორიებში მთავარი კატეგორია აქვს
            direct_product_ids = {main.id for main in main_category.product_set.all()}

            # ეს იქნება იმ პროდუქტების ID რომლებსაც კატეგორიებში მთავარი კატეგორიის ქვეკატეგორიები აქვს
            subcategory_product_ids = set()
            for subcategory in cat_dict[main_category]:
                subcategory_product_ids.update(
                    {sub.id for sub in subcategory.product_set.all()}
                )

        # თანაკვეთა იქნება ისეთი პროდუქტების ID სადაც მთავარი კატეგორია და ამ მთავარი კატეგორიის ქვეკატეგორიებიც აქვს
            intersection_ids_set = direct_product_ids & subcategory_product_ids

            # გაერთიანება იქნება ყველა უნიკალური პროდუქტის ID
            total_unique_ids = direct_product_ids | subcategory_product_ids

            # დავაბრუნოთ ჯეისონი საჭირო ინფორმაციით
            results.append({
                    'id': main_category.id,
                    'name': main_category.name,
                    'direct_product_count': len(direct_product_ids),
                    'subcategory_product_count': len(subcategory_product_ids),
                    'intersection_count': len(intersection_ids_set),
                    'total_product_count': len(total_unique_ids),
                })

        return results
        

class ProductManager(models.Manager):
    def get_products_by_category(self, category):
        """
        Returns a list of all products associated with a particular category and its subcategories
        :param category:
        """
        return self.prefetch_related(
                'category'
            ).filter(
                # ისეთი პროდუქტები სადაც კატეგორებში არის მთავარი კატეგორია ან ქვეკატეგორია
                Q(category=category) | Q(category__parent=category)
            ).distinct().values('id', 'name', 'price', 'quantity')
