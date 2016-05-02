from flask import Flask,render_template,request,url_for,redirect,flash,jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, RestaurantNear
from findARestaurant import findARestaurant

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


# ADD JSON ENDPOINT HERE
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)

@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('basic.html',restaurant=restaurant,items=items)

@app.route('/')
@app.route('/restaurants')
def restaurants():
    restaurant = session.query(Restaurant)
    return render_template('restaurantBasic.html',restaurants=restaurant)

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/near')
def restaurantsNear():
    restaurant = session.query(RestaurantNear)
    return render_template('Restaurantnear.html',restaurants=restaurant)


@app.route('/restaurants/new', methods=['GET', 'POST'])
def restaurantNew():
    if request.method == 'POST':
        newRestaurant=Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        flash("New Restaurant Added")
        return redirect(url_for('restaurants'))
    else:
        return render_template('newRestaurant.html')

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(
            name=request.form['name'],description=request.form[
                           'description'], price=request.form['price'], course=request.form['course'],restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("New Menu Item Added")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

# Task 2: Create route for editMenuItem function here


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()        
        flash("Menu Item Edited")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)

@app.route('/restaurants/<int:restaurant_id>/edit',
           methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    editedItem = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()        
        flash("Restaurant Item Edited")
        return redirect(url_for('restaurants'))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template(
            'editRestaurant.html', restaurant=editedItem)

# Task 3: Create a route for deleteMenuItem function here


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/',methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deletedItem=session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
    	session.delete(deletedItem)
    	session.commit()
    	flash("Menu Item Edited")    	
    	return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
    	return render_template(
    		'deletemenuitem.html', item=deletedItem)
  		
@app.route('/restaurants/<int:restaurant_id>/delete/',methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    deletedItem=session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
    	session.delete(deletedItem)
    	session.commit()
    	flash("Menu Item Edited")    	
    	return redirect(url_for('restaurants'))
    else:
    	return render_template(
    		'deleteRestaurant.html', restaurant=deletedItem)
@app.route('/restaurants/near/new', methods = ['GET', 'POST'])
def allRestaurant():
  if request.method == 'GET':
  	# RETURN ALL RESTAURANTS IN DATABASE
        return render_template('enterDetails.html')

  elif request.method == 'POST':
  	# MAKE A NEW RESTAURANT AND STORE IT IN DATABASE
    location = request.form['city']+", "+request.form['country']
    mealType = request.form['mealType']
    restaurant_info = findARestaurant(mealType, location)
    if restaurant_info != "No Restaurants Found":
      restaurant = RestaurantNear(restaurant_name = unicode(restaurant_info['name']), restaurant_address = unicode(restaurant_info['address']), restaurant_image = restaurant_info['image'])
      session.add(restaurant)
      session.commit() 
      return redirect(url_for('restaurantsNear'))
    else:
      return jsonify({"error":"No Restaurants Found for %s in %s" % (mealType, location)})
if __name__ == '__main__':
    app.secret_key='super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)