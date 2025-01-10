// This function adds a new size and price input group when the button is clicked
document.getElementById('add-size-price').addEventListener('click', function() {
    const container = document.getElementById('size-price-container');
    const newInputGroup = document.createElement('div');
    newInputGroup.innerHTML = `
        <input type="text" name="size[]" placeholder="Size (e.g., 30 cl)" required>
        <input type="number" step="0.01" name="price[]" placeholder="Price (e.g., 5.00)" required>
    `;
    container.appendChild(newInputGroup);
});
