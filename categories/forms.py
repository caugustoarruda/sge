from django import forms
from . import models


class CategoryForm(forms.ModelForm):

    class Meta:
        model = models.Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full rounded-lg border border-white/10 bg-slate-900/60 py-2.5 px-3 text-sm text-slate-100 placeholder-slate-500 shadow-inner outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/50'}),
            'description': forms.Textarea(attrs={'class': 'w-full rounded-lg border border-white/10 bg-slate-900/60 py-2.5 px-3 text-sm text-slate-100 placeholder-slate-500 shadow-inner outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/50'})
        }
        labels = {
            'name': 'Nome',
            'description': 'Descrição'
        }