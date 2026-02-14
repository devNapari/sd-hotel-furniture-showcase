// Notification System JavaScript

class NotificationManager {
    constructor() {
        this.contactsData = [];
        this.consultationsData = [];
        this.unreadCounts = { contacts: 0, consultations: 0 };
        this.currentDetailsView = null;
        this.init();
    }
    
    init() {
        // Add notification icon to navbar if not already present
        this.addNotificationIcon();
        
        // Setup event listeners
        this.setupEventListeners();
        
        // Initial load
        this.loadNotifications();
        
        // Refresh notifications every 30 seconds
        setInterval(() => this.refreshCounts(), 30000);
    }
    
    addNotificationIcon() {
        const navbar = document.querySelector('.navbar-text');
        if (!navbar || document.getElementById('notification-icon-btn')) return;
        
        const notificationIconHTML = `
            <div class="notification-icon-container" style="display: inline-block;">
                <button type="button" id="notification-icon-btn" class="btn btn-link" 
                        data-toggle="modal" data-target="#notificationsModal"
                        title="Notifications" style="position: relative; padding: 0; border: none; background: none;">
                    <i class="fa fa-bell notification-icon"></i>
                    <span id="notification-badge" class="notification-badge" style="display:none;">0</span>
                </button>
            </div>
        `;
        
        navbar.insertAdjacentHTML('beforeend', notificationIconHTML);
    }
    
    setupEventListeners() {
        // Tab switching
        document.addEventListener('click', (e) => {
            if (e.target.id === 'contacts-tab') {
                this.loadContacts();
            } else if (e.target.id === 'consultations-tab') {
                this.loadConsultations();
            }
        });
    }
    
    async loadNotifications() {
        await this.refreshCounts();
        await this.loadContacts();
    }
    
    async refreshCounts() {
        try {
            const response = await fetch('/api/admin/notifications/count');
            const data = await response.json();
            
            if (data.status === 'success') {
                this.unreadCounts = {
                    contacts: data.contacts,
                    consultations: data.consultations
                };
                
                this.updateBadges();
            }
        } catch (error) {
            console.error('Error refreshing notification counts:', error);
        }
    }
    
    updateBadges() {
        const total = this.unreadCounts.contacts + this.unreadCounts.consultations;
        const mainBadge = document.getElementById('notification-badge');
        const contactsBadge = document.getElementById('contacts-badge');
        const consultationsBadge = document.getElementById('consultations-badge');
        
        if (total > 0) {
            mainBadge.textContent = total;
            mainBadge.style.display = 'flex';
        } else {
            mainBadge.style.display = 'none';
        }
        
        if (this.unreadCounts.contacts > 0) {
            contactsBadge.textContent = this.unreadCounts.contacts;
            contactsBadge.style.display = 'inline-block';
        } else {
            contactsBadge.style.display = 'none';
        }
        
        if (this.unreadCounts.consultations > 0) {
            consultationsBadge.textContent = this.unreadCounts.consultations;
            consultationsBadge.style.display = 'inline-block';
        } else {
            consultationsBadge.style.display = 'none';
        }
    }
    
    async loadContacts() {
        const loading = document.getElementById('contacts-loading');
        const list = document.getElementById('contacts-list');
        const empty = document.getElementById('contacts-empty');
        
        loading.style.display = 'block';
        list.style.display = 'none';
        empty.style.display = 'none';
        
        try {
            const response = await fetch('/api/admin/notifications/contacts?per_page=100');
            const data = await response.json();
            
            if (data.status === 'success') {
                this.contactsData = data.messages;
                
                if (data.messages.length === 0) {
                    empty.style.display = 'block';
                } else {
                    list.innerHTML = this.renderContactsList(data.messages);
                    list.style.display = 'block';
                    
                    // Add event listeners to action buttons
                    this.attachContactListeners();
                }
            }
        } catch (error) {
            console.error('Error loading contacts:', error);
            empty.innerHTML = '<p class="text-danger">Error loading messages</p>';
            empty.style.display = 'block';
        } finally {
            loading.style.display = 'none';
        }
    }
    
