# from django import forms


# class PasswordResetRequestForm(forms.Form):
#     email = forms.EmailField(
#         label="Email",
#         widget=forms.EmailInput(
#             attrs={
#                 "placeholder": "Enter your email"
#             }
#         )
#     )

from django import forms
from django.contrib.auth.password_validation import (
    validate_password,
)


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Enter your email"
            }
        )
    )


class NewPasswordForm(forms.Form):
    password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter new password"
            }
        )
    )

    password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm new password"
            }
        )
    )

    def __init__(
        self,
        *args,
        user=None,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.user = user

    def clean_password1(self):
        password = self.cleaned_data[
            "password1"
        ]

        validate_password(
            password,
            self.user
        )

        return password

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get(
            "password1"
        )

        password2 = cleaned_data.get(
            "password2"
        )

        if (
            password1
            and password2
            and password1 != password2
        ):
            self.add_error(
                "password2",
                "Passwords do not match."
            )

        return cleaned_data