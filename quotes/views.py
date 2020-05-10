from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib import messages

import requests
import json

from .models import Stock
from .forms import StockForm


def search_stock(base_url, stock_ticker):
    try:
        token = settings.IEXCLOUD_TEST_API_TOKEN
        url = base_url + stock_ticker + '/quote?token=' + token
        data = requests.get(url)

        if data.status_code == 200:
            data = json.loads(data.content)
        else:
            data = {'Error' : 'There was a problem with your provided ticker symbol. Please try again'}
    except Exception as e:
        data = {'Error':'There has been some connection error. Please try again later.'}
    return data
   
def home(request):
    if request.method == 'POST':
        stock_ticker = request.POST['stock_ticker']
        base_url = 'https://sandbox.iexapis.com/stable/stock/'
        stocks = search_stock(base_url, stock_ticker)
        return render(request, 'quotes/home.html', {'stocks':stocks})
    return render(request, 'quotes/home.html')

def about(request):
    return render(request, 'quotes/about.html')

def add_stock(request):
    if request.method == 'POST':
        print('inside post')
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, 'stock has been added successfully.')
            return redirect('add_stock')
    else:
        stocks = Stock.objects.all()
        return render(request, 'quotes/add_stock.html', {'stocks':stocks})
    
if __name__ == "__main__":
    base_url = 'https://sandbox.iexapis.com/stable/stock/'
    stock_ticker = 'IBM'

    data = connect(base_url, stock_ticker)