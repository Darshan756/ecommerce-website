from django import forms 
from .models import CustomUser
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email','phone_number','password']
   
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
           self.add_error('confirm_password', 'Passwords do not match')
        return cleaned_data
    
    def save(self,commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        user.set_password(password)
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter phone number'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter password'
        self.fields['confirm_password'].widget.attrs['placeholder'] = 'Enter confirm password'
        for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'  


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter email', 'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password', 'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if not email:
            self.add_error('email', 'Email is required.')
        if not password:
            self.add_error('password', 'Password is required.')

        return cleaned_data
    
 



