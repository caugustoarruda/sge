import json
from django.shortcuts import render
from . import metrics


def home(request):
    
    context = {
        'product_metrics': metrics.get_product_metrics(),
        'sales_metrics': metrics.get_sales_metrics(),
        'daily_sales_data': json.dumps(metrics.get_daily_sales_data()),
        'daily_sales_quantity_data': json.dumps(metrics.get_daily_sales_quantity_data()),
        'product_count_by_category': json.dumps(metrics.get_graphic_product_category_metric()),
        'product_count_by_brand': json.dumps(metrics.get_graphic_product_brand_metric()),
    }
    print(context['product_count_by_category'])
    return render(
        request, 'home.html', context
    )

