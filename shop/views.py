from django.db.models import F, QuerySet, Sum
from django.shortcuts import render

from shop.models import Product


def products(request):
    if request.GET.get("color"):
        product_list = Product.objects.filter(color=request.GET.get("color"))
    else:
        product_list = Product.objects.all()
    order_by = request.GET.get("order_by")

    product_list = product_sorting(product_list, order_by)
    return render(request, "index.html", {"product_list": product_list})


def product_sorting(queryset: QuerySet, order_by: str):
    if order_by == "cost":
        return queryset.order_by("cost")
    elif order_by == "-cost":
        return queryset.order_by("cost")
    elif order_by == "sold":
        queryset = queryset.annotate(sold=Sum(F("cost") * F("purchase__count")))
        return queryset.order_by("sold")
    elif order_by == "popular":
        queryset = queryset.annotate(popular=Sum("purchase__count"))
        return queryset.order_by("popular")
    return queryset


def product_get(request):
    if request.POST.get("title"):
        product_info = Product.objects.filter(title=request.GET.get("title"))
        user_info = Product.objects.filter(purchase__user=request.user)
    else:
        product_info = "Title did not found"
        user_info = "Not available"
    order_by = request.GET.get("order_by")

    # product_info = product_sorting(product_info, order_by)
    return render(request, "index.html", {"product_info": product_info, "user_info": user_info})
