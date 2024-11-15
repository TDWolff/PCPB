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

    const form = document.getElementById('pc-parts-form');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const cpu = document.getElementById('cpu').value;
        const gpu = document.getElementById('gpu').value;

        const pcParts = {
            cpu: cpu,
            cpuBrand: getBrand(cpu, ['Intel', 'AMD']),
            gpu: gpu,
            gpuBrand: getBrand(gpu, ['NVIDIA', 'AMD']),
            psu: document.getElementById('psu').value,
            motherboard: document.getElementById('motherboard').value,
            ram: document.getElementById('ram').value,
            storage: document.getElementById('storage').value,
            case: document.getElementById('case').value,
            fans: document.getElementById('fans').value,
            cpuCooler: document.getElementById('cpu-cooler').value
        };

        localStorage.setItem('pcParts', JSON.stringify(pcParts));
        alert('PC parts saved successfully!');
    });

    // Load saved parts if available
    const savedParts = JSON.parse(localStorage.getItem('pcParts'));
    if (savedParts) {
        document.getElementById('cpu').value = savedParts.cpu || '';
        document.getElementById('gpu').value = savedParts.gpu || '';
        document.getElementById('psu').value = savedParts.psu || '';
        document.getElementById('motherboard').value = savedParts.motherboard || '';
        document.getElementById('ram').value = savedParts.ram || '';
        document.getElementById('storage').value = savedParts.storage || '';
        document.getElementById('case').value = savedParts.case || '';
        document.getElementById('fans').value = savedParts.fans || '';
        document.getElementById('cpu-cooler').value = savedParts.cpuCooler || '';
    }

    // Fetch parts data for autocomplete
    fetch('/api/parts')
        .then(response => response.json())
        .then(partsDict => {
            // Enable autocomplete for form fields based on part type
            $("#cpu").autocomplete({ source: partsDict.CPU });
            $("#gpu").autocomplete({ source: partsDict.GPU });
            $("#psu").autocomplete({ source: partsDict.PSU });
            $("#motherboard").autocomplete({ source: partsDict.Motherboard });
            $("#ram").autocomplete({ source: partsDict.RAM });
            $("#storage").autocomplete({ source: partsDict.Storage });
            $("#case").autocomplete({ source: partsDict.Case });
            $("#fans").autocomplete({ source: partsDict.Fans });
            $("#cpu-cooler").autocomplete({ source: partsDict["CPU Cooler"] });
        })
        .catch(error => console.error('Error fetching parts:', error));
});

function getBrand(partName, brands) {
    for (const brand of brands) {
        if (partName.toLowerCase().includes(brand.toLowerCase())) {
            return brand;
        }
    }
    return 'Unknown';
}

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