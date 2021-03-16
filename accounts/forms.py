from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model, authenticate

USERNAME_REGEX = '^[a-zA-Z0-9.@+-]*$'

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username', validators=[RegexValidator(
                        regex = USERNAME_REGEX,
                        message='Username must be Alphanumeric or contain any of the following ". @ + -"',
                        code='invalid_username'
                    )])
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        the_user = authenticate(username=username, password=password)

        if not the_user:
            raise forms.ValidationError("Invalid Credentials")
        # user_obj = User.objects.filter(username=username).first
        # if not user_obj:
        #     raise forms.ValidationError("Invalid Username")
        # else:    
        #     if not user_obj.check_password(password):
        #         raise forms.ValidationError("Invalid Password")
        return super(UserLoginForm, self).clean(*args, **kwargs)