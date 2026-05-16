from django.shortcuts import render
from . import metrics


def home(request):
    
    context = {
        'product_metrics': metrics.get_product_metrics()
    }

    return render(
        request, 'home.html', context
    )

