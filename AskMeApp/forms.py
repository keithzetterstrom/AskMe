from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        if ' ' in username:
            #self.add_error('username', 'username contanes probel')
            raise
        return username


class RegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(widget=forms.EmailInput)
    avatar = forms.ImageField()


class QuestionForm(forms.Form):
    title = forms.CharField()
    question_text = forms.CharField(widget=forms.TextInput)


class SettingsForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(widget=forms.EmailInput)
    avatar = forms.ImageField()
