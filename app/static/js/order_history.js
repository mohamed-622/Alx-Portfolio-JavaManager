// Function to filter orders by selected date
function filterOrdersByDate() {
    const selectedDate = document.getElementById('calendar').value;
    console.log("Selected Date:", selectedDate); // Log the selected date

    const orderElements = document.querySelectorAll('.order-item');
    console.log("Order Elements:", orderElements); // Log all orders for debugging

    orderElements.forEach(order => {
        const orderDate = order.getAttribute('data-date');
        console.log("Order Date:", orderDate); // Log each order's date

        // Compare the selected date with the order date
        if (orderDate === selectedDate) {
            console.log("Showing order:", order); // Log visible orders
            order.style.display = 'block';
        } else {
            console.log("Hiding order:", order); // Log hidden orders
            order.style.display = 'none';
        }
    });
}
