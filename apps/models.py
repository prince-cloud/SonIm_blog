from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime, timedelta
# Create your models here.
OFFICE = (
    ("PRESIDENT", "PRESIDENT"),
    ("VICE PRESIDENT", "VICE PRESIDENT"),
    ("GENERAL SECRETARY", "GENERAL SECRETARY"),
    ("ORGANIZING SECRETARY", "ORGANIZING SECRETARY"),
    ("FINANCIAL SECRETARY", "FINANCIAL SECRETARY"),
    ("TREASURER", "TREASURER"),
    ("PRO", "PRO"),
    ("TECH SUPPORT", "TECH SUPPORT"),
    ("JUNIOR EXECUTIVE", "JUNIOR EXECUTIVE"),
)

class Profile(models.Model):
    username = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='user_profile/', null=True, blank=True)
    office = models.CharField(choices=OFFICE, max_length=50)
    phone = models.CharField(max_length=10)
    

    def __str__(self):
        return str(self.username) 

class Event(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    image = models.ImageField(upload_to='event_pictures/', null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    content = models.TextField(max_length=100000)
    video_url = models.CharField(max_length=300, null=True, blank=True)
    created_date = models.DateTimeField(auto_now=True)
    
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super(Event, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-created_date',)

    def __str__(self):
        return self.title
    
    def is_new(self):
        return (timezone.now() - timedelta(days=7)) <= self.created_date



class Upcomingevent(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    created_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_date',)

    def __str__(self):
        return self.title



class Member(models.Model):
    full_name = models.CharField(max_length=100, null=False, blank=False)
    phone = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField()
    profile = models.ImageField(upload_to='member_prof_pic/', blank=True)
    reg_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

class Message(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message_body = models.TextField(max_length=100000)

    def __str__(self):
        return self.name + " -- " + self.subject



class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=300)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.event) + " ---- " + self.name



class Picture(models.Model):
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to='event_files/', blank=True)


    def __str__(self):
        return self.name
    

