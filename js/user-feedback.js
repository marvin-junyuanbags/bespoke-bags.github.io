// User Feedback and Review System

// Star Rating Component
class StarRating {
    constructor(container, options = {}) {
        this.container = typeof container === 'string' ? document.querySelector(container) : container;
        this.options = {
            maxStars: options.maxStars || 5,
            initialRating: options.initialRating || 0,
            readonly: options.readonly || false,
            size: options.size || 'medium', // small, medium, large
            onRate: options.onRate || null
        };
        this.currentRating = this.options.initialRating;
        this.init();
    }

    init() {
        this.render();
        if (!this.options.readonly) {
            this.bindEvents();
        }
    }

    render() {
        const sizeClass = `star-rating-${this.options.size}`;
        const readonlyClass = this.options.readonly ? 'readonly' : '';
        
        this.container.className = `star-rating ${sizeClass} ${readonlyClass}`;
        this.container.innerHTML = '';
        
        for (let i = 1; i <= this.options.maxStars; i++) {
            const star = document.createElement('span');
            star.className = 'star';
            star.dataset.rating = i;
            star.innerHTML = '★';
            
            if (i <= this.currentRating) {
                star.classList.add('active');
            }
            
            this.container.appendChild(star);
        }
        
        // Add rating text
        const ratingText = document.createElement('span');
        ratingText.className = 'rating-text';
        ratingText.textContent = this.getRatingText();
        this.container.appendChild(ratingText);
    }

    bindEvents() {
        const stars = this.container.querySelectorAll('.star');
        
        stars.forEach(star => {
            star.addEventListener('mouseenter', () => {
                this.highlightStars(parseInt(star.dataset.rating));
            });
            
            star.addEventListener('click', () => {
                this.setRating(parseInt(star.dataset.rating));
            });
        });
        
        this.container.addEventListener('mouseleave', () => {
            this.highlightStars(this.currentRating);
        });
    }

    highlightStars(rating) {
        const stars = this.container.querySelectorAll('.star');
        stars.forEach((star, index) => {
            if (index < rating) {
                star.classList.add('hover');
            } else {
                star.classList.remove('hover');
            }
        });
    }

    setRating(rating) {
        this.currentRating = rating;
        this.render();
        
        if (this.options.onRate) {
            this.options.onRate(rating);
        }
    }

    getRating() {
        return this.currentRating;
    }

    getRatingText() {
        const texts = {
            0: 'No rating',
            1: 'Poor',
            2: 'Fair',
            3: 'Good',
            4: 'Very Good',
            5: 'Excellent'
        };
        return texts[this.currentRating] || '';
    }
}

// Review System
class ReviewSystem {
    constructor() {
        this.reviews = this.loadReviews();
        this.init();
    }

    init() {
        this.createReviewSection();
        this.bindEvents();
        this.renderReviews();
    }

    createReviewSection() {
        const reviewSection = document.createElement('div');
        reviewSection.className = 'review-section';
        reviewSection.innerHTML = `
            <div class="review-header">
                <h3>Customer Reviews</h3>
                <button class="btn-write-review" id="btn-write-review">Write a Review</button>
            </div>
            
            <div class="review-summary">
                <div class="average-rating">
                    <div class="rating-number">0.0</div>
                    <div class="rating-stars"></div>
                    <div class="rating-count">0 reviews</div>
                </div>
                <div class="rating-breakdown">
                    <div class="rating-bar" data-stars="5">
                        <span class="stars">5 ★</span>
                        <div class="bar"><div class="fill" style="width: 0%"></div></div>
                        <span class="count">0</span>
                    </div>
                    <div class="rating-bar" data-stars="4">
                        <span class="stars">4 ★</span>
                        <div class="bar"><div class="fill" style="width: 0%"></div></div>
                        <span class="count">0</span>
                    </div>
                    <div class="rating-bar" data-stars="3">
                        <span class="stars">3 ★</span>
                        <div class="bar"><div class="fill" style="width: 0%"></div></div>
                        <span class="count">0</span>
                    </div>
                    <div class="rating-bar" data-stars="2">
                        <span class="stars">2 ★</span>
                        <div class="bar"><div class="fill" style="width: 0%"></div></div>
                        <span class="count">0</span>
                    </div>
                    <div class="rating-bar" data-stars="1">
                        <span class="stars">1 ★</span>
                        <div class="bar"><div class="fill" style="width: 0%"></div></div>
                        <span class="count">0</span>
                    </div>
                </div>
            </div>
            
            <div class="review-filters">
                <button class="filter-btn active" data-filter="all">All Reviews</button>
                <button class="filter-btn" data-filter="5">5 Stars</button>
                <button class="filter-btn" data-filter="4">4 Stars</button>
                <button class="filter-btn" data-filter="3">3 Stars</button>
                <button class="filter-btn" data-filter="2">2 Stars</button>
                <button class="filter-btn" data-filter="1">1 Star</button>
                <button class="filter-btn" data-filter="images">With Images</button>
            </div>
            
            <div class="reviews-list" id="reviews-list"></div>
            
            <div class="load-more-container">
                <button class="btn-load-more" id="btn-load-more" style="display: none;">Load More Reviews</button>
            </div>
        `;
        
        // Insert after product info or at the end of main content
        const insertPoint = document.querySelector('.product-info') || document.querySelector('main');
        if (insertPoint) {
            insertPoint.appendChild(reviewSection);
        }
    }

