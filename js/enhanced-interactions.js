// Enhanced Interactive Features for Bespoke Bags Website

// Advanced Product Filter and Search
class ProductFilter {
    constructor() {
        this.products = [];
        this.filters = {
            category: 'all',
            priceRange: 'all',
            material: 'all',
            color: 'all'
        };
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadProducts();
    }

    bindEvents() {
        // Filter buttons
        document.addEventListener('click', (e) => {
            if (e.target.matches('.filter-btn')) {
                this.handleFilterClick(e.target);
            }
        });

        // Search input
        const searchInput = document.querySelector('#product-search');
        if (searchInput) {
            searchInput.addEventListener('input', debounce((e) => {
                this.handleSearch(e.target.value);
            }, 300));
        }

        // Price range slider
        const priceSlider = document.querySelector('#price-range');
        if (priceSlider) {
            priceSlider.addEventListener('input', (e) => {
                this.handlePriceFilter(e.target.value);
            });
        }
    }

    handleFilterClick(button) {
        const filterType = button.dataset.filter;
        const filterValue = button.dataset.value;
        
        // Update active state
        document.querySelectorAll(`[data-filter="${filterType}"]`).forEach(btn => {
            btn.classList.remove('active');
        });
        button.classList.add('active');
        
        // Update filter
        this.filters[filterType] = filterValue;
        this.applyFilters();
    }

    handleSearch(searchTerm) {
        this.searchTerm = searchTerm.toLowerCase();
        this.applyFilters();
    }

    handlePriceFilter(maxPrice) {
        this.filters.maxPrice = parseInt(maxPrice);
        document.querySelector('#price-display').textContent = `$0 - $${maxPrice}`;
        this.applyFilters();
    }

    applyFilters() {
        const productCards = document.querySelectorAll('.product-card');
        
        productCards.forEach(card => {
            let show = true;
            
            // Category filter
            if (this.filters.category !== 'all') {
                const category = card.dataset.category;
                if (category !== this.filters.category) show = false;
            }
            
            // Material filter
            if (this.filters.material !== 'all') {
                const material = card.dataset.material;
                if (material !== this.filters.material) show = false;
            }
            
            // Search filter
            if (this.searchTerm) {
                const title = card.querySelector('.product-title').textContent.toLowerCase();
                const description = card.querySelector('.product-description').textContent.toLowerCase();
                if (!title.includes(this.searchTerm) && !description.includes(this.searchTerm)) {
                    show = false;
                }
            }
            
            // Price filter
            if (this.filters.maxPrice) {
                const price = parseInt(card.dataset.price);
                if (price > this.filters.maxPrice) show = false;
            }
            
            // Show/hide with animation
            if (show) {
                card.style.display = 'block';
                card.style.opacity = '0';
                setTimeout(() => {
                    card.style.opacity = '1';
                }, 50);
            } else {
                card.style.opacity = '0';
                setTimeout(() => {
                    card.style.display = 'none';
                }, 300);
            }
        });
        
        this.updateResultsCount();
    }

    updateResultsCount() {
        const visibleProducts = document.querySelectorAll('.product-card[style*="block"]').length;
        const resultsCounter = document.querySelector('#results-count');
        if (resultsCounter) {
            resultsCounter.textContent = `${visibleProducts} products found`;
        }
    }

    loadProducts() {
        // This would typically load from an API
        // For now, we'll work with existing DOM elements
        this.updateResultsCount();
    }
}

// Interactive Product Comparison
class ProductComparison {
    constructor() {
        this.compareList = [];
        this.maxCompare = 3;
        this.init();
    }

    init() {
        this.createCompareBar();
        this.bindEvents();
    }

    createCompareBar() {
        const compareBar = document.createElement('div');
        compareBar.className = 'compare-bar';
        compareBar.innerHTML = `
            <div class="compare-content">
                <span class="compare-title">Compare Products (<span id="compare-count">0</span>/${this.maxCompare})</span>
                <div class="compare-items" id="compare-items"></div>
                <button class="btn-compare" id="btn-compare" disabled>Compare Now</button>
                <button class="btn-clear-compare" id="btn-clear-compare">Clear All</button>
            </div>
        `;
        document.body.appendChild(compareBar);
    }

    bindEvents() {
        // Add to compare buttons
        document.addEventListener('click', (e) => {
            if (e.target.matches('.add-to-compare')) {
                this.addToCompare(e.target);
            }
        });

        // Compare button
        document.getElementById('btn-compare').addEventListener('click', () => {
            this.showComparison();
        });

        // Clear compare
        document.getElementById('btn-clear-compare').addEventListener('click', () => {
            this.clearCompare();
        });
    }

    addToCompare(button) {
        const productCard = button.closest('.product-card');
        const productId = productCard.dataset.productId;
        
        if (this.compareList.includes(productId)) {
            this.removeFromCompare(productId);
            button.textContent = 'Add to Compare';
            button.classList.remove('active');
        } else if (this.compareList.length < this.maxCompare) {
            this.compareList.push(productId);
            button.textContent = 'Remove from Compare';
            button.classList.add('active');
            this.updateCompareBar();
        } else {
            this.showNotification('Maximum 3 products can be compared', 'warning');
        }
    }

