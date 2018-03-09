from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control",
                "id":"user_id"
                }
            )
        )
    password = forms.CharField(
        max_length=32,
        widget=forms.PasswordInput(
            attrs={
                "class":"form-control",
                "id":"password_id"
                }
            )
        )

class RegisterForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control",
                "id":"email_id"
                }
            )
        )
    password = forms.CharField(
        max_length=32,
        widget=forms.PasswordInput(
            attrs={
                "class":"form-control",
                "id":"password_id"
                }
            )
        )
    password2 = forms.CharField(
        max_length=32,
        widget=forms.PasswordInput(
            attrs={
                "class":"form-control",
                "id":"password_confirm_id"
                }
            )
        )

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError('Password must match')
        return data
