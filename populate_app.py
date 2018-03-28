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
		"place_address":"236 Sauchiehall St, Glasgow G2 3HQ, UK",
		"place_name":"Tesco Metro",
		"expiration_date":"2018-03-25",
		"place_latitude": "55.8653348",
		"place_longitude": "-4.260937699999999"},
		{"title":"Double Chocolate Cookies",
		"price":"1.00",
		"description":"50p discount on cookies",
		"place_address":"219 Sauchiehall St, Glasgow G2 3EX, UK",
		"place_name":"Sainsbury's Local",
		"expiration_date":"2018-03-30",
		"place_latitude": "55.8650288",
		"place_longitude": "-4.2612464"},
		{"title": "Student discount",
		"price":"10% discount",
		"description": "10% discount applied for students",
		"place_address": "1137 Argyle St, Glasgow G3 8ND, UK",
		"place_name":"Roots, Fruits & Flowers Finnieston",
		"expiration_date":"2018-05-10",
		"place_latitude":"55.8647205",
		"place_longitude":"-4.2845401"}]
		
	clothes=[
		{"title":"Student Discount on H&M",
		"price":"40% off",
		"description":"Online discount on all items, excluding sales.",
		"place_address":"185 Buchanan St, Glasgow G1 2JA, UK",
		"place_name":"H&M",
		"expiration_date":"2018-04-15",
		"place_latitude": "55.8628432",
		"place_longitude": "-4.2526502"},
		{"title":"10% off on shoes at Deichman",
		"price":"10% off",
		"description":"In-store dscounts on all shoes",
		"place_address":"250 - 252 Sauchiehall Street, Glasgow G2 3EQ, United Kingdom",
		"place_name":"Deichmann",
		"expiration_date":"2018-04-15",
		"place_latitude": "55.865334",
		"place_longitude": "-4.261337999999999"}]
		
	enterntainment=[
		{"title":"Free entry for students",
		"price":"Free",
		"description":"Free entry for students with Student ID",
		"place_address":"51 W Regent St, Glasgow G2 2AE, UK",
		"place_name":"Cocomo",
		"expiration_date":"2020-02-20",
		"place_latitude": "55.862933",
		"place_longitude": "-4.2566535"},
		{"title":"Open Exhibition",
		"price":"Free",
		"description":"",
		"place_address":"167 Renfrew St, Glasgow G3 6RQ, UK",
		"place_name":"Glasgow School of Art",
		"expiration_date":"2018-03-30",
		"place_latitude": "55.866147",
		"place_longitude": "-4.2636933"}]

	restaurants = [
		{
			"title": "Byron Hamburgers for students!",
			"price": "20% discount",
			"description": "You get 20% discount at Byron Hamburgers! Bring your student ID with you!",
			"place_address": "100 W George St, Glasgow G2 1PP, UK",
			"place_name": "Byron Hamburgers",
			"place_latitude": "55.8624103",
			"place_longitude": "-4.255548699999999",
			"expiration_date": "2018-08-15"
		}
	]
		
		
	cats = {
		"Food & Groceries": {"offers":food},
		"Clothing":{"offers":clothes},
		"Entertainment":{"offers":enterntainment},
		"Restaurants & takeaway":{"offers":restaurants},
		"Bars & Pubs":{"offers":[]},
		"Technology":{"offers":[]},
		"Coffeshops":{"offers":[]},
		"Bookshops":{"offers":[]},
		"Office & stationery":{"offers":[]},
		"Fitness & lifestyle":{"offers":[]},
		"Cosmetics & drugstores":{"offers":[]}
	}
			   
	for cat, cat_data in cats.items():
		c=add_cat(cat)
		for p in cat_data["offers"]:
			add_offer(c,p["title"],p["price"],p["description"],p["place_address"],
			p["place_name"],p["expiration_date"],p['place_latitude'],p['place_longitude'])
			
	for c in Category.objects.all():
		for p in Offer.objects.filter(category=c):
			print("-{0} - {1}".format(str(c), str(p)))
				
def add_offer(cat, title, price, description, place_address, place_name, expiration_date,place_latitude=0,place_longitude=0):
	p=Offer.objects.get_or_create(category=cat, title=title, expiration_date=expiration_date)[0]
	p.price=price
	p.description=description
	p.place_address=place_address
	p.place_name=place_name
	p.place_latitude=place_latitude
	p.place_longitude=place_longitude
	
	p.rating=0
	p.save()
	return p
	
def add_cat(name):
	c= Category.objects.get_or_create(name=name)[0]
	c.save()
	return c
	
if __name__=='__main__':
	print("Starting population script...")
	populate()
