from django.db import models

class Transaction(models.Model):
    user_id = models.IntegerField(null=False)
    account_id = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)
    info = models.CharField(max_length=10000)

class Item_table(models.Model):
    user_id = models.IntegerField(null=False)
    item_id = models.CharField(max_length=100)
    access_token = models.CharField(max_length=100)

class Account(models.Model):
    user_id = models.IntegerField(null=False)
    account_id = models.CharField(max_length=100)
    item_id = models.CharField(max_length=10000)
    info = models.CharField(max_length=10000)


