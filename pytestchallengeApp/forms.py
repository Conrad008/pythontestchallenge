from django import forms


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Enter your email"
            }
        )
    )