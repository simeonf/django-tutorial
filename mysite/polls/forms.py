from django import forms

attrs = {'class': 'required'}
class RegistrationForm(forms.Form):
    username = forms.RegexField(regex=r'^[a-zA-Z]+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs),
                                error_messages={'invalid':
                                                "This value must contain only letters, "
                                                "numbers and underscores."}
                                )
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs,maxlength=75)),
                                label="E-mail")
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs,
                                render_value=False),
                                label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs,
                                render_value=False),
                                label="Password Again")

    def clean(self):
        data = self.cleaned_data
        if not data.get('password1') == data.get('password2'):
            raise forms.ValidationError("Passwords must match!")
        return data    

