from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from taxi.models import Driver, Car


REGEX_VALIDATOR = RegexValidator(
    regex=r'^[A-Z]{3}\d{5}$',
    message="License number must be in the format ABC12345: "
            "Consist only of 8 characters, "
            "first 3 characters are uppercase letters, "
            "last 5 characters are digits.",
    code='invalid_license_number'
)


class DriverCreationForm(UserCreationForm):
    """Form for creating a new driver."""

    license_number = forms.CharField(
        required=True,
        validators=[REGEX_VALIDATOR],
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverUpdateForm(forms.ModelForm):
    """Form for updating a driver."""

    license_number = forms.CharField(
        required=True,
        validators=[REGEX_VALIDATOR],
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    """Form for creating a new car."""

    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"


class CarSearchForm(forms.Form):
    model = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by model.."}),
    )
