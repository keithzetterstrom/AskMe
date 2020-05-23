from PIL import Image
from django import forms
from django.contrib.auth import authenticate
from django.forms import ModelForm
from AskMeApp.models import User, Question, Answer


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        super().clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data


class RegisterForm(ModelForm):
    repeat_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'avatar']
        widgets = {
            'password': forms.PasswordInput(),
            'email': forms.EmailInput(),
            'avatar': forms.ClearableFileInput()
        }

    def clean_avatar(self):
        image = self.cleaned_data.get('avatar')

        try:
            img = Image.open(image.file)
            if img.format not in ('JPG', 'PNG', 'JPEG'):
                raise forms.ValidationError("Invalid image type. Please upload jpg, png or jpeg")

            max_size = 64
            if any(dim > max_size for dim in image.image.size):
                fmt = img.format.lower()
                img.thumbnail((max_size, max_size))
                image.file = type(image.file)()
                img.save(image.file, fmt)
            return image

        except Exception:
            raise forms.ValidationError("Invalid image type. Please upload jpg, png or jpeg")

    def clean(self):
        cd = super().clean()
        if cd['password'] != cd['repeat_password']:
            self.add_error('password', 'Password mismatch')

    def save(self, commit=True):
        cd = self.cleaned_data
        user = User.objects.create_user(username=cd['username'],
                                        password=cd['password'],
                                        email=cd['email'],
                                        avatar=cd['avatar'])
        return user


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'question_text', 'tags']
        widgets = {
            'question_text': forms.Textarea(),
            'tags': forms.CheckboxSelectMultiple(),
        }


class SettingsForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'avatar']
        widgets = {
            'email': forms.EmailInput(),
            'avatar': forms.FileInput()
        }

    def clean_avatar(self):
        image = self.cleaned_data.get('avatar')

        try:
            img = Image.open(image.file)
            if img.format not in ('JPG', 'PNG', 'JPEG'):
                raise forms.ValidationError("Invalid image type. Please upload jpg, png or jpeg")

            max_size = 64
            if any(dim > max_size for dim in image.image.size):
                fmt = img.format.lower()
                img.thumbnail((max_size, max_size))
                image.file = type(image.file)()
                img.save(image.file, fmt)
            return image

        except Exception:
            raise forms.ValidationError("Invalid image type. Please upload jpg, png or jpeg")


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text']
        widgets = {
            'answer_text': forms.Textarea(),
        }
