// Shop functionality with API integration
let cart = [];
let allProducts = [];
let filteredProducts = [];
let currentPage = 1;
const productsPerPage = 9;

document.addEventListener('DOMContentLoaded', function() {
    initShop();
    loadCart();
    setupEventListeners();
});

// Function initShop
async function initShop() {
    await fetchProducts();
    
    // Load page from URL query parameter if it exists
    const urlParams = new URLSearchParams(window.location.search);
    const pageParam = urlParams.get('page');
    if (pageParam) {
        currentPage = parseInt(pageParam, 10);
        const totalPages = Math.ceil(filteredProducts.length / productsPerPage);
        if (currentPage < 1 || currentPage > totalPages) {
            currentPage = 1;
        }
    }
    
    renderProducts();
    updateProductCount();
    setCurrentYear();
}

// Fetch products from API
async function fetchProducts() {
    try {
        // Fetch all products with a large per_page to avoid pagination limits
        const response = await fetch('/api/products?per_page=100');
        const data = await response.json();
        
        if (data.status === 'success') {
            allProducts = data.products;
            filteredProducts = [...allProducts];
        } else {
            console.error('Failed to fetch products:', data.message);
            // Fallback to static data if API fails
            allProducts = SHOP_PRODUCTS || [];
            filteredProducts = [...allProducts];
        }
    } catch (error) {
        console.error('Error fetching products:', error);
        // Fallback to static data if API fails
        allProducts = SHOP_PRODUCTS || [];
        filteredProducts = [...allProducts];
    }
}

function setupEventListeners() {
    // Category filters
    document.getElementById('catAll').addEventListener('change', handleAllCategoriesFilter);
    document.querySelectorAll('.category-filter').forEach(filter => {
        filter.addEventListener('change', handleCategoryFilter);
    });

    // Price filters
    document.querySelectorAll('.price-filter').forEach(filter => {
        filter.addEventListener('change', handlePriceFilter);
    });

    // Sort
    document.getElementById('sortBy').addEventListener('change', handleSort);

    // Clear filters
    document.getElementById('clearFilters').addEventListener('click', clearFilters);

    // View toggles
    document.getElementById('gridView').addEventListener('click', () => toggleView('grid'));
    document.getElementById('listView').addEventListener('click', () => toggleView('list'));

    // Checkout button
    document.getElementById('checkoutBtn').addEventListener('click', handleCheckout);
}

function handleAllCategoriesFilter(e) {
    const categoryFilters = document.querySelectorAll('.category-filter');
    if (e.target.checked) {
        categoryFilters.forEach(filter => filter.checked = false);
    }
    applyFilters();
}

function handleCategoryFilter() {
    const allFilter = document.getElementById('catAll');
    const anyChecked = Array.from(document.querySelectorAll('.category-filter')).some(f => f.checked);
    if (anyChecked) {
        allFilter.checked = false;
    } else {
        allFilter.checked = true;
    }
    applyFilters();
}

function handlePriceFilter() {
    applyFilters();
}

function handleSort() {
    const sortValue = document.getElementById('sortBy').value;
    
    switch(sortValue) {
        case 'price-low':
            filteredProducts.sort((a, b) => a.price - b.price);
            break;
        case 'price-high':
            filteredProducts.sort((a, b) => b.price - a.price);
            break;
        case 'name':
            filteredProducts.sort((a, b) => a.name.localeCompare(b.name));
            break;
        default:
            filteredProducts = [...allProducts];
    }
    
    renderProducts();
}

function applyFilters() {
    let products = [...allProducts];
    
    // Category filter
    const allCategories = document.getElementById('catAll').checked;
    if (!allCategories) {
        const selectedCategories = Array.from(document.querySelectorAll('.category-filter:checked'))
            .map(f => f.value);
        
        if (selectedCategories.length > 0) {
            products = products.filter(p => {
                // Handle both slug and category_id
                const categorySlug = p.category?.slug || p.category;
                return selectedCategories.includes(categorySlug);
            });
        }
    }
    
    // Price filter
    const selectedPrices = Array.from(document.querySelectorAll('.price-filter:checked'))
        .map(f => f.value);
    
    if (selectedPrices.length > 0) {
        products = products.filter(product => {
            return selectedPrices.some(range => {
                const [min, max] = range.split('-').map(Number);
                return product.price >= min && product.price <= max;
            });
        });
    }
    
    filteredProducts = products;
    currentPage = 1;
    renderProducts();
    updateProductCount();
}

