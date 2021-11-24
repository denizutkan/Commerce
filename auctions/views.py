from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Comment, Categorie, Bid


def index(request):

    active_listings = Listing.objects.filter(activation = True).all()
    
    return render(request, "auctions/index.html",{
        "active_listings":active_listings,
        "categorie_number": 0
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def item(request,item_name):

    wishlist = False
    lower_bid = False
    user_listing = False

    item = Listing.objects.get(name=item_name)

    ## check the item is in the wishlist
    if request.user.is_authenticated:
        wishlist = False
        ## get the user who signed in
        user = User.objects.get(username= request.user.username)
        if item in user.wishlist.all():
            wishlist = True
        if item in user.created_listing.all():
            user_listing = True

    if request.method == 'POST':

        user = User.objects.get(username= request.user.username)
        
        if request.POST.get("wishlist"):
            
            if request.user.is_authenticated:
                if item in user.wishlist.all():
                    user.wishlist.remove(item)
                else:
                    user.wishlist.add(item)

        if request.POST.get("closelisting"):
            
            if request.user.is_authenticated:

                item.activation = False
                item.save()

        if request.POST.get("add_comment"):

            new_comment = request.POST.get("comment").capitalize()

            if new_comment != "":

                comment = Comment(comment=new_comment)
                comment.save()
                item.comments.add(comment)
                user.comments.add(comment)

        if request.POST.get("place_bid"):

            new_bid = request.POST.get("new_bid")

            if item.bid.bid > int(new_bid):
                lower_bid = True

                return render(request, "auctions/item.html",{

                "wishlist":wishlist,
                "user_listing":user_listing,
                "item": item,
                "description": item.description,
                "comments": item.comments.all(),
                "bid":item.bid,
                "error":lower_bid,
                "activation":item.activation,
                "item_categories":item.item_categories.all()
                })

            else:
                
                item.bid.bid = int(new_bid)
                item.bid.save()
                item.winner = user.username
                item.save()


        return HttpResponseRedirect(reverse("item",args=(item_name,)))



    return render(request, "auctions/item.html",{

        "wishlist":wishlist,
        "user_listing":user_listing,
        "item": item,
        "description": item.description,
        "comments": item.comments.all(),
        "bid":item.bid,
        "error":lower_bid,
        "activation":item.activation,
        "item_categories":item.item_categories.all()
        
    })




@login_required
def create(request):

    DefaultBid = 1
    if request.method == 'POST':
        item_name = request.POST.get("name", "").capitalize()
        if Listing.objects.filter(name=item_name):
            error = True

            return render(request, "auctions/create.html",{
                "error1": error,
                "categories":Categorie.objects.all()
            })

        item_bid = request.POST.get("bid", DefaultBid)
        item_description = request.POST.get("description", "").capitalize()
        item_image = request.POST.get("image", "")
            

        
        bid = Bid(bid=item_bid)
        bid.save()
        
        item = Listing(name= item_name,bid = bid,description=item_description, image=item_image)
        item.save()

        for categorie in Categorie.objects.all():
            item_categorie = request.POST.get(f"{categorie.categorie}")
            if item_categorie != None:
                item.item_categories.add(categorie)
                categorie.listings.add(item)

        user = User.objects.get(username= request.user.username)
        user.created_listing.add(item)
        return HttpResponseRedirect(reverse("item",args=(item_name,)))

    return render(request, "auctions/create.html",{
        "categories":Categorie.objects.all()
    })

def wishlist(request):

    if request.user.is_authenticated:
        ## get the user who signed in
        user = User.objects.get(username= request.user.username)
            
    return render(request, "auctions/wishlist.html",{
        "wishlist": user.wishlist.all()
    })

def categories(request):
    
    return render(request, "auctions/categories.html",{
        "categories":Categorie.objects.all()
    })

def categorie_page(request, categorie_number):
    active_listings = Listing.objects.filter(activation = True).all()
    categorie_listings = Categorie.objects.get(id=categorie_number)

    return render(request, "auctions/index.html",{
        "categorie_number": categorie_number,
        "active_listings":active_listings,
        "categorie_listings": categorie_listings.listings.all()
    })