# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class ProductManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData["name"]) < 2:
            errors["name"] = "name too short"
        if len(postData["description"]) < 10:
            errors["description"] = "Description is too short"
        return errors

    def category_validator(self, postData):
        errors = {}
        if len(postData['newcategory']) < 2:
            errors["bad_category_name"] = "Category name is too short"
        return errors
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return "<Product: {} {}>".format(self.name, self.id)

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    category = models.ForeignKey(Category, related_name="products")
    image = models.CharField(max_length=255)
    objects = ProductManager()
    def __str__(self):
        return "<Product: {} {}>".format(self.name, self.id)