function clearFilters() {
    document.getElementById('catAll').checked = true;
    document.querySelectorAll('.category-filter').forEach(f => f.checked = false);
    document.querySelectorAll('.price-filter').forEach(f => f.checked = false);
    document.getElementById('sortBy').value = 'featured';
    
    filteredProducts = [...allProducts];
    currentPage = 1;
    renderProducts();
    updateProductCount();
    
    // Reset URL to remove page parameter
    window.history.pushState({ page: 1 }, '', window.location.pathname);
}

// Function renderProducts
function renderProducts() {
    const container = document.getElementById('productsContainer');
    const start = (currentPage - 1) * productsPerPage;
    const end = start + productsPerPage;
    const productsToShow = filteredProducts.slice(start, end);
    
    container.innerHTML = '';
    
    if (productsToShow.length === 0) {
        container.innerHTML = `
            <div class="col-12 text-center py-5">
                <i class="bi bi-inbox fs-1 text-muted d-block mb-3"></i>
                <p class="text-muted">No products found matching your criteria.</p>
                <button class="btn btn-primary" onclick="clearFilters()">Clear Filters</button>
            </div>
        `;
        return;
    }
    
    productsToShow.forEach(product => {
        const col = document.createElement('div');
        col.className = 'col-md-6 col-lg-4';
        
        // Get product image - use main_image from API with placeholder fallback
        const productImage = product.main_image;
        const inStock = product.stock_quantity > 0 || product.inStock !== false;
        const rating = product.average_rating || product.rating || 0;
        const reviews = product.review_count || product.reviews || 0;
        const categoryName = product.category?.name || getCategoryName(product.category);
        
        // Use placeholder if main_image is not available
        const imageUrl = productImage || '/static/images/default-product.svg';
        
        const imageHtml = `
                <div class="position-relative">
                    <img src="${imageUrl}" class="card-img-top" alt="${product.name}" style="height: 250px; object-fit: cover;">
                    ${!inStock ? '<span class="badge bg-danger position-absolute top-0 end-0 m-2">Out of Stock</span>' : ''}
                    ${product.is_featured ? '<span class="badge bg-warning position-absolute top-0 start-0 m-2">Featured</span>' : ''}
                    <div class="product-overlay position-absolute top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center">
                        <button class="btn btn-light btn-sm me-2" onclick="quickView(${product.id})">
                            <i class="bi bi-eye"></i> Quick View
                        </button>
                    </div>
                </div>`;

        col.innerHTML = `
            <div class="card h-100 border-0 shadow-sm product-card">
                ${imageHtml}
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <h5 class="card-title h6 mb-0">${product.name}</h5>
                        <span class="badge bg-light text-dark">${categoryName}</span>
                    </div>
                    <div class="mb-2">
                        ${renderStars(rating)}
                        <small class="text-muted">(${reviews})</small>
                    </div>
                    <p class="card-text text-muted small">${(product.short_description || product.description || '').substring(0, 80)}...</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <span class="h5 mb-0 text-amber">$${parseFloat(product.price).toFixed(2)}</span>
                        <button class="btn btn-primary btn-sm" onclick="addToCart(${product.id})" ${!inStock ? 'disabled' : ''}>
                            <i class="bi bi-cart-plus"></i> Add to Cart
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        container.appendChild(col);
    });
    
    renderPagination();
}

function renderPagination() {
    const totalPages = Math.ceil(filteredProducts.length / productsPerPage);
    const pagination = document.getElementById('pagination');
    
    if (totalPages <= 1) {
        pagination.innerHTML = '';
        return;
    }
    
    let html = '';
    
    // Previous button
    html += `
        <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
            <a class="page-link" href="#" onclick="changePage(${currentPage - 1}); return false;">Previous</a>
        </li>
    `;
    
    // Page numbers
    for (let i = 1; i <= totalPages; i++) {
        if (i === 1 || i === totalPages || (i >= currentPage - 1 && i <= currentPage + 1)) {
            html += `
                <li class="page-item ${i === currentPage ? 'active' : ''}">
                    <a class="page-link" href="#" onclick="changePage(${i}); return false;">${i}</a>
                </li>
            `;
        } else if (i === currentPage - 2 || i === currentPage + 2) {
            html += '<li class="page-item disabled"><span class="page-link">...</span></li>';
        }
    }
    
    // Next button
    html += `
        <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
            <a class="page-link" href="#" onclick="changePage(${currentPage + 1}); return false;">Next</a>
        </li>
    `;
    
    pagination.innerHTML = html;
}

function changePage(page) {
    const totalPages = Math.ceil(filteredProducts.length / productsPerPage);
    if (page < 1 || page > totalPages) return;
    
    currentPage = page;
    renderProducts();
    
    // Update URL with current page number
    const newUrl = `${window.location.pathname}?page=${page}`;
    window.history.pushState({ page: page }, '', newUrl);
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function renderStars(rating) {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    let html = '';
    
    for (let i = 0; i < fullStars; i++) {
        html += '<i class="bi bi-star-fill text-warning"></i>';
    }
    
    if (hasHalfStar) {
        html += '<i class="bi bi-star-half text-warning"></i>';
    }
    
    const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
    for (let i = 0; i < emptyStars; i++) {
        html += '<i class="bi bi-star text-warning"></i>';
    }
    
    return html;
}

function getCategoryName(category) {
    if (typeof category === 'object' && category.name) {
        return category.name;
    }
    
    const names = {
        'guest-room': 'Guest Room',
        'lobby': 'Lobby',
        'restaurant': 'Restaurant',
        'outdoor': 'Outdoor'
    };
    return names[category] || category;
}

function addToCart(productId) {
    const product = allProducts.find(p => p.id === productId);
    if (!product) return;
    
    const inStock = product.stock_quantity > 0 || product.inStock !== false;
    if (!inStock) return;
    
    const existingItem = cart.find(item => item.id === productId);
    
    if (existingItem) {
        existingItem.quantity++;
    } else {
        cart.push({
            id: product.id,
            name: product.name,
            price: parseFloat(product.price),
            image: product.main_image,
            quantity: 1
        });
    }
    
    saveCart();
    updateCartUI();
    
    // Show toast notification
    showToast(`${product.name} added to cart!`);
}

function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    saveCart();
    updateCartUI();
}

function updateQuantity(productId, change) {
    const item = cart.find(item => item.id === productId);
    if (!item) return;
    
    item.quantity += change;
    
    if (item.quantity <= 0) {
        removeFromCart(productId);
    } else {
        saveCart();
        updateCartUI();
    }
}

// Function updateCartUI with null check for checkoutBtn
function updateCartUI() {
    const cartCount = document.getElementById('cartCount');
    const cartItems = document.getElementById('cartItems');
    const cartTotal = document.getElementById('cartTotal');
    const checkoutBtn = document.getElementById('checkoutBtn'); // This might be null on shop page
    
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    const totalPrice = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    
    // Update cart count and total (these should exist)
    if (cartCount) cartCount.textContent = totalItems;
    if (cartTotal) cartTotal.textContent = `$${totalPrice.toFixed(2)}`;
    
    // Handle cart items
    if (cartItems) {
        if (cart.length === 0) {
            cartItems.innerHTML = `
                <div class="text-center text-muted py-5">
                    <i class="bi bi-cart3 fs-1 d-block mb-3"></i>
                    <p>Your cart is empty</p>
                </div>
            `;
        } else {
            let html = '';
            cart.forEach(item => {
                const imageHtml = item.image ? `<img src="${item.image}" alt="${item.name}" style="width: 80px; height: 80px; object-fit: cover;" class="rounded">` : `<div style="width: 80px; height: 80px;" class="bg-light rounded d-flex align-items-center justify-content-center"><i class="bi bi-image text-muted"></i></div>`;
                html += `
                    <div class="cart-item border-bottom pb-3 mb-3">
                        <div class="d-flex gap-3">
                            ${imageHtml}
                            <div class="flex-grow-1">
                                <h6 class="mb-1">${item.name}</h6>
                                <p class="text-muted small mb-2">$${item.price.toFixed(2)}</p>
                                <div class="d-flex align-items-center gap-2">
                                    <button class="btn btn-sm btn-outline-secondary" onclick="updateQuantity(${item.id}, -1)">-</button>
                                    <span>${item.quantity}</span>
                                    <button class="btn btn-sm btn-outline-secondary" onclick="updateQuantity(${item.id}, 1)">+</button>
                                    <button class="btn btn-sm btn-outline-danger ms-auto" onclick="removeFromCart(${item.id})">
                                        <i class="bi bi-trash"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            });
            cartItems.innerHTML = html;
        }
    }
    
    // Only disable/enable checkoutBtn if it exists (checkout functionality might not be on shop page)
    if (checkoutBtn) {
        checkoutBtn.disabled = cart.length === 0;
    }
}

