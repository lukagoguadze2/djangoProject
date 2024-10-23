from django.core.exceptions import ValidationError

from .models import Item
from django import forms


class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['cart', 'product', 'quantity']
        widgets = {
            'quantity': forms.NumberInput(
                attrs={
                    'class': 'form-control form-control-sm text-center border-0',
                    'value': 1,
                    'type': 'text',
                    'min': 1,
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        product = cleaned_data.get('product')
        cart = cleaned_data.get('cart')

        if cart and product and quantity is not None:
            item_exists = Item.objects.filter(cart=cart, product=product).first()
            if item_exists and item_exists.quantity + quantity > product.quantity:
                raise ValidationError(f'ბაზაში არის მხოლოდ {product.quantity} პროდუქტი.')
            elif quantity > product.quantity:
                raise ValidationError(f'ბაზაში არის მხოლოდ {product.quantity} პროდუქტი.')

            if item_exists:
                item_exists.quantity += quantity
                item_exists.save()

        return cleaned_data
