from django.contrib.auth.models import AbstractUser
from django.db import models

class Bid(models.Model):

    bid = models.IntegerField()

    def __str__(self):
        return f"{self.bid}$"
    

class Comment(models.Model):

    comment = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.comment}"

class Categorie(models.Model):

    categorie = models.CharField(max_length=15)
    listings = models.ManyToManyField('Listing',blank=True)

    def __str__(self):
        return f"{self.id}. {self.categorie}"
    
    

class Listing(models.Model):

    name = models.CharField(max_length=40)
    image = models.CharField(max_length=100000000, blank=True)
    description = models.CharField(max_length=100)
    comments = models.ManyToManyField(Comment, blank= True, related_name="comments")
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="bids")
    item_categories = models.ManyToManyField(Categorie,blank= True)
    activation = models.BooleanField(default=True)
    winner = models.CharField(max_length=32,blank=True)
    

    def __str__(self):
        return f"{self.name}" 


class User(AbstractUser):

    wishlist = models.ManyToManyField(Listing, blank= True, related_name="items")
    comments = models.ManyToManyField(Comment, blank= True)
    created_listing = models.ManyToManyField(Listing,blank=True)

    pass
