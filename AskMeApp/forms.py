import string
from PIL import Image
from django import forms
from django.contrib.auth import authenticate
from django.db import transaction
from django.forms import ModelForm
from AskMeApp.models import User, Question, Answer, Tag


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        super().clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        # если пользователь не зарегистрирован, возвращаем сообщение об ошибке
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
        # провверяем, является ли файл картинкой и соответствует ли он нужным форматам
        try:
            img = Image.open(image.file)
            if img.format not in ('JPG', 'PNG', 'JPEG'):
                raise forms.ValidationError("Invalid image type. Please upload jpg, png or jpeg")

            max_size = 64
            # если картинка больше нужного размера, изменяем размер
            if any(dim > max_size for dim in image.image.size):
                fmt = img.format.lower()
                img.thumbnail((max_size, max_size))
                image.file = type(image.file)()
                img.save(image.file, fmt)
            return image

        except:
            return image

    def clean(self):
        cd = super().clean()
        # проверяем соответствие придуманного пароля и повторенного пароля при регистрации
        if cd['password'] != cd['repeat_password']:
            self.add_error('password', 'Password mismatch')

    def save(self, commit=True):
        cd = self.cleaned_data
        # сохранение переопределено, тк стандартнное сохранение user не учитывает аватар
        user = User.objects.create_user(username=cd['username'],
                                        password=cd['password'],
                                        email=cd['email'],
                                        avatar=cd['avatar'])
        return user


class QuestionForm(ModelForm):
    tags = forms.CharField()

    class Meta:
        model = Question
        fields = ['title', 'question_text']
        widgets = {
            'question_text': forms.Textarea(),
            # 'tags': forms.CheckboxSelectMultiple(),
        }

    def clean_tags(self):
        tags_set = self.cleaned_data.get('tags')
        tags_ids = []
        tags_lst = tags_set.split(' ')
        for tag in tags_lst:
            if not tag:
                continue
            tt = str.maketrans("", "", ".,;")
            tag_name = tag.translate(tt)
            try:
                with transaction.atomic():
                    tag_obj = Tag(tag_name=tag_name)
                    tag_obj.save()
                    tags_ids.append(tag_obj.id)
            except:
                tags_ids.append(Tag.objects.get(tag_name=tag_name).id)
        return tags_ids


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

        except:
            return image


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text']
        widgets = {
            'answer_text': forms.Textarea(),
        }