async function quickView(productId) {
    try {
        const response = await fetch(`/api/products/${productId}`);
        const data = await response.json();
        
        if (data.status !== 'success') {
            console.error('Failed to fetch product details');
            return;
        }
        
        const product = data.product;
        
        // Get product image from main_image with placeholder fallback
        const productImage = product.main_image;
        const imageUrl = productImage || '/static/images/default-product.svg';
        
        const inStock = product.stock_quantity > 0 || product.inStock !== false;
        const rating = product.average_rating || product.rating || 0;
        const reviews = product.review_count || product.reviews || 0;
        const categoryName = product.category?.name || getCategoryName(product.category);
        const features = product.features || [];
        
        const imageHtml = `
                <div class="col-md-6">
                    <img src="${imageUrl}" alt="${product.name}" class="img-fluid rounded">
                </div>`;

        const detailsColClass = 'col-md-6';

        const modalContent = document.getElementById('quickViewContent');
        modalContent.innerHTML = `
            <div class="row g-4">
                ${imageHtml}
                <div class="${detailsColClass}">
                    <span class="badge bg-light text-dark mb-2">${categoryName}</span>
                    <h3 class="mb-3">${product.name}</h3>
                    <div class="mb-3">
                        ${renderStars(rating)}
                        <span class="text-muted ms-2">(${reviews} reviews)</span>
                    </div>
                    <h4 class="text-amber mb-3">$${parseFloat(product.price).toFixed(2)}</h4>
                    <p class="mb-4">${product.description || product.short_description || ''}</p>
                    ${features.length > 0 ? `
                        <h6 class="fw-bold mb-2">Features:</h6>
                        <ul class="mb-4">
                            ${features.map(f => `<li>${f}</li>`).join('')}
                        </ul>
                    ` : ''}
                    <div class="d-flex gap-2">
                        <button class="btn btn-primary flex-grow-1" onclick="addToCart(${product.id}); bootstrap.Modal.getInstance(document.getElementById('quickViewModal')).hide();" ${!inStock ? 'disabled' : ''}>
                            <i class="bi bi-cart-plus"></i> Add to Cart
                        </button>
                        ${!inStock ? '<span class="badge bg-danger align-self-center">Out of Stock</span>' : ''}
                    </div>
                </div>
            </div>
        `;
        
        const modal = new bootstrap.Modal(document.getElementById('quickViewModal'));
        modal.show();
    } catch (error) {
        console.error('Error fetching product details:', error);
    }
}

