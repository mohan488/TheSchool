from django import forms
from .models import User, Question


class userForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput,help_text='Atleast 8 characters having 1 digit and 1 special character')
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    first_name = forms.CharField(label='First Name',)
    last_name = forms.CharField(label='Last Name',)
    email = forms.EmailField(label='Email',)
    username = forms.CharField(label='User Name',)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

    def clean_first_name(self):
        firstname = self.cleaned_data['first_name']

        if any(char.isdigit() for char in firstname):
            raise forms.ValidationError("First Name cannot have numbers")
        return firstname

    def clean_last_name(self):
        lastname = self.cleaned_data['last_name']

        if any(char.isdigit() for char in lastname):
            raise forms.ValidationError("Last Name cannot have numbers")
        return lastname
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if "edu" != email.split("@")[1].split('.')[1]:
            raise forms.ValidationError("Please use .edu email ")
        return email

    def clean_password2(self):
        pas = self.cleaned_data['password']
        cd =   self.cleaned_data['password2']
        MIN_LENGTH=8
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if pas and cd:
            if pas != cd:
                raise forms.ValidationError('Passwords don\'t match.')
            else:
                if len(pas)<MIN_LENGTH:
                    raise forms.ValidationError("Password should have atleast %d characters"%MIN_LENGTH)
                if pas.isdigit():
                    raise forms.ValidationError("Password should not be all numeric")
                if pas.isalpha():
                    raise forms.ValidationError("Password should have atleast one digit")
                if not any(char in special_characters for char in pas):
                    raise forms.ValidationError("Password should have atleast one Special Character")


class loginForm(forms.Form):
    class Meta:
        model = User
        fields = ('username','password')

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class questionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text',)

    text = forms.CharField(label="Question", widget=forms.Textarea)
