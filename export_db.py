import csv

from django.shortcuts import redirect
# from api.models import Category, Product


def exportaDB(request):
    reader = csv.DictReader(open("products.csv"))
    for raw in reader:
        cat = Category.objects.get(name=raw['category'])
        print(cat)
        p = Product(
            name=raw['name'],
            category=cat,
            price=raw['price'],
            cost=raw['cost']
        )

        p.save()

    # cat = Category.objects.get(id=1)
    # p = Product(name='Beatles Blog', category=cat, price=100)
    # p.save()

    return redirect('categories-list')


def exportaStock(request):
    reader = csv.DictReader(open("products.csv"))
    for raw in reader:
        prod = Product.objects.get(name=raw['nProducto'])

        if prod:
            prod.stock = raw['stock']
        else:
            print(raw['nProducto'], "not found")

        prod.save()

    # cat = Category.objects.get(id=1)
    # p = Product(name='Beatles Blog', category=cat, price=100)
    # p.save()

    return redirect('categories-list')