function toggleView(view) {
    const gridBtn = document.getElementById('gridView');
    const listBtn = document.getElementById('listView');
    const container = document.getElementById('productsContainer');
    
    if (view === 'grid') {
        gridBtn.classList.add('active');
        listBtn.classList.remove('active');
        container.className = 'row g-4';
    } else {
        listBtn.classList.add('active');
        gridBtn.classList.remove('active');
        container.className = 'row g-3';
    }
}

function handleCheckout() {
    // Check if user is logged in
    // This would need to be implemented with proper authentication check
    alert('Checkout functionality will be implemented with backend integration.\n\nTotal: $' + 
          cart.reduce((sum, item) => sum + (item.price * item.quantity), 0).toFixed(2) +
          '\n\nPlease log in to complete your purchase.');
}

function saveCart() {
    localStorage.setItem('hotelFurnitureCart', JSON.stringify(cart));
}

function loadCart() {
    const saved = localStorage.getItem('hotelFurnitureCart');
    if (saved) {
        cart = JSON.parse(saved);
        updateCartUI();
    }
}

function updateProductCount() {
    const countElement = document.getElementById('productCount');
    if (countElement) {
        countElement.textContent = filteredProducts.length;
    }
}

function setCurrentYear() {
    const yearElement = document.getElementById('currentYear');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }
}

function showToast(message) {
    // Simple toast notification
    const toast = document.createElement('div');
    toast.className = 'position-fixed bottom-0 end-0 p-3';
    toast.style.zIndex = '9999';
    toast.innerHTML = `
        <div class="toast show" role="alert">
            <div class="toast-header">
                <i class="bi bi-check-circle-fill text-success me-2"></i>
                <strong class="me-auto">Success</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">${message}</div>
        </div>
    `;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}