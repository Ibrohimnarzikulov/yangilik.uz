from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Profile


class SignupForm(UserCreationForm):
    """Ro'yxatdan o'tish formasi — username, email, ism, familiya va parol."""
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={
            'placeholder': 'you@example.com',
            'class': 'form-control',
        }),
    )
    first_name = forms.CharField(
        max_length=150,
        required=False,
        label="Ism",
        widget=forms.TextInput(attrs={
            'placeholder': "Ismingiz",
            'class': 'form-control',
        }),
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        label="Familiya",
        widget=forms.TextInput(attrs={
            'placeholder': "Familiyangiz",
            'class': 'form-control',
        }),
    )

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Foydalanuvchi nomi',
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Parol maydonlariga ham class qo'shamiz
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '••••••••',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '••••••••',
        })


class LoginForm(AuthenticationForm):
    """Tizimga kirish formasi — username va parol."""
    username = forms.CharField(
        label="Foydalanuvchi nomi",
        widget=forms.TextInput(attrs={
            'placeholder': 'Foydalanuvchi nomi',
            'class': 'form-control',
            'autofocus': True,
        }),
    )
    password = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'form-control',
        }),
    )


class ProfileForm(forms.ModelForm):
    """Foydalanuvchi asosiy ma'lumotlarini tahrirlash uchun forma."""
    first_name = forms.CharField(
        max_length=150,
        required=False,
        label="Ism",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        label="Familiya",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class AvatarForm(forms.ModelForm):
    """Avatar yuklash/almashtirish uchun forma."""
    avatar = forms.ImageField(
        required=False,
        label="Avatar",
        widget=forms.FileInput(attrs={'class': 'form-control-file'}),
    )

    class Meta:
        model = Profile
        fields = ("avatar",)