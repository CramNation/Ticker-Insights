from django.shortcuts import render
from backtests.choices import symbol_choices


def index(request):

    return render(request, 'tickersymbols/search.html')


