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
        if self.instance.product_id is not None:  # თუ instance არის გადაცემული მაშინ შევამოწმოთ პირდაპირ
            cleaned_data['quantity'] = self.instance.quantity + cleaned_data.get('quantity', 0)
            if cleaned_data['quantity'] > self.instance.product.quantity:
                raise ValidationError(
                    f"ბაზაში არის მხოლოდ {self.instance.product.quantity} {self.instance.product.name}"
                )

        elif (  # თუ პირველად ემატება Item-ი მაშინ შევამოწმოთ შემდეგნაირად
                'quantity' in cleaned_data and
                'product' in cleaned_data and
                cleaned_data['quantity'] > cleaned_data['product'].quantity
        ):
            raise ValidationError(
                f"ბაზაში არის მხოლოდ {cleaned_data['product'].quantity} {cleaned_data['product'].name}"
            )

        return cleaned_data
