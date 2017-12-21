from flask import Flask , render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

##import CRUD Operations##
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

##Create session and connect do DB##
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#Making an API Endpoint (GET Request)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJson(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItem=[item.serialize for item in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJson(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one();
    return jsonify(MenuItem=menuItem.serialize)

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):

    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)

#Create route for newMenuItem 

@app.route('/restaurants/<int:restaurant_id>/new/' , methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], price=request.form['price'], description=request.form['description'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

#Create route for editMenuItem

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):

    oldItem = session.query(MenuItem).filter_by(id=menu_id).one();

    if request.method == 'POST':        
        if request.form['name']:
            oldItem.name=request.form['name']
        if request.form['price']:
            oldItem.price = request.form['price']
        if request.form['description']:
            oldItem.description = request.form['description']
        session.add(oldItem)
        session.commit()
        flash("menu item updated!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item = oldItem)

#Create a route for deleteMenuItem 

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/' , methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    
    item = session.query(MenuItem).filter_by(id=menu_id).one();

    if request.method == 'POST':        
        session.delete(item)
        session.commit()
        flash("menu item deleted!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item = item)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run (host = '0.0.0.0', port = 5000)