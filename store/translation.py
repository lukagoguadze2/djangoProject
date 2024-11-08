from modeltranslation.translator import register, TranslationOptions
from django.utils.translation import gettext_lazy as _
from .models import Category


@register(Category)
class NewsTranslationOptions(TranslationOptions):
    fields = ('name',)

    fallback_values = {'name': _('ტექსტი არ არის გადათარგმნილი')}
