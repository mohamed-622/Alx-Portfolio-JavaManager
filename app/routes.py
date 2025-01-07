from flask import render_template, request, redirect, url_for, session, flash, current_app as app
from . import db
from .models import User, Order, MenuItem, SizePrice


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        
        if user:
            session['user_id'] = user.id
            flash('Logged in successfully!', 'success')
            return redirect(url_for('orders'))
        else:
            flash('Invalid username or password!', 'danger')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))


@app.route('/orders', methods=['GET'])
def orders():
    if 'user_id' not in session:
        flash('Please log in to view orders!', 'warning')
        return redirect(url_for('login'))
    
    # Query menu items and user orders
    menu_items = MenuItem.query.order_by(MenuItem.name, MenuItem.size).all()
    user_orders = Order.query.filter_by(user_id=session['user_id']).all()
    
    return render_template('orders.html', menu_items=menu_items, orders=user_orders)


@app.route('/create_order', methods=['POST'])
def create_order():
    if 'user_id' not in session:
        flash('Please log in to create orders!', 'warning')
        return redirect(url_for('login'))
    
    # Extract order details from the form
    item_name = request.form['item_name']
    size = request.form['size']
    quantity = int(request.form['quantity'])
    
    # Query the price from the menu
    menu_item = MenuItem.query.filter_by(name=item_name, size=size).first()
    if not menu_item:
        flash('Invalid menu item!', 'danger')
        return redirect(url_for('orders'))
    
    # Calculate total price
    total_price = menu_item.price * quantity
    
    # Create the order
    new_order = Order(
        order_number=f"ORD{int(Order.query.count()) + 1:03}",
        user_id=session['user_id'],
        description=f"{quantity} x {item_name} ({size})",
        total_price=total_price
    )
    db.session.add(new_order)
    db.session.commit()
    
    flash('Order added successfully!', 'success')
    return redirect(url_for('orders'))


@app.route('/order_history', methods=['GET'])
def order_history():
    if 'user_id' not in session:
        flash('Please log in to view order history!', 'warning')
        return redirect(url_for('login'))

    # Fetch user-specific orders sorted by date
    user_orders = Order.query.filter_by(user_id=session['user_id']).order_by(Order.created_at.desc()).all()

    return render_template('order_history.html', orders=user_orders)

@app.route('/menu', methods=['GET', 'POST'])
def menu_management():
    if 'user_id' not in session:
        flash('Please log in to access the menu management page.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Add a new menu item
        name = request.form.get('name')
        sizes = request.form.getlist('size')  # List of sizes
        prices = request.form.getlist('price')  # List of corresponding prices

        if name and sizes and prices and len(sizes) == len(prices):
            new_item = MenuItem(name=name)
            for size, price in zip(sizes, prices):
                new_item.sizes.append(SizePrice(size=size, price=float(price)))
            db.session.add(new_item)
            db.session.commit()
            flash(f'Menu item "{name}" added successfully!', 'success')
        else:
            flash('Please provide valid input for name, sizes, and prices.', 'danger')

    menu_items = MenuItem.query.all()
    return render_template('menu.html', menu_items=menu_items)