    bindEvents() {
        // Write review button
        document.getElementById('btn-write-review').addEventListener('click', () => {
            this.showReviewForm();
        });
        
        // Filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.filterReviews(e.target.dataset.filter);
            });
        });
        
        // Load more button
        document.getElementById('btn-load-more').addEventListener('click', () => {
            this.loadMoreReviews();
        });
    }

    showReviewForm() {
        const modal = document.createElement('div');
        modal.className = 'review-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>Write a Review</h3>
                    <button class="close-modal">&times;</button>
                </div>
                <form class="review-form" id="review-form">
                    <div class="form-group">
                        <label>Overall Rating *</label>
                        <div class="rating-input" id="rating-input"></div>
                    </div>
                    
                    <div class="form-group">
                        <label for="review-title">Review Title *</label>
                        <input type="text" id="review-title" name="title" required maxlength="100" placeholder="Summarize your experience">
                    </div>
                    
                    <div class="form-group">
                        <label for="review-text">Your Review *</label>
                        <textarea id="review-text" name="review" required minlength="10" maxlength="1000" rows="5" placeholder="Share your thoughts about this product..."></textarea>
                        <div class="char-count">0/1000</div>
                    </div>
                    
                    <div class="form-group">
                        <label for="reviewer-name">Your Name *</label>
                        <input type="text" id="reviewer-name" name="name" required maxlength="50" placeholder="Enter your name">
                    </div>
                    
                    <div class="form-group">
                        <label for="reviewer-email">Email (optional)</label>
                        <input type="email" id="reviewer-email" name="email" maxlength="100" placeholder="your@email.com">
                        <small>Your email will not be published</small>
                    </div>
                    
                    <div class="form-group">
                        <label for="review-images">Add Photos (optional)</label>
                        <input type="file" id="review-images" name="images" multiple accept="image/*" max="5">
                        <small>You can upload up to 5 images</small>
                    </div>
                    
                    <div class="form-group checkbox-group">
                        <label>
                            <input type="checkbox" id="recommend-product" name="recommend">
                            I would recommend this product to others
                        </label>
                    </div>
                    
                    <div class="form-actions">
                        <button type="button" class="btn-cancel">Cancel</button>
                        <button type="submit" class="btn-submit">Submit Review</button>
                    </div>
                </form>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Initialize star rating
        const ratingInput = new StarRating('#rating-input', {
            onRate: (rating) => {
                modal.querySelector('#review-form').dataset.rating = rating;
            }
        });
        
        // Character counter
        const reviewText = modal.querySelector('#review-text');
        const charCount = modal.querySelector('.char-count');
        reviewText.addEventListener('input', () => {
            const count = reviewText.value.length;
            charCount.textContent = `${count}/1000`;
            if (count > 900) {
                charCount.style.color = '#e74c3c';
            } else {
                charCount.style.color = '#666';
            }
        });
        
        // Form submission
        modal.querySelector('#review-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.submitReview(e.target, modal);
        });
        
        // Close modal
        modal.querySelector('.close-modal').addEventListener('click', () => {
            modal.remove();
        });
        
        modal.querySelector('.btn-cancel').addEventListener('click', () => {
            modal.remove();
        });
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });
    }

    submitReview(form, modal) {
        const formData = new FormData(form);
        const rating = parseInt(form.dataset.rating);
        
        if (!rating) {
            showNotification('Please select a rating', 'error');
            return;
        }
        
        const review = {
            id: Date.now(),
            rating: rating,
            title: formData.get('title'),
            review: formData.get('review'),
            name: formData.get('name'),
            email: formData.get('email'),
            recommend: formData.get('recommend') === 'on',
            date: new Date().toISOString(),
            helpful: 0,
            images: [] // In a real app, you'd upload images to a server
        };
        
        this.addReview(review);
        modal.remove();
        showNotification('Thank you for your review!', 'success');
    }

    addReview(review) {
        this.reviews.unshift(review);
        this.saveReviews();
        this.renderReviews();
        this.updateSummary();
    }

    renderReviews() {
        const reviewsList = document.getElementById('reviews-list');
        reviewsList.innerHTML = '';
        
        this.reviews.forEach(review => {
            const reviewElement = this.createReviewElement(review);
            reviewsList.appendChild(reviewElement);
        });
        
        this.updateSummary();
    }

    createReviewElement(review) {
        const reviewDiv = document.createElement('div');
        reviewDiv.className = 'review-item';
        reviewDiv.dataset.rating = review.rating;
        
        const date = new Date(review.date).toLocaleDateString();
        const recommendBadge = review.recommend ? '<span class="recommend-badge">✓ Recommends</span>' : '';
        
        reviewDiv.innerHTML = `
            <div class="review-header">
                <div class="reviewer-info">
                    <div class="reviewer-name">${this.escapeHtml(review.name)}</div>
                    <div class="review-date">${date}</div>
                </div>
                <div class="review-rating"></div>
            </div>
            
            <div class="review-content">
                <h4 class="review-title">${this.escapeHtml(review.title)}</h4>
                <p class="review-text">${this.escapeHtml(review.review)}</p>
                ${recommendBadge}
            </div>
            
            <div class="review-actions">
                <button class="btn-helpful" data-review-id="${review.id}">
                    👍 Helpful (${review.helpful})
                </button>
                <button class="btn-report" data-review-id="${review.id}">
                    🚩 Report
                </button>
            </div>
        `;
        
        // Add star rating
        const ratingContainer = reviewDiv.querySelector('.review-rating');
        new StarRating(ratingContainer, {
            initialRating: review.rating,
            readonly: true,
            size: 'small'
        });
        
        // Bind action events
        reviewDiv.querySelector('.btn-helpful').addEventListener('click', () => {
            this.markHelpful(review.id);
        });
        
        reviewDiv.querySelector('.btn-report').addEventListener('click', () => {
            this.reportReview(review.id);
        });
        
        return reviewDiv;
    }

    updateSummary() {
        if (this.reviews.length === 0) return;
        
        const totalReviews = this.reviews.length;
        const averageRating = this.reviews.reduce((sum, review) => sum + review.rating, 0) / totalReviews;
        
        // Update average rating
        document.querySelector('.rating-number').textContent = averageRating.toFixed(1);
        document.querySelector('.rating-count').textContent = `${totalReviews} review${totalReviews !== 1 ? 's' : ''}`;
        
        // Update star display
        const starsContainer = document.querySelector('.rating-stars');
        new StarRating(starsContainer, {
            initialRating: Math.round(averageRating),
            readonly: true,
            size: 'medium'
        });
        
        // Update rating breakdown
        for (let i = 1; i <= 5; i++) {
            const count = this.reviews.filter(review => review.rating === i).length;
            const percentage = totalReviews > 0 ? (count / totalReviews) * 100 : 0;
            
            const ratingBar = document.querySelector(`[data-stars="${i}"]`);
            ratingBar.querySelector('.fill').style.width = `${percentage}%`;
            ratingBar.querySelector('.count').textContent = count;
        }
    }

    filterReviews(filter) {
        // Update active filter button
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-filter="${filter}"]`).classList.add('active');
        
        // Filter reviews
        const reviewItems = document.querySelectorAll('.review-item');
        reviewItems.forEach(item => {
            let show = true;
            
            if (filter !== 'all') {
                if (filter === 'images') {
                    // Show reviews with images (placeholder logic)
                    show = false;
                } else {
                    const rating = parseInt(item.dataset.rating);
                    show = rating === parseInt(filter);
                }
            }
            
            item.style.display = show ? 'block' : 'none';
        });
    }

    markHelpful(reviewId) {
        const review = this.reviews.find(r => r.id === reviewId);
        if (review) {
            review.helpful++;
            this.saveReviews();
            
            // Update button text
            const button = document.querySelector(`[data-review-id="${reviewId}"]`);
            button.textContent = `👍 Helpful (${review.helpful})`;
            button.disabled = true;
            
            showNotification('Thank you for your feedback!', 'success');
        }
    }

    reportReview(reviewId) {
        showNotification('Review has been reported for moderation', 'info');
    }

    loadReviews() {
        const saved = localStorage.getItem('bespoke-reviews');
        return saved ? JSON.parse(saved) : [];
    }

    saveReviews() {
        localStorage.setItem('bespoke-reviews', JSON.stringify(this.reviews));
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Feedback Widget
class FeedbackWidget {
    constructor() {
        this.init();
    }

    init() {
        this.createWidget();
        this.bindEvents();
    }

    createWidget() {
        const widget = document.createElement('div');
        widget.className = 'feedback-widget';
        widget.innerHTML = `
            <button class="feedback-trigger" id="feedback-trigger">
                💬 Feedback
            </button>
            
            <div class="feedback-panel" id="feedback-panel">
                <div class="feedback-header">
                    <h4>How can we improve?</h4>
                    <button class="close-feedback">&times;</button>
                </div>
                
                <form class="feedback-form" id="feedback-form">
                    <div class="feedback-type">
                        <label>What type of feedback is this?</label>
                        <select name="type" required>
                            <option value="">Select type...</option>
                            <option value="bug">Bug Report</option>
                            <option value="feature">Feature Request</option>
                            <option value="improvement">Improvement Suggestion</option>
                            <option value="general">General Feedback</option>
                        </select>
                    </div>
                    
                    <div class="feedback-message">
                        <label for="feedback-text">Your Message *</label>
                        <textarea id="feedback-text" name="message" required rows="4" placeholder="Tell us what you think..."></textarea>
                    </div>
                    
                    <div class="feedback-contact">
                        <label for="feedback-email">Email (optional)</label>
                        <input type="email" id="feedback-email" name="email" placeholder="your@email.com">
                        <small>We'll only use this to follow up if needed</small>
                    </div>
                    
                    <div class="feedback-actions">
                        <button type="button" class="btn-cancel">Cancel</button>
                        <button type="submit" class="btn-submit">Send Feedback</button>
                    </div>
                </form>
            </div>
        `;
        
        document.body.appendChild(widget);
    }

    bindEvents() {
        const trigger = document.getElementById('feedback-trigger');
        const panel = document.getElementById('feedback-panel');
        const form = document.getElementById('feedback-form');
        
        trigger.addEventListener('click', () => {
            panel.classList.toggle('active');
        });
        
        document.querySelector('.close-feedback').addEventListener('click', () => {
            panel.classList.remove('active');
        });
        
        document.querySelector('.feedback-form .btn-cancel').addEventListener('click', () => {
            panel.classList.remove('active');
            form.reset();
        });
        
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.submitFeedback(form);
        });
        
        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!widget.contains(e.target)) {
                panel.classList.remove('active');
            }
        });
    }

    submitFeedback(form) {
        const formData = new FormData(form);
        const feedback = {
            type: formData.get('type'),
            message: formData.get('message'),
            email: formData.get('email'),
            timestamp: new Date().toISOString(),
            page: window.location.pathname
        };
        
        // In a real application, you would send this to your server
        console.log('Feedback submitted:', feedback);
        
        // Save to localStorage for demo purposes
        const existingFeedback = JSON.parse(localStorage.getItem('bespoke-feedback') || '[]');
        existingFeedback.push(feedback);
        localStorage.setItem('bespoke-feedback', JSON.stringify(existingFeedback));
        
        showNotification('Thank you for your feedback!', 'success');
        form.reset();
        document.getElementById('feedback-panel').classList.remove('active');
    }
}

// Initialize feedback systems
document.addEventListener('DOMContentLoaded', function() {
    // Initialize review system on product pages
    if (document.querySelector('.product-info') || window.location.pathname.includes('product')) {
        new ReviewSystem();
    }
    
    // Initialize feedback widget on all pages
    new FeedbackWidget();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { StarRating, ReviewSystem, FeedbackWidget };
}