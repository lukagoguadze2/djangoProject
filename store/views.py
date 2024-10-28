from abc import abstractmethod, ABC

from django.db.models import Q
from django.views import View
from django.views.generic import ListView, DetailView

from order.forms import AddItemForm
from .forms import SearchForm
from django.shortcuts import get_object_or_404

from .models import Category, Product, Tag
from order.models import Item


# რადგან ერთი და იმავე POST რექუერსტს ვიყენევთ გამოვაცხადოთ abstract კლასი
class PostRequest(View, ABC):
    additional_context = {}  # ჩვენით ჩავამატოთ რაიმე დამატებითი კონტექსტი

    @abstractmethod
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        item_data = self.request.POST.copy()
        if self.request.user.is_authenticated:  # შევამოწმოთ თუ მომხმარებელი არის შესული ექაუნთში
            item_data['cart'] = self.request.user.usercart.id

            if item := Item.objects.select_related('product').filter(
                    product_id=item_data.get('product'),
                    cart_id=item_data.get('cart')
            ).first():
                add_item_form = AddItemForm(item_data, instance=item)
            else:
                add_item_form = AddItemForm(item_data)

            if add_item_form.is_valid():
                add_item_form.save()

            self.additional_context['add_item_form'] = add_item_form

        return self.get(request, *args, **kwargs)


class IndexView(ListView, PostRequest):
    model = Product
    paginate_by = 6
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug', '')

        # თუ slug არის მაშინ კატეგორიების URL-იძახებს views
        if slug:
            category = get_object_or_404(Category, slug=slug)
            context['current_page_overload'] = category.name
            context['categories'] = Category.objects.get_categories_with_product_count(category)
        else:
            context['current_page_overload'] = None
            context['categories'] = Category.objects.get_main_categories_with_product_count()

        context['tags'] = Tag.objects.all()
        context['form'] = SearchForm(self.request.GET or None)  # ეს ფორმა გამოიყენება პროდუქტების სერჩისათვის

        # გადავცეთ queries HTML-ს შემდეგ რომ გამოჩნდეს რა გავფილტრეთ
        context['queries'] = {f: n for f, n in self.request.GET.items()}

        # თუ request GET მეთოდი გვაქვს მაშინ წავშალოთ add_item_form რადგან ის მხოლოდ POST რექუესტზე გვჭირდება
        if self.request.method == "GET" and 'add_item_form' in self.additional_context:
            del self.additional_context['add_item_form']

        context.update(self.additional_context)  # დავამატოთ ჩვენი დამატებითი კონტექსტი

        return context

    def get_ordering(self):
        order_dict = {
            '0': None,
            '1': 'price',
            '2': '-price',
            '3': '-product_add_date'
        }
        sort_type = self.request.GET.get('sort', '0')
        self.ordering = order_dict.get(sort_type, None)

        return super().get_ordering()

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.kwargs.get('slug') is not None:
            category = Category.objects.filter(slug=self.kwargs.get('slug')).first()
            queryset = queryset.filter(
                category__in=category.get_descendants(include_self=True)
            ).distinct()

        form = SearchForm(self.request.GET)

        if form.is_valid():
            q = form.cleaned_data.get('q')
            range_input = form.cleaned_data.get('rangeInput')
            tag = form.cleaned_data.get('tag')

            if q is not None:
                q = form.cleaned_data['q']
                # შევამოწმოთ დასერჩილი სიტყვა არის თუ არა სახელში, აღწერაში ან სლეგში
                queryset = queryset.filter(
                    Q(name__icontains=q) |
                    Q(description__icontains=q) |
                    Q(slug__icontains=q)
                )

            if range_input is not None:
                queryset = queryset.filter(price__lte=range_input)

            if tag is not None:
                queryset = queryset.filter(tags=tag)

        return queryset.prefetch_related('category').prefetch_related('tags')


class ProductView(DetailView, PostRequest):
    model = Product
    pk_url_kwarg = 'product_id'
    template_name = 'product_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['current_page_overload'] = context[self.get_context_object_name(self.object)].name
        context['categories'] = Category.objects.get_main_categories_with_product_count()

        context["related_products"] = self.model.objects.prefetch_related('category').filter(
                category__in=self.object.category.all()
            )

        if self.request.method == "GET" and 'add_item_form' in self.additional_context:
            del self.additional_context['add_item_form']

        context['add_item_form'] = self.additional_context.get('add_item_form', None) or AddItemForm()

        return context
