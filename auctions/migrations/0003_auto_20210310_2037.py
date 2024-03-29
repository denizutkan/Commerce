# Generated by Django 3.1.3 on 2021-03-10 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bids_comments_listing'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bids',
            new_name='Bid',
        ),
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
        migrations.AddField(
            model_name='user',
            name='wishlist',
            field=models.ManyToManyField(blank=True, related_name='items', to='auctions.Listing'),
        ),
    ]