    removeFromCompare(productId) {
        this.compareList = this.compareList.filter(id => id !== productId);
        this.updateCompareBar();
    }

    updateCompareBar() {
        const compareBar = document.querySelector('.compare-bar');
        const compareCount = document.getElementById('compare-count');
        const compareItems = document.getElementById('compare-items');
        const compareBtn = document.getElementById('btn-compare');
        
        compareCount.textContent = this.compareList.length;
        compareBtn.disabled = this.compareList.length < 2;
        
        if (this.compareList.length > 0) {
            compareBar.classList.add('active');
        } else {
            compareBar.classList.remove('active');
        }
        
        // Update items display
        compareItems.innerHTML = this.compareList.map(id => {
            const product = document.querySelector(`[data-product-id="${id}"]`);
            const title = product.querySelector('.product-title').textContent;
            return `<span class="compare-item">${title}</span>`;
        }).join('');
    }

    showComparison() {
        // Create comparison modal
        const modal = document.createElement('div');
        modal.className = 'comparison-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h2>Product Comparison</h2>
                    <button class="close-modal">&times;</button>
                </div>
                <div class="comparison-table">
                    ${this.generateComparisonTable()}
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Close modal event
        modal.querySelector('.close-modal').addEventListener('click', () => {
            modal.remove();
        });
        
        // Close on outside click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });
    }

    generateComparisonTable() {
        // This would generate a detailed comparison table
        // For now, return a placeholder
        return '<p>Detailed product comparison table would be generated here</p>';
    }

    clearCompare() {
        this.compareList = [];
        document.querySelectorAll('.add-to-compare.active').forEach(btn => {
            btn.textContent = 'Add to Compare';
            btn.classList.remove('active');
        });
        this.updateCompareBar();
    }
}

// Interactive Image Gallery with Zoom
class ImageGallery {
    constructor(selector) {
        this.gallery = document.querySelector(selector);
        if (this.gallery) {
            this.init();
        }
    }

    init() {
        this.createZoomOverlay();
        this.bindEvents();
    }

    createZoomOverlay() {
        const overlay = document.createElement('div');
        overlay.className = 'image-zoom-overlay';
        overlay.innerHTML = `
            <div class="zoom-container">
                <img class="zoom-image" src="" alt="">
                <button class="zoom-close">&times;</button>
                <button class="zoom-prev">‹</button>
                <button class="zoom-next">›</button>
            </div>
        `;
        document.body.appendChild(overlay);
    }

    bindEvents() {
        // Image click to zoom
        this.gallery.addEventListener('click', (e) => {
            if (e.target.matches('img')) {
                this.openZoom(e.target);
            }
        });

        // Zoom controls
        const overlay = document.querySelector('.image-zoom-overlay');
        overlay.querySelector('.zoom-close').addEventListener('click', () => {
            this.closeZoom();
        });
        
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                this.closeZoom();
            }
        });
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (overlay.classList.contains('active')) {
                if (e.key === 'Escape') this.closeZoom();
                if (e.key === 'ArrowLeft') this.prevImage();
                if (e.key === 'ArrowRight') this.nextImage();
            }
        });
    }

    openZoom(img) {
        const overlay = document.querySelector('.image-zoom-overlay');
        const zoomImg = overlay.querySelector('.zoom-image');
        
        zoomImg.src = img.src;
        zoomImg.alt = img.alt;
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    closeZoom() {
        const overlay = document.querySelector('.image-zoom-overlay');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    prevImage() {
        // Implementation for previous image navigation
    }

    nextImage() {
        // Implementation for next image navigation
    }
}

// Notification System
class NotificationSystem {
    constructor() {
        this.createContainer();
    }

    createContainer() {
        const container = document.createElement('div');
        container.className = 'notification-container';
        document.body.appendChild(container);
    }

    show(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-message">${message}</span>
                <button class="notification-close">&times;</button>
            </div>
        `;
        
        const container = document.querySelector('.notification-container');
        container.appendChild(notification);
        
        // Show animation
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        
        // Auto remove
        setTimeout(() => {
            this.remove(notification);
        }, duration);
        
        // Manual close
        notification.querySelector('.notification-close').addEventListener('click', () => {
            this.remove(notification);
        });
    }

    remove(notification) {
        notification.classList.add('hide');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }
}

// Initialize enhanced features
document.addEventListener('DOMContentLoaded', function() {
    // Initialize product filter
    if (document.querySelector('.product-grid')) {
        new ProductFilter();
    }
    
    // Initialize product comparison
    if (document.querySelector('.product-card')) {
        new ProductComparison();
    }
    
    // Initialize image gallery
    if (document.querySelector('.product-gallery')) {
        new ImageGallery('.product-gallery');
    }
    
    // Initialize notification system
    window.notifications = new NotificationSystem();
});

// Global notification function
function showNotification(message, type = 'info', duration = 5000) {
    if (window.notifications) {
        window.notifications.show(message, type, duration);
    }
}

// Utility function for debouncing
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}