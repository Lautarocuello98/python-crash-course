from django.shortcuts import render
from django.http import HttpResponse
from .models import Pizza

def index(request):
    return HttpResponse("Pizzeria Home Page")

def pizzas(request):
    """Show all pizzas."""
    pizzas = Pizza.objects.order_by('name')
    context = {'pizzas': pizzas}
    return render(request, 'pizzas/pizzas.html', context)


def pizza(request, pizza_id):
    """Show one pizza and its toppings."""

    pizza = Pizza.objects.get(id=pizza_id)

    toppings = pizza.topping_set.all()

    context = {
        'pizza': pizza,
        'toppings': toppings
    }

    return render(request, 'pizzas/pizza.html', context)