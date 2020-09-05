from django import forms
from .models import Member, Event, Upcomingevent, Message, Profile, Comment, Picture
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from multiupload.fields import MultiFileField

class ProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        label="Profile",
        help_text="upload a passport sized photograph",
    )
    office = forms.ChoiceField(
        help_text="please select respective office",
        choices=(
    ("PRESIDENT", "PRESIDENT"),
    ("VICE PRESIDENT", "VICE PRESIDENT"),
    ("GENERAL SECRETARY", "GENERAL SECRETARY"),
    ("ORGANIZING SECRETARY", "SECRETARY"),
    ("FINANCIAL SECRETARY", "FINANCIAL SECRETARY"),
    ("TREASURER", "TREASURER"),
    ("PRO", "PRO"),
    ("TECH SUPPORT", "TECH SUPPORT"),
    ("JUNIOR EXECUTIVE", "JUNIOR EXECUTIVE"),
)
    )
    class Meta:
        model = Profile
        fields = ('username', 'phone', 'profile_picture', 'office',)


class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(
        label="Re-enter password",
        widget=forms.PasswordInput
    )
    password = forms.CharField(
        widget=forms.PasswordInput
    )
    username = forms.CharField(
        help_text="case sensitive",
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', )

    def clean_password2(self, *args, **kwargs):
        data = self.cleaned_data
        p = data['password2']
        p_1 = data['password']
        if len(p) < 6:
            raise forms.ValidationError(
                'Your password should be 6 or more characters')
        if p == p_1:
            return p
        raise forms.ValidationError("Your passwords do not match")


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('full_name', 'phone', 'email', 'profile',)


class EventForm(forms.ModelForm):
    video_url = forms.CharField(
        help_text="leave blank if no video",
        required=False,
    )

    class Meta:
        model = Event
        fields = ('title', 'description', 'content', 'video_url', 'image', )


class DateInput(forms.DateTimeInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class UpcomingEventForm(forms.ModelForm):
    date = forms.DateTimeField(widget=DateInput)
    time = forms.TimeField(widget=TimeInput)

    class Meta:
        model = Upcomingevent
        fields = ('title', 'description', 'date', 'time',)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('name', 'email', 'subject', 'message_body',)
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'common-input mb-20 form-control',
                    'placeholder': 'Enter your name here'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'common-input mb-20 form-control',
                    'placeholder': 'Enter email here'
                }
            ),
            'subject': forms.TextInput(
                attrs={
                    'class': 'common-input mb-20 form-control',
                    'placeholder': 'Enter subject here'
                }
            ),
            'message_body': forms.Textarea(
                attrs={
                    'class': 'common-textarea form-control',
                    'placeholder': 'Enter Message here'
                }
            ),
        }


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body',)
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'common-input mb-20 form-control',
                    'placeholder': 'Enter your name here'
                }
            ),
            'body': forms.Textarea(
                attrs={
                    'class': 'common-textarea form-control',
                    'placeholder': 'Enter Comments here'
                }
            ),
        }

class AddPictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ('image',)
        widgets = {
            'image': forms.ClearableFileInput(
                attrs={
                    'multiple': True
                }
            )
        }