from django import forms
from django.core.exceptions import ValidationError
from . import models


class OutflowForm(forms.ModelForm):

    class Meta:
        model = models.Outflow
        fields = ['product', 'quantity', 'description']
        widgets = {
            'product': forms.Select(attrs={'class': 'w-full appearance-none rounded-lg border border-white/10 bg-slate-900/60 py-2.5 px-3 pr-8 text-sm text-slate-100 placeholder-slate-500 shadow-inner outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/50'}),
            'quantity': forms.NumberInput(attrs={'class': 'w-full rounded-lg border border-white/10 bg-slate-900/60 py-2.5 px-3 text-sm text-slate-100 placeholder-slate-500 shadow-inner outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/50'}),
            'description': forms.Textarea(attrs={'class': 'w-full rounded-lg border border-white/10 bg-slate-900/60 py-2.5 px-3 text-sm text-slate-100 placeholder-slate-500 shadow-inner outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/50'})
        }
        labels = {
            'product': 'Produto',
            'quantity': 'Quantidade',
            'description': 'Descrição'
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        product = self.cleaned_data.get('product')

        if quantity > product.quantity:
            raise ValidationError(
                f'A quantidade disponível em estoque para o produto {product.title} é de {product.quantity}'
            )
        else:
            return quantity