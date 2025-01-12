from flask import render_template, request, redirect, url_for, session, flash, current_app as app
from . import db
from .models import User, Order, MenuItem, SizePrice
from sqlalchemy.orm import joinedload
from datetime import datetime


@app.route('/')
def home():
    # Redirect to the login/orders page if the user is logged in
    return redirect(url_for('login'))

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
            return redirect(url_for('login'))
        
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

    today = datetime.now().date()
    user_orders = Order.query.filter(
        Order.user_id == session['user_id'],
        Order.created_at >= today
    ).order_by(Order.created_at.desc()).limit(10).all()
    
    # Pass indexed current_order to the template
    current_order_with_index = [
        {"index": i, **item} for i, item in enumerate(session.get('current_order', []))
    ]
    
    return render_template(
        'orders.html',
        menu_items=menu_items,
        orders=user_orders,
        current_order=current_order_with_index
    )

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
    
    # Calculate total price for this item
    item_total = size_price.price * quantity
    
    # Initialize 'current_order' in session if it doesn't exist
    if 'current_order' not in session:
        session['current_order'] = []
    
    # Append the new item to the current order
    session['current_order'].append({
        'item_name': item_name,
        'size': size,
        'price': size_price.price,
        'quantity': quantity,
        'item_total': item_total
    })
    session.modified = True
    
    flash(f'Added {quantity} x {item_name} ({size}) to your order!', 'success')
    return redirect(url_for('orders'))

@app.route('/finalize_order', methods=['POST'])
def finalize_order():
    if 'user_id' not in session:
        flash('Please log in to finalize orders!', 'warning')
        return redirect(url_for('login'))
    
    if 'current_order' not in session or not session['current_order']:
        flash('No items to finalize!', 'danger')
        return redirect(url_for('orders'))
    
    # Combine items into a single description
    description = ", ".join(
        f"{item['quantity']} x {item['item_name']} ({item['size']})"
        for item in session['current_order']
    )
    
    # Calculate total price
    total_price = sum(item['item_total'] for item in session['current_order'])
    
    # Save the order
    new_order = Order(
        order_number=f"ORD{int(Order.query.count()) + 1:03}",
        user_id=session['user_id'],
        description=description,
        total_price=total_price
    )
    db.session.add(new_order)
    db.session.commit()
    
    # Clear the current order
    session.pop('current_order', None)
    flash('Order finalized successfully!', 'success')
    return redirect(url_for('orders'))

@app.route('/remove_item', methods=['POST'])
def remove_item():
    if 'current_order' not in session or not session['current_order']:
        flash('No items to remove!', 'danger')
        return redirect(url_for('orders'))
    
    try:
        # Get the index of the item to remove
        item_index = int(request.form['item_index'])
        
        # Remove the item
        removed_item = session['current_order'].pop(item_index)
        session.modified = True  # Mark the session as modified
        
        flash(f"Removed {removed_item['quantity']} x {removed_item['item_name']} ({removed_item['size']}) from the order.", 'success')
    except (IndexError, ValueError):
        flash('Invalid item index!', 'danger')
    
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