    async loadConsultations() {
        const loading = document.getElementById('consultations-loading');
        const list = document.getElementById('consultations-list');
        const empty = document.getElementById('consultations-empty');
        
        loading.style.display = 'block';
        list.style.display = 'none';
        empty.style.display = 'none';
        
        try {
            const response = await fetch('/api/admin/notifications/consultations?per_page=100');
            const data = await response.json();
            
            if (data.status === 'success') {
                this.consultationsData = data.requests;
                
                if (data.requests.length === 0) {
                    empty.style.display = 'block';
                } else {
                    list.innerHTML = this.renderConsultationsList(data.requests);
                    list.style.display = 'block';
                    
                    // Add event listeners to action buttons
                    this.attachConsultationListeners();
                }
            }
        } catch (error) {
            console.error('Error loading consultations:', error);
            empty.innerHTML = '<p class="text-danger">Error loading requests</p>';
            empty.style.display = 'block';
        } finally {
            loading.style.display = 'none';
        }
    }
    
    renderContactsList(messages) {
        return messages.map(msg => `
            <div class="notification-item ${msg.isRead ? '' : 'unread'}" data-id="${msg.id}">
                <div class="notification-item-header">
                    <div>
                        <div class="notification-item-name">
                            ${msg.firstName} ${msg.lastName}
                            ${msg.isRead ? '' : '<span class="notification-badge-unread">NEW</span>'}
                        </div>
                        <div class="notification-item-time">${this.formatDate(msg.createdAt)}</div>
                    </div>
                </div>
                <div class="notification-item-subject"><strong>Subject:</strong> ${msg.subject}</div>
                <div style="font-size: 13px; color: #666; margin-bottom: 8px;">
                    <strong>From:</strong> ${msg.email}
                </div>
                <div style="font-size: 13px; color: #666; margin-bottom: 10px;">
                    ${msg.message.substring(0, 100)}${msg.message.length > 100 ? '...' : ''}
                </div>
                <div class="notification-item-actions">
                    <button class="btn-view-details" onclick="notificationManager.viewContactDetails(${msg.id})">
                        <i class="fa fa-eye"></i> View
                    </button>
                    ${msg.isRead ? '' : `
                        <button class="btn-mark-read" onclick="notificationManager.markContactRead(${msg.id})">
                            <i class="fa fa-check"></i> Mark Read
                        </button>
                    `}
                    <button class="btn-delete" onclick="notificationManager.deleteContact(${msg.id})">
                        <i class="fa fa-trash"></i> Delete
                    </button>
                </div>
            </div>
        `).join('');
    }
    
