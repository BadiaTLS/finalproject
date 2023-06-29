from django import forms

class LoginForm(forms.Form):
    from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'text-body', 'id': 'email'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'text-body', 'id': 'password'})
    )
