from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db import models
from django.contrib.auth.decorators import login_required
from .models import Event, Upcomingevent, Gallery, Profile, Comment, Images
from .forms import MemberForm, EventForm, UpcomingEventForm, AddPictureForm, MessageForm, ProfileForm, RegisterForm, AddCommentForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.forms import modelformset_factory

from django.views.generic.edit import FormView
# Create your views here.


def index(request):
    events = Event.objects.all()
    upcomingevents = Upcomingevent.objects.all()
    return render(request,
                  'index.html',
                  {
                      'events': events,
                      'upcomingevents': upcomingevents,
                  })


def event(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events,})


def eventdetail(request, event_slug):
    eventdetail = get_object_or_404(Event, slug=event_slug)
    pictures = Gallery.objects.all()

    if request.method == 'POST':
        form = AddCommentForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.event_id = eventdetail.id
            messages.success(request, 'Comment succeffully posted')
            comment.save()
            form.save()
        else:
            messages.error(request, 'invalid data entry')

    return render(request, 
        'events.html', 
            {
                'eventdetail': eventdetail, 
                'comment_form': AddCommentForm(),
                'pictures': pictures,
            })

        

def event_pictures(request):
    gallerypics = Gallery.objects.all()
    eventpics = Event.objects.all()
    #event_pictures = get_object_or_404(Gallery, slug=gallery_slug)
    return render(request, 'event_pictures.html',
                  {
                      'event_pictures': event_pictures,
                      'gallerypics': gallerypics,
                      'eventpics': eventpics,

                  })


def gallery(request):
    pictures = Gallery.objects.all()
    return render(request,
                  'gallery.html',
                  {
                      'pictures': pictures,
                  })


def be_a_member(request):
    if request.method == 'POST':
        form = MemberForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
    return render(request,
                  'be_a_member.html',
                  {
                      'member_form': MemberForm(),
                  })


@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            newevent = form.save(commit=False)
            newevent.author = request.user
            newevent.save()
            return redirect('index')
    return render(request,
                  'add_event.html',
                  {
                      'add_event_form': EventForm(),
                  })


@login_required
def add_upcoming_event(request):
    if request.method == 'POST':
        form = UpcomingEventForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            messages.error(request, 'Invalid Data Entry')
    return render(request,
                  'add_upcoming_event.html',
                  {
                      'add_upcoming_event_form': UpcomingEventForm(),
                  })


""" @login_required
def add_picture(request):
    if request.method == 'POST':
        form = AddPictureForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_picture')
        else:
            messages.error(request, 'Picture not added')
    return render(request,
                  'add_picture.html',
                  {
                      'add_picture_form': AddPictureForm(),
                  })
 """

def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        form = MessageForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message successfully sent')
        else:
            messages.error(request, 'Invalid Data Entry')
    return render(request,
                  'contact.html',
                  {
                      'message_form': MessageForm(),
                  })


def our_team(request):
    users = User.objects.all()
    profiles = Profile.objects.all()
    return render(request, 'our_team.html', {'users': users, 'profiles':profiles,})


def register(request):
    if request.method == "POST":
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = form.save()
            user.set_password(data['password'])
            user.save()
            return redirect('create_profile')

    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {"form": form})


def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, files=request.FILES)
        new_user = User.objects.all().order_by('-id').first()
        print(new_user)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.user_id = new_user.id
            form.save()
            return redirect('our_team')

    return render(request, 'registration/create_profile.html',
                  {
                      'create_user_form': ProfileForm(),

                  })


@login_required
def add_picture(request):
    if request.method == 'POST':
        form = AddPictureForm(data=request.POST, files=request.FILES)
        files = request.FILES.getlist('image')
        if form.is_valid():
            for f in files:
                gallery = Gallery(image=f,)
                gallery.save()
        else:
            messages.error(request, 'Picture not added')
    return render(request,
                  'add_picture.html',
                  {
                      'add_picture_form': AddPictureForm(),
                  })
                  