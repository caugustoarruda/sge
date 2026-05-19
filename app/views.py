import json
from django.shortcuts import render
from . import metrics


def home(request):
    
    context = {
        'product_metrics': metrics.get_product_metrics(),
        'sales_metrics': metrics.get_sales_metrics(),
        'daily_sales_data': json.dumps(metrics.get_daily_sales_data()),
    }
    print(context['daily_sales_data'])
    return render(
        request, 'home.html', context
    )

