let selectedMeals = [];

function addMeal(name, price) {
    selectedMeals.push({ name, price });
    alert(`${name} added to your order.`);
    updateCheckout();
}

function updateCheckout() {
    const checkoutSection = document.getElementById('checkout-section');
    const selectedMealsList = document.getElementById('selected-meals');
    const totalPriceElement = document.getElementById('total-price');

    if (selectedMeals.length > 0) {
        checkoutSection.style.display = 'block';
        selectedMealsList.innerHTML = '';
        let total = 0;

        selectedMeals.forEach(meal => {
            const li = document.createElement('li');
            li.textContent = `${meal.name} - ${meal.price} KES`;
            selectedMealsList.appendChild(li);
            total += meal.price;
        });

        totalPriceElement.textContent = total;
    } else {
        checkoutSection.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    updateCheckout();
});

document.getElementById('checkout-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const paymentMethod = document.getElementById('payment-method').value;
    const deliveryLocation = document.getElementById('location').value;
    const phoneNumber = document.getElementById('phone').value;

    let orderSummary = 'Order Summary:\n';
    selectedMeals.forEach(meal => {
        orderSummary += `${meal.name} - ${meal.price} KES\n`;
    });

    const totalAmount = selectedMeals.reduce((total, meal) => total + meal.price, 0);
    orderSummary += `Total Amount: ${totalAmount} KES\n`;
    orderSummary += `Payment Method: ${paymentMethod}\n`;
    orderSummary += `Delivery Location: ${deliveryLocation}\n`;
    orderSummary += `Phone Number: ${phoneNumber}\n`;

    alert(orderSummary);
});
