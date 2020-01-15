from __future__ import unicode_literals
from django.db import models
import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def validate(self, postData):
        errors = {}
        if Users.objects.filter(email= postData['email']):
            errors['email_exists'] = "This email address is already linked to another account"
        if len(postData['first_name']) < 2:
            errors["first_name"] = "Name field is required"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Name field is required"
        if EMAIL_REGEX.match(postData['email']) == None:
            errors["email"] = "Please input a valid email"
        if len(postData['pw']) < 8:
            errors["pw"] = "Password must be at least 8 characters long"
        if postData['pw'] !=postData['confirm']:
            errors['confirm'] = "Must match password"
        return errors

    def logVal(self, postData):
        user = Users.objects.filter(email = postData['login_email'])
        errors = {}
        if EMAIL_REGEX.match(postData['login_email']) == None:
            errors["email"] = "Please input a valid email"
        if len(postData['login_password']) < 8:
            errors["pw"] = "Password must be at least 8 characters long"
        if not user:
            errors['email'] = "Please enter valid email address"
        if user and not bcrypt.checkpw(postData['login_password'].encode('utf8'), user[0].password.encode('utf8')):
            errors['password'] = "Invalid password"
        return errors
    
    def jobval(self,postData):
        errors = {}
        if len(postData['title']) < 1:
            errors["title"] = "Title cannot be left blank"
        if len(postData['description']) < 1:
            errors["description"]= "Description cannot be left blank"
        if len(postData['title']) < 3:
            errors["title"] = "Title must be at least 3 characters"
        if len(postData['description']) < 3:
            errors["description"] = "Description must be at least 3 characters"
        if len(postData['location']) < 1:
            errors['location'] = "Location cannot be left blank"
        if len(postData['location']) < 3:
            errors['location'] = "Location must be at least 3 chacaters long"
        return errors

class Users(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    confirm = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Jobs(models.Model):
    title = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    location = models.CharField(max_length = 255)
    created_by = models.ForeignKey(Users, related_name = "jobs_planned")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