    renderConsultationsList(requests) {
        return requests.map(req => {
            const cartTotal = req.cartItems ? req.cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0) : 0;
            
            return `
                <div class="notification-item ${req.isRead ? '' : 'unread'}" data-id="${req.id}">
                    <div class="notification-item-header">
                        <div>
                            <div class="notification-item-name">
                                ${req.firstName} ${req.lastName}
                                ${req.isRead ? '' : '<span class="notification-badge-unread">NEW</span>'}
                            </div>
                            <div class="notification-item-time">${this.formatDate(req.createdAt)}</div>
                        </div>
                    </div>
                    <div class="notification-item-subject"><strong>Subject:</strong> ${req.subject}</div>
                    <div style="font-size: 13px; color: #666; margin-bottom: 8px;">
                        <strong>From:</strong> ${req.email} | <strong>Date:</strong> ${req.preferredDate} @ ${req.preferredTime}
                    </div>
                    ${req.cartItems && req.cartItems.length > 0 ? `
                        <div style="font-size: 12px; color: #666; margin-bottom: 8px;">
                            <strong>Items:</strong> ${req.cartItems.length} products | <strong>Total:</strong> $${cartTotal.toFixed(2)}
                        </div>
                    ` : ''}
                    <div style="font-size: 13px; color: #666; margin-bottom: 10px;">
                        ${req.message.substring(0, 100)}${req.message.length > 100 ? '...' : ''}
                    </div>
                    <div class="notification-item-actions">
                        <button class="btn-view-details" onclick="notificationManager.viewConsultationDetails(${req.id})">
                            <i class="fa fa-eye"></i> View
                        </button>
                        ${req.isRead ? '' : `
                            <button class="btn-mark-read" onclick="notificationManager.markConsultationRead(${req.id})">
                                <i class="fa fa-check"></i> Mark Read
                            </button>
                        `}
                        <button class="btn-delete" onclick="notificationManager.deleteConsultation(${req.id})">
                            <i class="fa fa-trash"></i> Delete
                        </button>
                    </div>
                </div>
            `;
        }).join('');
    }
    
    viewContactDetails(id) {
        const msg = this.contactsData.find(m => m.id === id);
        if (!msg) return;
        
        const detailsHTML = `
            <div class="details-modal-content">
                <div style="padding: 20px;">
                    <h5 class="mb-4">Contact Message Details</h5>
                    
                    <div class="details-field">
                        <div class="details-field-label">Name</div>
                        <div class="details-field-value">${msg.firstName} ${msg.lastName}</div>
                    </div>
                    
                    <div class="details-field">
                        <div class="details-field-label">Email</div>
                        <div class="details-field-value">
                            <a href="mailto:${msg.email}">${msg.email}</a>
                        </div>
                    </div>
                    
                    ${msg.phone ? `
                        <div class="details-field">
                            <div class="details-field-label">Phone</div>
                            <div class="details-field-value">
                                <a href="tel:${msg.phone}">${msg.phone}</a>
                            </div>
                        </div>
                    ` : ''}
                    
                    ${msg.company ? `
                        <div class="details-field">
                            <div class="details-field-label">Company</div>
                            <div class="details-field-value">${msg.company}</div>
                        </div>
                    ` : ''}
                    
                    <div class="details-field">
                        <div class="details-field-label">Subject</div>
                        <div class="details-field-value">${msg.subject}</div>
                    </div>
                    
                    <div class="details-field">
                        <div class="details-field-label">Message</div>
                        <div class="details-field-value" style="white-space: pre-wrap; line-height: 1.6;">
                            ${msg.message}
                        </div>
                    </div>
                    
                    <div class="details-field">
                        <div class="details-field-label">Newsletter Subscription</div>
                        <div class="details-field-value">
                            ${msg.newsletter ? '<span class="badge badge-success">Subscribed</span>' : '<span class="badge badge-secondary">Not Subscribed</span>'}
                        </div>
                    </div>
                    
                    <div class="details-field">
                        <div class="details-field-label">Submitted</div>
                        <div class="details-field-value">${this.formatDateTime(msg.createdAt)}</div>
                    </div>
                </div>
            </div>
        `;
        
        this.showDetailsModal('Contact Message', detailsHTML);
        
        // Mark as read
        if (!msg.isRead) {
            this.markContactRead(id);
        }
    }
    
    viewConsultationDetails(id) {
        const req = this.consultationsData.find(r => r.id === id);
        if (!req) return;
        
        const cartTotal = req.cartItems ? req.cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0) : 0;
        
        let cartHTML = '';
        if (req.cartItems && req.cartItems.length > 0) {
            cartHTML = `
                <div class="details-field">
                    <div class="details-field-label">Selected Products</div>
                    <table class="cart-items-table">
                        <thead>
                            <tr>
                                <th>Product</th>
                                <th>Qty</th>
                                <th>Price</th>
                                <th>Subtotal</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${req.cartItems.map(item => `
                                <tr>
                                    <td><strong>${item.name}</strong> (#${item.id})</td>
                                    <td>${item.quantity}</td>
                                    <td>$${item.price.toFixed(2)}</td>
                                    <td><strong>$${(item.price * item.quantity).toFixed(2)}</strong></td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                    <div style="text-align: right; margin-top: 10px; padding: 10px; background-color: #f8f9fa; border-radius: 4px;">
                        <strong>Total: $${cartTotal.toFixed(2)}</strong>
                    </div>
                </div>
            `;
        }
        
        const detailsHTML = `
            <div class="details-modal-content">
                <div style="padding: 20px;">
                    <h5 class="mb-4">Consultation Request Details</h5>
                    
                    <div class="details-field">
                        <div class="details-field-label">Name</div>
                        <div class="details-field-value">${req.firstName} ${req.lastName}</div>
                    </div>
                    
                    <div class="details-field">
                        <div class="details-field-label">Email</div>
                        <div class="details-field-value">
                            <a href="mailto:${req.email}">${req.email}</a>
                        </div>
                    </div>
                    
                    <div class="details-field">
                        <div class="details-field-label">Phone</div>
                        <div class="details-field-value">
                            <a href="tel:${req.phone}">${req.phone}</a>
                        </div>
                    </div>
                    
                    ${req.company ? `
                        <div class="details-field">
                            <div class="details-field-label">Company</div>
                            <div class="details-field-value">${req.company}</div>
                        </div>
                    ` : ''}
                    
                    <div class="details-field">
                        <div class="details-field-label">Subject</div>
                        <div class="details-field-value">${req.subject}</div>
                    </div>
                    
                    <div class="details-field">
                        <div class="details-field-label">Message</div>
                        <div class="details-field-value" style="white-space: pre-wrap; line-height: 1.6;">
                            ${req.message}
                        </div>
                    </div>
                    
                    <div class="details-field">
                        <div class="details-field-label">Preferred Consultation Date</div>
                        <div class="details-field-value">${req.preferredDate}</div>
                    </div>
                    
                    <div class="details-field">
                        <div class="details-field-label">Preferred Consultation Time</div>
                        <div class="details-field-value">${req.preferredTime}</div>
                    </div>
                    
                    ${cartHTML}
                    
                    <div class="details-field">
                        <div class="details-field-label">Newsletter Subscription</div>
                        <div class="details-field-value">
                            ${req.newsletter ? '<span class="badge badge-success">Subscribed</span>' : '<span class="badge badge-secondary">Not Subscribed</span>'}
                        </div>
                    </div>
                    
                    <div class="details-field">
                        <div class="details-field-label">Submitted</div>
                        <div class="details-field-value">${this.formatDateTime(req.createdAt)}</div>
                    </div>
                </div>
            </div>
        `;
        
        this.showDetailsModal('Consultation Request', detailsHTML);
        
        // Mark as read
        if (!req.isRead) {
            this.markConsultationRead(id);
        }
    }
    
    showDetailsModal(title, content) {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.id = 'detailsModal';
        modal.setAttribute('tabindex', '-1');
        modal.setAttribute('role', 'dialog');
        modal.innerHTML = `
            <div class="modal-dialog modal-lg" role="document">
                <div class="modal-content">
                    <div class="modal-header bg-primary text-white">
                        <h5 class="modal-title">${title}</h5>
                        <button type="button" class="btn-close btn-close-white" data-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        ${content}
                    </div>
                </div>
            </div>
        `;
        
        // Remove old modal if exists
        const oldModal = document.getElementById('detailsModal');
        if (oldModal) oldModal.remove();
        
        document.body.appendChild(modal);
        
        // Show using jQuery if available
        if (window.jQuery) {
            window.jQuery(modal).modal('show');
        }
    }
    
    async markContactRead(id) {
        try {
            const response = await fetch(`/api/admin/notifications/contact/${id}/read`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                const item = document.querySelector(`.notification-item[data-id="${id}"]`);
                if (item) {
                    item.classList.remove('unread');
                }
                
                this.refreshCounts();
            }
        } catch (error) {
            console.error('Error marking contact as read:', error);
        }
    }
    
    async markConsultationRead(id) {
        try {
            const response = await fetch(`/api/admin/notifications/consultation/${id}/read`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                const item = document.querySelector(`.notification-item[data-id="${id}"]`);
                if (item) {
                    item.classList.remove('unread');
                }
                
                this.refreshCounts();
            }
        } catch (error) {
            console.error('Error marking consultation as read:', error);
        }
    }
    
    async deleteContact(id) {
        if (!confirm('Are you sure you want to delete this message?')) return;
        
        try {
            const response = await fetch(`/api/admin/notifications/contact/${id}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                this.loadContacts();
                this.refreshCounts();
            }
        } catch (error) {
            console.error('Error deleting contact:', error);
            alert('Error deleting message');
        }
    }
    
    async deleteConsultation(id) {
        if (!confirm('Are you sure you want to delete this request?')) return;
        
        try {
            const response = await fetch(`/api/admin/notifications/consultation/${id}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                this.loadConsultations();
                this.refreshCounts();
            }
        } catch (error) {
            console.error('Error deleting consultation:', error);
            alert('Error deleting request');
        }
    }
    
    attachContactListeners() {
        // Listeners attached via onclick attributes in HTML
    }
    
    attachConsultationListeners() {
        // Listeners attached via onclick attributes in HTML
    }
    
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    }
    
    formatDateTime(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) + 
               ' at ' + date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    }
}

// Initialize notification manager when page loads
let notificationManager;
document.addEventListener('DOMContentLoaded', () => {
    notificationManager = new NotificationManager();
});
