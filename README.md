# Online Shop

### Table of Contents
- [Description](#description)
- [Features](#features)
- [Installing](#installing)
***
## Description
Django project that consists of a fully featured online shop. With essential functionalities of an e-commerce platform.
This online shop will enable clients to browse products, add them to the cart, 
apply discount codes, go through the checkout process, pay with a credit card, and obtain an invoice.
It also implement a recommendation engine to recommend products to your customers,
and you will use internationalization to offer your site in multiple languages.
***
## Features
* Product catalog, shopping cart(using sessions), custom context processors.
* Celery with RabbitMQ as a massage broker, and monitoring with Flower.
* Integrated a payment system with Braintree.
* Exporting orders to CSV files and PDF(WeasyPrint) invoce feat.
* Custom views for the administration site.
* Coupon system to apply discounts.
* Product recommendation engine(redis).
***
## Installing

Clone the project:
```
git clone https://github.com/davkdev620/online_shop.git
```

Install the requirements.txt file:
```
pip install -r requirements.txt
```

Make migration:
```
python manage.py makemigrations
python manage.py migrate
```

Crate super user:
```
python manage.py createsuperuser
```

Add some products.


To run the app on local host: 
```
python manage.py runserver
```

To get mails with orders and voice set your email data at:
- orders/tasks.py -> mail_sent(line 14)
- payment/tasks.py -> email(line 18)
- settings.py -> Email settings

Create a new account at Braintree:
- https://www.braintreepayments.com/sandbox 
- Set the Merchant ID, Public Key and Private key at settings.py

Installing and run RabbitMQ(for deb like system):
```
apt install rabbitmq
rabbitmq-server
```
Open CLI:
```
sudo apt install rabbitmq-server
sudo systemctl enable rabbitmq-server 
sudo systemctl start  rabbitmq-server
systemctl status  rabbitmq-server
```
Then open another shell and start the Celery worker from your project directory, using
the following command:
```
celery -A online_shop worker -l info
```

To run Flower:
```
celery -A online_shop flower
```
- http://localhost:5555/dashboard
- https://flower.readthedocs.io/

<br>

__For production use, before publish the project, change the SECRET_KEY. It’s recommended to set it as local variable!__ 
