from django import forms
from . import models


class ProductForm(forms.ModelForm):

    class Meta:
        model = models.Product
        fields = ['title', 'category', 'brand', 'description', 'serie_number', 'cost_price', 'selling_price']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full rounded-lg border border-white/10 bg-slate-900/60 py-2.5 px-3 text-sm text-slate-100 placeholder-slate-500 shadow-inner outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/50'}),
            'category': forms.Select(attrs={'class': 'w-full appearance-none rounded-lg border border-white/10 bg-slate-900/60 py-2.5 px-3 pr-8 text-sm text-slate-100 placeholder-slate-500 shadow-inner outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/50'}),
            'brand': forms.Select(attrs={'class': 'w-full appearance-none rounded-lg border border-white/10 bg-slate-900/60 py-2.5 px-3 pr-8 text-sm text-slate-100 placeholder-slate-500 shadow-inner outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/50'}),
            'description': forms.Textarea(attrs={'class': 'w-full rounded-lg border border-white/10 bg-slate-900/60 py-2.5 px-3 text-sm text-slate-100 placeholder-slate-500 shadow-inner outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/50'}),
            'serie_number': forms.TextInput(attrs={'class': 'w-full rounded-lg border border-white/10 bg-slate-900/60 py-2.5 px-3 text-sm text-slate-100 placeholder-slate-500 shadow-inner outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/50'}),
            'cost_price': forms.NumberInput(attrs={'class': 'w-full rounded-lg border border-white/10 bg-slate-900/60 py-2.5 px-3 text-sm text-slate-100 placeholder-slate-500 shadow-inner outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/50'}),
            'selling_price': forms.NumberInput(attrs={'class': 'w-full rounded-lg border border-white/10 bg-slate-900/60 py-2.5 px-3 text-sm text-slate-100 placeholder-slate-500 shadow-inner outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/50'})
        }
        labels = {
            'title': 'Titulo',
            'category': 'Categoria',
            'brand': 'Marca',
            'description': 'Descrição',
            'serie_number': 'Número de série',
            'cost_price': 'Preço de custo',
            'selling_price': 'Preço de venda'
        }