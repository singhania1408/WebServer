import os

import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base=declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }



class MenuItem(Base):

	__tablename__= 'menu_item'

	name = Column( 
	String(80),nullable = False)

	id = Column( 
	Integer,primary_key = True) 

	course = Column(String(250))
	description = Column(String(250))
	price = Column(String(8))
	
	restaurant_id = Column(
	Integer, ForeignKey('restaurant.id'))
	
	restaurant = relationship(Restaurant)

	@property
	def serialize(self):
	        """Return object data in easily serializeable format"""
	        return {
	            'name': self.name,
	            'description': self.description,
	            'id': self.id,
	            'price': self.price,
	            'course': self.course,
	        }

class RestaurantNear(Base):
  __tablename__ = 'restaurantnear'
  id = Column(Integer, primary_key = True)
  restaurant_name = Column(String)
  restaurant_address = Column(String)
  restaurant_image = Column(String)
  
  
  #Add a property decorator to serialize information from this database
  @property
  def serialize(self):
    return {
      'restaurant_name': self.restaurant_name,
      'restaurant_address': self.restaurant_address,
      'restaurant_image' : self.restaurant_image,
      'id' : self.id
      
      }	
engine = create_engine('sqlite:///restaurantMenu.db')

Base.metadata.create_all(engine)


