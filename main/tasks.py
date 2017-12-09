from __future__ import absolute_import , unicode_literals
import random
from celery.decorators import task
from main.models import Product,Bidder
import datetime


@task(name="sum_two_numbers")
def add(x , y):
    return x + y


@task(name="multiply_two_numbers")
def mul(x , y):
    total = x * (y * random.randint(3 , 100))
    return total


@task(name="sum_list_numbers")
def xsum(numbers):
    return sum(numbers)

@task(name="call the models")
def callmodels():
    a=Product.objects.all()
    # all_bidders = Bidder.objects.all()
    len_a=len(a)
    b=[]
    c=[]
    cr_date=str(datetime.datetime.now())
    # current_date=str("%04d%02d-%02d %02d:%02d:%02d" %(cr_date.year,cr_date.month,cr_date.day,cr_date.hour,cr_date.minute,cr_date.second))
    # len_b=len(all_bidders)
    # bidder_id_list = []
    # bidder_bid_amount = []
    for ind in a:

        if cr_date > str(ind.bid_end_date):
            H=1
            try:
                winner_bid = Bidder.objects.filter(product_id=ind.id).last()

                b.append(str(ind.bid_end_date))
                c.append(str(ind.id))

                temp=Product.objects.get(id=ind.id)
                temp.sold=True
                temp.sold_to=str(winner_bid.user_name)
                temp.sold_amount=winner_bid.bid_amount
                temp.save()

            except:
                temp = Product.objects.get(id=ind.id)
                temp.bid_end_date=temp.bid_end_date+datetime.timedelta(minutes = 10)
                temp.save()
            # print("%s-%s-%s" % (ii.year , ii.month , ii.day))
    return print(b),print(cr_date),print(str(ind.bid_end_date))