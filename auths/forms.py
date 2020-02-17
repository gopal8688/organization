from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Customer

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Customer
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Customer
        fields = ('email',)