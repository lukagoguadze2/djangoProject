from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

# Storing orders without Models
orders = []


def order_list(request):
    if request.method == 'GET':
        order_list_html = "<ul>"
        for order in orders:
            order_list_html += f"<li>{order['customer_name']} ordered {order['product_name']} x{order['quantity']}</li>"
        order_list_html += "</ul>"
        order_list_html += '<a href="/order/create-order/">Create Order</a>'
        return HttpResponse(order_list_html)

    return HttpResponse(status=404)


@csrf_exempt
def create_order(request):
    if request.method == "POST":
        customer_name = request.POST.get('customer_name')
        product_name = request.POST.get('product_name')
        quantity = request.POST.get('quantity')

        orders.append({
            'customer_name': customer_name,
            'product_name': product_name,
            'quantity': quantity
        })

        return redirect('/order/')

    if request.method == "GET":
        return HttpResponse(f'''
            <form method="POST" action="/order/create-order/">
                <input type="text" name="customer_name" placeholder="Customer Name" required>
                <input type="text" name="product_name" placeholder="Product Name" required>
                <input type="number" name="quantity" placeholder="Quantity" required>
                <button type="submit">Submit Order</button>
            </form>
        ''')

    return HttpResponse(status=404)
