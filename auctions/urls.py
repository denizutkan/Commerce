from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("categories",views.categories, name="categories"),
    path("categorie_id=<int:categorie_number>",views.categorie_page,name="categorie_page"),
    path("<str:item_name>",views.item, name="item")
    
]
