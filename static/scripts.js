document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/price')
        .then(response => response.json())
        .then(data => {
            const dealsContainer = document.getElementById('deals-scroll');
            const dotsContainer = document.getElementById('dots');
            data.topdiscount.forEach((deal, index) => {
                // Create deal element
                const dealElement = document.createElement('div');
                dealElement.classList.add('deal');
                dealElement.innerHTML = `
                    <div class="deal-image">
                        <a href="${deal.link}" target="_blank">
                            <img src="static/images/${deal.image}" alt="${deal.name}">
                        </a>
                    </div>
                    <div class="deal-name">
                        <p>${deal.name}</p>
                    </div>
                    <div class="deal-info">
                        <p class="current-price">$${deal.current_price.toFixed(2)}</p>
                        <p class="discount">${deal.discount.toFixed(2)}% off</p>
                        <p class="original-price">$${deal.original_price.toFixed(2)}</p>
                    </div>
                `;
                dealsContainer.appendChild(dealElement);

                // Create dot element
                const dotElement = document.createElement('span');
                dotElement.classList.add('dot');
                dotElement.addEventListener('click', () => {
                    currentSlide(index);
                    resetSlideInterval();
                });
                dotsContainer.appendChild(dotElement);
            });

            // Initialize the first slide
            showSlides(slideIndex);
            // Start automatic slide rotation
            slideInterval = setInterval(() => {
                showSlides(slideIndex += 1);
            }, 3000); // Change slide every 3 seconds
        })
        .catch(error => console.error('Error fetching deals:', error));
});

let slideIndex = 0;
let slideInterval;

function showSlides(n) {
    const slides = document.getElementsByClassName('deal');
    const dots = document.getElementsByClassName('dot');
    if (n >= slides.length) { slideIndex = 0 }
    if (n < 0) { slideIndex = slides.length - 1 }
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = 'none';
    }
    for (let i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(' active', '');
    }
    slides[slideIndex].style.display = 'block';
    dots[slideIndex].className += ' active';
}

function currentSlide(n) {
    showSlides(slideIndex = n);
}

function resetSlideInterval() {
    clearInterval(slideInterval);
    slideInterval = setInterval(() => {
        showSlides(slideIndex += 1);
    }, 5000); // Change slide every 5 seconds after manual click
}