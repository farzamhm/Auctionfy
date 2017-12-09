from django.shortcuts import render, redirect, render_to_response
from .forms import RegistrationForm, EditProfileForm
from django.contrib.auth.decorators import login_required
import random
import sys, os, django
from django.http import *
from django.views.generic import  ListView, TemplateView, CreateView, DetailView, DeleteView
from .models import *
from main.forms import SearchBox
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
import datetime
from django.db.models import Max
import smtplib
from django.template import loader
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib.auth.mixins import LoginRequiredMixin

sys.path.append("C:/Users/Vaio/Desktop/auction1")
os.environ["DJANGO_SETTINGS_MODULE"]="auction.settings"
django.setup() 

def home(request):
    return render(request, 'profile/home.html')

def about(request):
    return render(request , 'profile/About.html')
def contact(request):
    return render(request , 'profile/Contact.html')
@login_required
def chat(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    rooms = Room.objects.order_by("title")

    # Render that in the index template
    return render(request, "index.html", {
        "rooms": rooms,
    })



def save_bid(request):
    context = dict()
    context['product_list'] = Product.objects.get(id=request.POST.get('product_id'))
    context['seller'] = Seller.objects.get(product_id_id=request.POST.get('product_id'))
    try:
        last_bid=Bidder.objects.filter(product_id=request.POST.get('product_id')).last()
        last_bid_amount=last_bid.bid_amount
    except:
        last_bid = Product.objects.get(id=request.POST.get('product_id'))
        last_bid_amount=last_bid.minimum_price
    if request.method == 'POST':
        if int(request.POST.get('minimum_price')) > int(request.POST.get('bid_amount')):
            context['error'] = "bid price should be more than minimum price"
            return render(request, 'main/product_detail.html', context)
        elif int(last_bid_amount) >= int(request.POST.get('bid_amount')):
            context['error'] = "bid price should be higher than last bid amount"
            return render(request, 'main/product_detail.html', context)
        else:
            x = Bidder.objects.filter(product_id=Product.objects.get(id=request.POST.get('product_id'))).values('user_name')
            a = 0
            for item in x:
                if item['user_name'] == request.user.id:
                    y = Bidder.objects.get(user_name=request.user.id, product_id=Product.objects.get(id=request.POST.get('product_id')))
                    y.bid_amount = int(request.POST.get('bid_amount'))
                    y.save()
                    a = 1
            if not a:
                obj = Bidder(user_name=request.user, product_id=Product.objects.get(id=request.POST.get('product_id')), bid_amount=int(request.POST.get('bid_amount')))
                obj.save()
            return HttpResponseRedirect(reverse('view_product'))
    return render(request, 'main/product_detail.html', context)

def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = RegistrationForm()
    args = {'form': form}
    return render(request, 'profile/reg_form.html/', args)


class homepage(TemplateView):
    template_name= 'profile/homepage.html'

    def get(self, request):
        form = SearchBox()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = SearchBox(request.POST)
        if form.is_valid():
            text = form.cleaned_data['search']
            form = SearchBox()

        args = {'form':form ,'text':text}
        return render(request, self.template_name, args)

def profile(request):#LoginRequiredMixin,request):

    return render(request,'profile/profile.html')


def edit_profile(request):
    login_url = '/login/'
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form':form}
        return render(request, 'profile/edit_profile.html', args)


class ProductView(LoginRequiredMixin,ListView):
    model=Product
    login_url = '/login/'
class AddProductView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    model = Product
    fields = ["product_name", "category", "minimum_price", "bid_end_date", "image", "description"]

    def form_valid(self, form):
        obj = Seller(user_name = self.request.user, product_id = form.save())
        obj.save()
        return super(AddProductView, self).form_valid(form)

    def get_success_url(self):
        return reverse('view_product')

class ProductDetailView(LoginRequiredMixin,DetailView):
    model = Product
    context_object_name = 'product_list'
    login_url = '/login/'
 
    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        x = Seller.objects.all()
        context["seller"] = Seller.objects.get(product_id_id=self.kwargs['pk'])
        return context


class BidderListView(LoginRequiredMixin,ListView):
    model = Bidder
    login_url = '/login/'
    def get_queryset(self):
        return Bidder.objects.filter(product_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(BidderListView, self).get_context_data(**kwargs)
        context["product_id"] = self.kwargs['pk']
        context["room"] = Product.objects.get(id= self.kwargs['pk']).product_name
        context["sold"] = Product.objects.get(id=self.kwargs['pk']).sold

        return context

class ProductDelete(DeleteView,LoginRequiredMixin):
    model = Product
    login_url = '/login/'
    def get_context_data(self, **kwargs):
        context = super(ProductDelete, self).get_context_data(**kwargs)
        context["product_id"] = self.kwargs['pk']
        return context
    def get_success_url(self):
        return reverse('view_product')


@login_required
def index(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    rooms = Room.objects.order_by("title")


    # Render that in the index template
    return render(request, "index.html", {
        "rooms": rooms,
    })

@login_required
def index1(request,pk):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    rooms = Room.objects.order_by("title")
    print(pk)
    rooms = Room.objects.filter(ID_product=pk)


    # Render that in the index template
    return render(request, "index.html", {
        "rooms": rooms,
    })
 
# fromaddr = "auctionify.herokuapp@gmail.com"
# toaddr = "zhosseinzadeh.hanza@yahoo.com"
# msg = MIMEMultipart()
# msg['From'] = fromaddr
# msg['To'] = toaddr
# msg['Subject'] = "test_first"
# print('1')
# body = "you have recieved a new bid"
# msg.attach(MIMEText(body, 'plain'))
# print('2')
# server = smtplib.SMTP('smtp.gmail.com', 587)
# print('3')
# server.starttls()
# server.login(fromaddr, "farzam123")
# print('4')
# text = msg.as_string()
# server.sendmail(fromaddr, toaddr, text)
# print ('successfull')
# server.quit()


def mailing(bidder, seller):
    template = loader.get_template("main/college_mail.html")
    if (bidder == 0):
        result = template.render(context={'status': "Your product bid end has been completed. "
                                                    "No auction customers for you product. Please register once again."})
        friend = seller[0]['email']
        msg = MIMEMultipart()
        msg['From'] = 'auctionify.herokuapp@gmail.com'
        msg['To'] = seller[0]['email']
        msg['Subject'] = "Product auction date ended"
        msg.attach(MIMEText(result, 'html'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('auctionify.herokuapp@gmail.com', 'farzam123')
        text = msg.as_string()
        server.sendmail('auctionify.herokuapp@gmail.com', friend, text)
        server.close()
    else:
        result = template.render(context={'status': "You won the product in auction please contact "+seller[0]['email']})
        friend = bidder[0]['email']
        msg = MIMEMultipart()
        msg['From'] = 'auctionify.herokuapp@gmail.com'
        msg['To'] = bidder[0]['email']
        msg['Subject'] = "Product auction date ended"
        msg.attach(MIMEText(result, 'html'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('auctionify.herokuapp@gmail.com', 'farzam123')
        text = msg.as_string()
        server.sendmail('auctionify.herokuapp@gmail.com', friend, text)
        server.close()

        result = template.render(context={'status': "Your product bid"
                                                    " end date has been completed. please contact " + bidder[0]['email'] +" bid the product for highest amount"})
        friend = seller[0]['email']
        msg = MIMEMultipart()
        msg['From'] = 'auctionify.herokuapp@gmail.com'
        msg['To'] = seller[0]['email']
        msg['Subject'] = "Product auction date ended"
        msg.attach(MIMEText(result, 'html'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('auctionify.herokuapp@gmail.com', 'farzam123')
        text = msg.as_string()
        server.sendmail('auctionify.herokuapp@gmail.com', friend, text)
        server.close()

        if(len(bidder)>1):
            result = template.render(context={'status':"your bid amount did not win the product! Come explore for more products and bid them!"})
            friend = ",".join(person['email'] for person in bidder[1:])
            msg = MIMEMultipart()
            msg['From'] = 'auctionify.herokuapp@gmail.com'
            msg['To'] = friend
            msg['Subject'] = "college report using onlinedb.py"
            msg.attach(MIMEText(result, 'html'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('auctionify.herokuapp@gmail.com', 'farzam123')
            text = msg.as_string()
            server.sendmail('auctionify.herokuapp@gmail.com', friend, text)
            server.close()


def send_email():
    product = Product.objects.all()
    for item in product:
        if(item.bid_end_date <= datetime.date.today()):
            bidder = User.objects.filter(bidder__product_id=item.id).annotate(max = Max('bidder__bid_amount')).values('email').order_by('-max')
            seller = User.objects.filter(seller__product_id=item.id).values('email')
            if(bidder):
                mailing(bidder, seller)
            else:
                mailing(0, seller)
            Bidder.objects.filter(product_id=item.id).delete()
            Seller.objects.filter(product_id=item.id).delete()
            Product.objects.get(id=item.id).delete()


# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
 
 
# fromaddr = "auctionify.herokuapp@gmail.com"
# toaddr = "zhosseinzadeh.hanza@yahoo.com"
# msg = MIMEMultipart()
# msg['From'] = fromaddr
# msg['To'] = toaddr
# msg['Subject'] = "test_first"
# print('1')
# body = "you have recieved a new bid"
# msg.attach(MIMEText(body, 'plain'))
# print('2')
# server = smtplib.SMTP('smtp.gmail.com', 587)
# print('3')
# server.starttls()
# server.login(fromaddr, "farzam123")
# print('4')
# text = msg.as_string()
# server.sendmail(fromaddr, toaddr, text)
# print ('successfull')
# server.quit()
