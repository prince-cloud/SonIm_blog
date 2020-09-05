from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db import models
from django.contrib.auth.decorators import login_required
from .models import Event, Upcomingevent, Profile, Comment, Picture, Member
from .forms import AddPictureForm, MemberForm, EventForm, UpcomingEventForm,  MessageForm, ProfileForm, RegisterForm, AddCommentForm
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
    pictures = Picture.objects.all()

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



def gallery(request):
    pictures = Picture.objects.all()
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
            return redirect('/')
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
            return redirect('/')
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
def add_picture(request, id):
    add_picture = get_object_or_404(Event, id=id)

    if request.method == 'POST':
        form = AddPictureForm(data=request.POST, files=request.FILES)
        files = request.FILES.getlist('image')
        if form.is_valid():
            
            for f in files:
                picture = form.save(commit=False)
                picture.id = add_picture.id
                picture = Picture.objects.create(image=f, name=add_picture.slug)
                picture.save()
            
            return redirect ('index')
    return render(request, 
        'add_picture.html',
        {
            'event': event,
            'add_picture': add_picture,
            'add_picture_form': AddPictureForm(),
            
            
        })

def registered_members(request):
    members = Member.objects.all()
    return render (request, 'memberlist.html', {'members': members})