import os
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm1.settings')
from datetime import date
import django
django.setup()


import random
from accounts.models import Customer, Product, Order, Tag
from faker import Faker

fakegen = Faker()
def add_tag():
    t = ['Kitchen', 'Sports', 'Summer']
    tag = Tag.objects.get_or_create(name = random.choice(t))[0]
    tag.save()
    return tag


def populate():
    p = ['Vaccum Cleaner', 'Laptop', 'Radio', 'Bag', 'Spoon', 'Cupboard', 'Bulp',
            'Fish Tank', 'Gloves', 'Pot', 'Shoes', 'Slipper', 'Belt', 'Charger', 'Chips', 'Broom']
    c = ['Indoor', 'Outdoor']
    s = ['Pending', 'Delivered']

    tag = add_tag()


    fake_phone = random.randint(2222222222, 9999999999)
    fake_email = fakegen.email()
    fake_name = fakegen.name()
    # fake_date = Customer.objects.get_or_create(date_created = fakegen.date())[0]
    # fake_date = datetime.strptime(fake_date, '%Y-%m-%d').date()
    fake_pro_name = random.choice(p)
    stat = random.choice(s)
    fake_price = random.randint(100, 7000)
    cat = random.choice(c)
    fake_date = date.today()

    cus = Customer.objects.get_or_create(name = fake_name, phone = fake_phone, email = fake_email, date_created = fake_date)[0]


    pro = Product.objects.get_or_create(name = fake_pro_name, price = fake_price, category = cat, date_created = fake_date)[0]

    pro.settag(tag)

    ord = Order.objects.get_or_create(customer = cus, product = pro, status = stat, date_created = fake_date)[0]

if __name__ == '__main__':
    print("populating script")
    for i in range(21):
        populate()
    print("populating complete")
