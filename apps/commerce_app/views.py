from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Category, Product
from django.contrib.auth.models import User
from .forms import PriceForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from social_django.models import UserSocialAuth

# Create your views here.
def index(request):
    # Product.objects.filter(id=11),#pornhub
    # Product.objects.filter(id=22),#aderol
    # Product.objects.filter(id=14),#box of wine
    # Product.objects.filter(id=23),#pallet of monsters
    # featured products
    context = {
        "categories": Category.objects.all(),
        "products":Product.objects.all(),
    }
    return render(request, "commerce_app/index.html", context)

def checkout(request):
    return render(request, "commerce_app/checkout.html")

def edit(request):
    print request.session["cart"]
    request.session["cart"] = request.session["updatedCart"]
    total = 0.00
    for i in request.session["cart"]:
            total += request.session["cart"][i]["quantity"] * request.session["cart"][i]["price"]
    context = {
        "total" : total
    }
    return render(request, "commerce_app/edit.html", context)

def showCategory(request, category):
    context = {
        "categories": Category.objects.all(),
        "products": Product.objects.filter(category=Category.objects.get(name=category))
    }
    return render(request, "commerce_app/showItems.html", context)

def searchHelper(string, term):
    term = term.lower()
    string = string.lower()
    for i in range(0, len(string)):
        match = False
        if string[i] == term[0] and i + len(term) <= len(string):
            match = True
            for j in range(1, len(term)):
                if string[i + j] != term[j]:
                    match = False
                    break
        if match:
            return True
    return False

def search(request):
    return redirect("/search/" + request.POST["search"])

def showSearchResults(request, searchTerm):
    results=[]
    for product in Product.objects.all():
        if searchHelper(product.name, searchTerm):
            print product.name
            results.append(product)
        elif searchHelper(product.description, searchTerm):
            print product.name
            results.append(product)
    context = {
        "categories": Category.objects.all(),
        "products": results
    }
    return render(request, "commerce_app/showItems.html", context)

@login_required
def addproduct(request):
    if not request.user.is_superuser:
        return redirect("/shop")
    context = {
        "categories": Category.objects.all(),
        "priceform": PriceForm(),
    }
    return render(request, "commerce_app/addProduct.html", context)

@login_required
def create(request):
    if request.POST["newcategory"] != "":
        errors = Product.objects.category_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect("/addproduct")
        category = Category.objects.create(name=request.POST["newcategory"])
        Product.objects.create(name=request.POST["name"], description=request.POST["description"], price=float(request.POST["price"]), category=category, image=request.POST["img"])
    else:
        errors = Product.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect("/commerce_app/addproduct")
        category = Category.objects.get(id=int(request.POST["category"]))
        Product.objects.create(name=request.POST["name"], description=request.POST["description"], price=float(request.POST["price"]), category=category, image=request.POST["img"])
    return redirect("/")

@login_required
def checkout(request):
    total = 0.00
    for i in request.session["cart"]:
            total += request.session["cart"][i]["quantity"] * request.session["cart"][i]["price"]
    context = {
        "total" : total
    }
    return render(request, "commerce_app/checkout.html", context)

@login_required
def cart(request, id):
    if "cart" not in request.session:
        request.session["cart"] = {}
    product = Product.objects.get(id=id)
    if str(product.id) not in request.session["cart"]:
        request.session["cart"][product.id] = {
            "name" : product.name,
            "price" : product.price,
            "quantity" : int(request.POST["quantity"]),
            "id":product.id
        }
        request.session["updatedCart"] = request.session["cart"]
        return redirect("/edit")
    request.session["cart"][str(product.id)]['quantity'] += int(request.POST["quantity"])
    request.session["updatedCart"] = request.session["cart"]
    return redirect("/edit")

@login_required
def remove(request, id):
    request.session["cart"].pop(str(id))
    request.session["updatedCart"] = request.session["cart"]
    return redirect("/edit")

@login_required
def update(request, id):
    product = Product.objects.get(id=id)
    request.session["cart"][str(product.id)]["quantity"] = int(request.POST["quantity"])
    request.session["updatedCart"] = request.session["cart"]
    return redirect("/edit")