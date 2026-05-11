from django.forms import ModelForm
from . import models


class BrandForm(ModelForm):

    class Meta:
        model = models.Brand
        fields = ['name', 'description']