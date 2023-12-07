from django.db import models
from datetime import datetime
import re


class UserManager(models.Manager):
    def basic_validator(self,postData):
        errors = {}
        if len(postData['fname']) < 3:
            errors["fname"] = "User First Name should be at least 6 characters"
        if len(postData['lname']) < 3:
            errors["lname"] = "User Last Name should be at least 6 characters"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['useremail']):      
            errors['useremail'] = "Invalid email address!"
        if len(User.objects.filter(email_address = postData['useremail'])) > 0:
            errors["useremail"] = "Email address exist!"
            
        if len(postData['inputpass']) < 8 :
            errors['inputpass'] = "Password is Weak, Choose Another Please!"
        if postData['inputpass'] != postData['confirminputpass']:
            errors['confirminputpass'] = "Password does not match!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email_address = models.EmailField()
    password = models.TextField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    def new_user(first_name,last_name,email_address,password):
        return User.objects.create(first_name=first_name,last_name=last_name,email_address=email_address,password=password)
    
class Message(models.Model):
    message_entry = models.TextField(default="This is an Empty Message!")
    user = models.ForeignKey(User,related_name = "messages",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def new_msg(message_entry,user):
        Message.objects.create(message_entry=message_entry,user=user)
    def display_msgs():
        return Message.objects.all()
    def delete_msg(id):
        msg1 = Message.objects.filter(id=int(id))
        msg1.delete()
    
class Comment(models.Model):
    comment_entry = models.TextField()
    user = models.ForeignKey(User,related_name="comments",on_delete=models.CASCADE)
    message = models.ForeignKey(Message,related_name="comments",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def new_cmnt(comment_entry,user,message):
        Comment.objects.create(comment_entry=comment_entry,user=user,message=message)
    
    def delete_cmnt(id):
        cmnt1 = Comment.objects.get(id=int(id))
        cmnt1.delete()