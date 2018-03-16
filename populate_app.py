import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','app.settings')

import django
django.setup()
from studeals.models import Category, Offer, Comment, Vote

def populate():
	food=[
		{"title":"Tesco Two For One on Bread",
		"price":"Two for one",
		"description":"includes fresh loaves, paninis etc.",
		"place_address":"Sauchiehall Street",
		"place_name":"Tesco Metro",
		"expiration_date":"2018-03-25",
		"rating":"4"},
		{"title":"Double Chocolate Cookies",
		"price":"1.00",
		"description":"50p discount on cookies",
		"place_address":"Sauchiehall Street",
		"place_name":"Sainsburry's Local",
		"expiration_date":"2018-03-30",
		"rating":"5"}]
		
	clothes=[
		{"title":"Student Discount on H&M",
		"price":"40% off",
		"description":"Online discount on all items, excluding sales.",
		"place_address":"handm.com",
		"place_name":"H&M",
		"expiration_date":"2018-04-15",
		"rating":"3"},
		{"title":"10% off on shoes at Deichman",
		"price":"10% off",
		"description":"In-store dscounts on all shoes",
		"place_address":"Sauchiehall Street",
		"place_name":"Deichman",
		"expiration_date":"2018-04-15",
		"rating":"3"}]
		
	enterntainment=[
		{"title":"Free entry for students",
		"price":"Free",
		"description":"Free entry for students with Student ID",
		"place_address":"George Square",
		"place_name":"Cocomo",
		"expiration_date":"2020-02-20",
		"rating":"3"},
		{"title":"Open Exhibition",
		"price":"Free",
		"description":"",
		"place_address":"Glasgow School of Art",
		"place_name":"Glasgow School of Art",
		"expiration_date":"2018-03-30",
		"rating":"3"}]
		
		
	cats={"Food": {"offers":food},
		   "Clothes":{"offers":clothes},
		   "Entertainment":{"offers":enterntainment} }
			   
	for cat, cat_data in cats.items():
		c=add_cat(cat)
		for p in cat_data["offers"]:
			add_offer(c,p["title"],p["price"],p["description"],p["place_address"],
			p["place_name"],p["expiration_date"],p["rating"])
			
	for c in Category.objects.all():
		for p in Offer.objects.filter(category=c):
			print("-{0} - {1}".format(str(c), str(p)))
				
def add_offer(cat, title, price, description, place_address, place_name, expiration_date,rating):
	p=Offer.objects.get_or_create(category=cat, title=title, expiration_date=expiration_date)[0]
	p.price=price
	p.description=description
	p.place_address=place_address
	p.place_name=place_name
	
	p.rating=rating
	p.save()
	return p
	
def add_cat(name):
	c= Category.objects.get_or_create(name=name)[0]
	c.save()
	return c
	
if __name__=='__main__':
	print("Starting population script...")
	populate()