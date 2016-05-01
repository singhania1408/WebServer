from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
myFirstRestaurant = Restaurant(name = "2nd")
session.add(myFirstRestaurant)
myFirstRestaurant = Restaurant(name = "3rd")
session.add(myFirstRestaurant)
myFirstRestaurant = Restaurant(name = "4th")
session.add(myFirstRestaurant)
myFirstRestaurant = Restaurant(name = "5th")
session.add(myFirstRestaurant)
myFirstRestaurant = Restaurant(name = "6th")
session.add(myFirstRestaurant)
session.commit()
cheesepizza = MenuItem(name="Veggie Burger", description = "Made with all natural ingredients and fresh mozzarella", course="Entree", price="$8.99", restaurant=myFirstRestaurant)
session.add(cheesepizza)
session.commit()
firstResult = session.query(Restaurant).first()
items = session.query(MenuItem).all()
for item in items:
    print item.name
restaurants = session.query(Restaurant).all()
for restaurant in restaurants:
    print restaurant.name
veggieBurgers = session.query(MenuItem).filter_by(name= 'Veggie Burger')
for veggieBurger in veggieBurgers:
    print veggieBurger.id
    print veggieBurger.price
    print veggieBurger.restaurant.name
    print "\n"

