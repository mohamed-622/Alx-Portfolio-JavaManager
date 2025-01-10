// Function to filter orders by selected date
function filterOrdersByDate() {
    const selectedDate = document.getElementById('calendar').value;
    const orderElements = document.querySelectorAll('.order-item');

    orderElements.forEach(order => {
        const orderDate = order.getAttribute('data-date');
        
        // Show or hide order based on selected date
        order.style.display = (orderDate === selectedDate || selectedDate === "") ? 'block' : 'none';
    });
}
