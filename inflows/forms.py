from django import forms
from . import models


class InflowForm(forms.ModelForm):

    class Meta:
        model = models.Inflow
        fields = ['supplier', 'product', 'quantity', 'description']
        widgets = {
            'supplier': forms.Select(attrs={'class': 'w-full appearance-none rounded-lg border border-white/10 bg-slate-900/60 py-2.5 px-3 pr-8 text-sm text-slate-100 placeholder-slate-500 shadow-inner outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/50'}),
            'product': forms.Select(attrs={'class': 'w-full appearance-none rounded-lg border border-white/10 bg-slate-900/60 py-2.5 px-3 pr-8 text-sm text-slate-100 placeholder-slate-500 shadow-inner outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/50'}),
            'quantity': forms.NumberInput(attrs={'class': 'w-full rounded-lg border border-white/10 bg-slate-900/60 py-2.5 px-3 text-sm text-slate-100 placeholder-slate-500 shadow-inner outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/50'}),
            'description': forms.Textarea(attrs={'class': 'w-full rounded-lg border border-white/10 bg-slate-900/60 py-2.5 px-3 text-sm text-slate-100 placeholder-slate-500 shadow-inner outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/50'})
        }
        labels = {
            'supplier': 'Fornecedor',
            'product': 'Produto',
            'quantity': 'Quantidade',
            'description': 'Descrição'
        }