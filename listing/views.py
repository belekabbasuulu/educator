from django.shortcuts import render, redirect
from django.views import View
from .models import Listing, User, Categories
from django.contrib import auth
from django.core.paginator import Paginator
from django.db.models import Q


class BaseView(View):

    def get(self, request):
        listing = Listing.objects.order_by('-listing_date')[:8]
        context = {"listing": listing}
        return render(request, 'home.html', context)


def create_view(request):
    if request.method == 'POST':
        title = request.POST['title']
        owner = request.user
        price = request.POST['price']
        description = request.POST['description']
        image = request.FILES['image']
        category = request.POST['category']
        status = request.POST['status']

        category = Categories.objects.get(id=int(category))
        listing = Listing.objects.create(
            title=title,
            owner=owner,
            price=price,
            description=description,
            image=image,
            category=category,
            status = status
        )
        listing.save()
        return redirect('/')
    else:
        categories = Categories.objects.all()
        STATUS = [i[0] for i in Listing.STATUS]
        context = {
            'categories': categories,
            'STATUS': STATUS
        }
        return render(request, 'create.html', context)


class AllView(View):

    def get(self, request):
        listing = Listing.objects.all()
        categories = Categories.objects.all()
        paginator = Paginator(listing, 4)
        if 'page' in request.GET:
            page_num = request.GET['page']
        else:
            page_num = 1
        page = paginator.get_page(page_num)
        context = {
            'page': page,
            'listing': page.object_list,
            "categories": categories
        }
        return render(request, 'all_tutors.html', context)


def detail_view(request, id):
    list_item = Listing.objects.get(id=id)
    related_list = Listing.objects.filter(
        ~Q(id=list_item.id), category__title__iexact=list_item.category)[:8]
    context = {
        "item": list_item,
        "related_list": related_list
    }
    return render(request, 'detail.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('base')
        else:
            return redirect('login')
    else:
        return render(request, 'login.html')


def registration(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        address = request.POST['address']
        phone = request.POST['phone']
        password = request.POST['password']
        email = request.POST['email']

        user = User.objects.create_user(
            username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        user.save()
        return redirect('login')
    else:
        return render(request, 'registration.html')


def search_view(request):
    if request.method == 'POST':
        listings = Listing.objects.all()
        if 'keywords' in request.POST:
            keywords = request.POST['keywords']
            if keywords:
                listings = listings.filter(
                    Q(title__icontains=keywords) |
                    Q(description__icontains=keywords) |
                    Q(price__icontains=keywords) |
                    Q(owner__first_name__icontains=keywords) |
                    Q(owner__last_name__icontains=keywords)
                )
        context = {
            "listings": listings
        }
        return render(request, 'search.html', context)
    else:
        return render(request, 'home.html')


def all_search_view(request):
    if request.method == 'POST':
        if 'keywords' in request.POST:
            keywords = request.POST['keywords']
            listings = Listing.objects.filter(
                Q(title__icontains=keywords) | 
                Q(description__icontains=keywords) | 
                Q(status__iexact=keywords) |
                Q(category__title__iexact=keywords)
            )
        context = {"listings": listings}
        return render(request, 'search.html', context)
    else:
        return render(request, 'all_tutors.html')


def user_panel_view(request):
    us = request.user
    return render(request, 'user_panel.html', {"us": us})
