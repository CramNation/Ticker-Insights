from django.shortcuts import render
from backtests.earnings import EarningsClass
from backtests.sma import SMAClass
from django.http import HttpResponse, Http404
from matplotlib import pylab
from pylab import *
import io
import base64
from backtests.choices import symbol_choices


def index(request):
    
    if 'symbol' in request.GET:
        symbol = request.GET.get('symbol', 'Invalid Symbol')
        symbol_upper = request.GET.get('symbol', 'Invalid Symbol').upper()
        request.session['symbol'] = symbol
    else:
        symbol = request.session['symbol']
        symbol_upper = request.session['symbol'].upper()
    
    if symbol_upper in symbol_choices:
    # Initiliaze earnings object
        earnings_object = EarningsClass(symbol)

    #String 1
        Q1_string_context = earnings_object.Q1_string

    #String 2
        Q2_string_context = earnings_object.Q2_string

    #String 3
        Q3_string_context = earnings_object.Q3_string

    #String 4
        Q4_string_context = earnings_object.Q4_string

    #Plot 1
        Q1_plot = earnings_object.Q1_plot

    #Plot 2
        Q2_plot = earnings_object.Q2_plot

    #Plot 2
        Q3_plot = earnings_object.Q3_plot

    #Plot 2
        Q4_plot = earnings_object.Q4_plot

    
        context = {
        'symbol':symbol,
        'symbol_upper':symbol_upper,
        'Q1_string_context':Q1_string_context,
        'Q2_string_context':Q2_string_context,
        'Q3_string_context':Q3_string_context,
        'Q4_string_context':Q4_string_context,
        'Q1_plot':Q1_plot,
        'Q2_plot':Q2_plot,
        'Q3_plot':Q3_plot,
        'Q4_plot':Q4_plot,
        }

    
        return render(request, 'backtests/earnings.html', context)
    else:
        return render(request, 'tickersymbols/invalidsymbol.html')

def sma(request):

    symbol = request.session.get('symbol', 'none')
    symbol_upper = request.session['symbol'].upper()

    if symbol_upper in symbol_choices:

        sma_object = SMAClass(symbol)

        plot = sma_object.plot()

        context = {
        'symbol':symbol,
        'plot':plot,
        } 
    
    return render(request, 'backtests/sma.html', context)

def yieldcurve(request):

    symbol = request.session.get('symbol', 'none')
    
    return render(request, 'backtests/yieldcurve.html', {'symbol': symbol})

