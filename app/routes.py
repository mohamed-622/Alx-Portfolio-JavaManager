from flask import render_template, request, redirect, url_for, session, flash, current_app as app
from . import db
from .models import User, Order, MenuItem, SizePrice
from sqlalchemy.orm import joinedload



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

@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        
        if not username or not password or not email:
            flash('All three inputs are required.', 'danger')
            return redirect(url_for('new_user'))
        
        # Check if the user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('new_user'))

        # Create a new user
        new_user = User(username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('new_user.html')


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
    
    menu_items = MenuItem.query.options(
        joinedload(MenuItem.sizes)  # Load sizes associated with each menu item
    ).order_by(MenuItem.name).all()

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
    
    # Query the menu item and size/price relationship
    size_price = SizePrice.query.join(MenuItem).filter(
        MenuItem.name == item_name,
        SizePrice.size == size
    ).first()
    
    if not size_price:
        flash('Invalid menu item or size!', 'danger')
        return redirect(url_for('orders'))
    
    # Calculate total price
    total_price = size_price.price * quantity
    
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
        sizes = request.form.getlist('size[]')  # List of sizes
        prices = request.form.getlist('price[]')  # List of corresponding prices

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


@app.route('/menu/modify/<int:item_id>', methods=['GET', 'POST'])
def modify_menu_item(item_id):
    if 'user_id' not in session:
        flash('Please log in to access the menu management page.', 'warning')
        return redirect(url_for('login'))

    item = MenuItem.query.get_or_404(item_id)

    if request.method == 'POST':
        name = request.form.get('name')
        sizes = request.form.getlist('size[]')
        prices = request.form.getlist('price[]')

        if name and sizes and prices and len(sizes) == len(prices):
            item.name = name
            # Remove old sizes and add new ones
            item.sizes = []
            for size, price in zip(sizes, prices):
                item.sizes.append(SizePrice(size=size, price=float(price)))
            db.session.commit()
            flash(f'Menu item "{name}" updated successfully!', 'success')
            return redirect(url_for('menu_management'))
        else:
            flash('Please provide valid input for name, sizes, and prices.', 'danger')

    return render_template('modify_menu_item.html', item=item)


@app.route('/menu/delete/<int:item_id>', methods=['POST'])
def delete_menu_item(item_id):
    if 'user_id' not in session:
        flash('Please log in to access the menu management page.', 'warning')
        return redirect(url_for('login'))

    item = MenuItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash(f'Menu item "{item.name}" deleted successfully!', 'success')
    return redirect(url_for('menu_management'))
