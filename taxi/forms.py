from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Driver, Car


def validate_license_number(lic_number: str) -> str:
    if len(lic_number) != 8:
        raise ValidationError("License number must be equal 8 symbols")
    elif len(lic_number) == 8:
        for i in range(0, 3):
            if lic_number[i] != lic_number[i].capitalize():
                raise ValidationError("First 3 letter must be capitalize")
            if not lic_number[i].isalpha():
                raise ValidationError("first 3 symbols must be a letter")
        for elem in range(3, 8):
            if not lic_number[elem].isnumeric():
                raise ValidationError("Last 5 symbols must be a integer")
    return lic_number


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = (UserCreationForm.Meta.fields + ("first_name",
                                                  "last_name",
                                                  "license_number"))

    def clean_license_number(self):
        lic_number = self.cleaned_data["license_number"]
        return validate_license_number(lic_number)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        lic_number = self.cleaned_data["license_number"]
        return validate_license_number(lic_number)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
