from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.http import HttpResponse
from accounts.models import *
from accounts.forms import OrderForm, UserForm
from accounts.filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import pandas as pd
import seaborn as sns
from bokeh.plotting import figure, show
from django_pandas.io import read_frame
from plotly.offline import plot
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio

# Create your views here.

def registerpage(request):
    form = UserForm()

    if request.method=="POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')


    context = {'form':form}
    return render(request, 'accounts/register.html', context)

def loginpage(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'username or pasword is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutuser(request):
    logout(request)
    return redirect('login')


def home(request):

    customers = Customer.objects.all()
    orders = Order.objects.all()

    o = orders[:5]
    total_customers = customers.count()
    total_orders = orders.count()
    pending = orders.filter(status='Pending').count()
    delivered = orders.filter(status='Delivered').count()
    qs = Order.objects.all()
    df = qs.to_dataframe()
    l = []
    q = []
    d = dict()
    x = df['product'].unique()
    for i in df['product']:
        if i in d:
            d[i] = d[i] + 1
        else:
            d[i] = 1
    for i in x:
        l.append(d[i])
    x_data = x
    y_data = l
    # data = [go.Bar(
    #         x=['giraffes', 'orangutans', 'monkeys'],
    #         y=[20, 14, 23]
    # )]

    # plot_div = py.iplot(data, filename='basic-bar')

    # plot_div = plot([go.Bar(x=x_data, y=y_data, mode='lines', name='test', opacity=0.8, marker_color='green')], output_type='div')    

    fig = px.bar(x=x_data, y=y_data)
    pio.write_html(fig, file='hello_world.html', auto_open=True)

    context = {'customers':customers, 'orders':orders, 'pending':pending, 'delivered':delivered, 'total_customers':total_customers,
                    'total_orders':total_orders, 'o':o, 'df': df, 'fig':fig}
    return render(request, 'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products':products})

def customer(request, pk):
    customers = Customer.objects.get(id=pk)
    orders = Order.objects.all()
    orders_counts = orders.count()
    myfilter = OrderFilter(request.GET, queryset=orders)
    orders = myfilter.qs
    context = {'customers':customers, 'orders':orders, 'orders_counts':orders_counts, 'myfilter':myfilter}
    return render(request, 'accounts/customer.html', context)


def createorder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields = ('product', 'status'))
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(instance = customer)
    # form = OrderForm(initial = {'customer':customer})
    if request.method=='POST':
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance = customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset':formset}
    return render(request, 'accounts/order_form.html', context)


def updateorder(request, pk):
    orders = Order.objects.get(id=pk)
    form = OrderForm(instance = orders)
    if request.method=='POST':
        form = OrderForm(request.POST, instance=orders)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}

    return render(request, 'accounts/order_form.html', context)

def deleteorder(request, pk):
    orders = Order.objects.get(id=pk)
    if request.method=="POST":
        orders.delete()
        return redirect('/')
    context = {'item':orders}
    return render(request, 'accounts/delete_form.html', context)
