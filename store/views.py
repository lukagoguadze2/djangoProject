from django.core.paginator import Paginator
from django.db.models import Q
from order.forms import AddItemForm
from .forms import SearchCategory
from django.shortcuts import render, get_object_or_404

from .models import Category, Product, Tag


def index(request, slug=''):  # index view-ს იძახებს ორი სხვადასხვა URL
    nothing, price_low_to_high, price_high_to_low, by_date = '0', '1', '2', '3'
    page_id = int(page_id) if (page_id := request.GET.get('page', '1')).isdigit() else 1

    add_item_form = None
    if request.method == "POST":
        item_data = request.POST.copy()
        item_data['cart'] = request.user.usercart.id

        add_item_form = _submit_form(item_data, request.method)

    # პროდუქტების გაფილტვრა კატეგორიის მიხედვით START
    if slug:
        category = Category.objects.filter(slug=slug).first()

        _products = Product.objects.prefetch_related('category').filter(
            category__in=category.get_descendants(include_self=True)
        ).distinct()
    else:
        category = None
        _products = Product.objects.prefetch_related('category')
    # პროდუქტების გაფილტვრა კატეგორიის მიხედვით END

    # პროდუქტების გაფილტვრა form-ით
    form = SearchCategory()
    results = _products

    if 'q' in request.GET:
        form = SearchCategory(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            # შევამოწმოთ დასერჩილი სიტყვა არის თუ არა სახელში, აღწერაში ან სლეგში
            results = _products.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(slug__icontains=q)
            )

    tag = request.GET.get('tag')
    if tag:
        results = results.filter(tags__id=int(tag))

    range_input = request.GET.get('rangeInput')
    if range_input:
        results = results.filter(price__lte=range_input)
    # პროდუქტების გაფილტვრა form-ით END

    # sorting
    if request.GET.get('sort') == price_low_to_high:
        results = results.order_by('price')
    elif request.GET.get('sort') == price_high_to_low:
        results = results.order_by('-price')
    if request.GET.get('page') == by_date:
        results = results.order_by('-product_add_date')

    paginator = Paginator(results.prefetch_related('tags'), per_page=6)

    if category:
        categories = Category.objects.get_categories_with_product_count(category)
    else:
        categories = Category.objects.get_main_categories_with_product_count()

    return render(
        request,
        template_name='index.html',
        context={
            "current_page_overload": category.name if category else None,
            "category": category,
            "categories": categories,
            "tags": Tag.objects.all(),
            "page_obj": paginator.get_page(page_id),
            "add_item_form": add_item_form,
            "form": form
        }
    )


def product_details(request, slug: str, product_id: int):
    form = None
    if request.method == "POST":
        item_data = request.POST.copy()
        item_data['cart'] = request.user.usercart.id

        form = _submit_form(item_data, request.method)

    product = get_object_or_404(Product.objects.prefetch_related('category'), id=product_id)

    return render(
        request,
        'product_details.html',
        {
            "current_page_overload": product.name,
            "product": product,
            "categories": Category.objects.get_categories_with_product_count(),
            "related_products": Product.objects.prefetch_related('category').filter(
                category__in=product.category.all()
            ),
            "item_form": AddItemForm() if form is None else form,
        }
    )


def _submit_form(request_data, method="GET"):
    form = None
    if method == "POST":
        form = AddItemForm(request_data)
        if form.is_valid():
            form.save()

    return form
