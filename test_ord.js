
        // Sample order data
        const orders = [
            
        {
            id: "CP-2025-5",
                date: "2025\u002D12\u002D05",
                    status: "Processing",
                        statusText: {
                'Processing': '⏳ Pending',
                    'Accepted': '✅ Order Confirmed',
                        'Packed': '📦 Packed',
                            'Shipped': '🚚 Shipped',
                                'Out for Delivery': '🛵 Out for Delivery',
                                    'Delivered': '🎉 Delivered',
                                        'Rejected': '❌ Rejected',
                } ["Processing"] || "Processing",
                items: [
                    
                ],
        subtotal: [ 0].reduce((a, b) => a + b, 0),
            shipping: 0,
                tax: 0,
                    total: [ 0].reduce((a, b) => a + b, 0),
                        shippingAddress: "John Doe, 123 Classic Car Lane, Auburn, TX 46706",
                            tracking: "UPS: 1Z999AA1234567890",
                                paymentMethod: "Visa ending in 4242"
            },
        
        {
            id: "CP-2025-6",
                date: "2025\u002D12\u002D15",
                    status: "Processing",
                        statusText: {
                'Processing': '⏳ Pending',
                    'Accepted': '✅ Order Confirmed',
                        'Packed': '📦 Packed',
                            'Shipped': '🚚 Shipped',
                                'Out for Delivery': '🛵 Out for Delivery',
                                    'Delivered': '🎉 Delivered',
                                        'Rejected': '❌ Rejected',
                } ["Processing"] || "Processing",
                items: [
                    
        { name: "Brake Pad Set", specs: "2004 Toyota • New", quantity: { { j.quantity } }, price: { { j.item.price | inr_raw } }, image: "/media/images/f1.jpg" },
        
                ],
        subtotal: [ { { k.total_price | inr_raw } },  0].reduce((a, b) => a + b, 0),
            shipping: 0,
                tax: 0,
                    total: [ { { k.total_price | inr_raw } },  0].reduce((a, b) => a + b, 0),
                        shippingAddress: "John Doe, 123 Classic Car Lane, Auburn, CA 46706",
                            tracking: "UPS: 1Z999AA1234567890",
                                paymentMethod: "Visa ending in 4242"
            },
        

        ];

        // DOM elements
        const ordersGrid = document.getElementById('ordersGrid');
        const emptyState = document.getElementById('emptyState');
        const orderModal = document.getElementById('orderModal');
        const closeModal = document.getElementById('closeModal');
        const modalOrderId = document.getElementById('modalOrderId');
        const modalBody = document.getElementById('modalBody');

        // Render orders function
        function renderOrders(filteredOrders) {
            ordersGrid.innerHTML = '';

            if (filteredOrders.length === 0) {
                emptyState.style.display = 'block';
                return;
            }

            emptyState.style.display = 'none';

            filteredOrders.forEach(order => {
                const orderCard = document.createElement('div');
                orderCard.className = 'order-card';
                orderCard.innerHTML = `
                    <div class="order-header">
                        <div>
                            <div class="order-id">${order.id}</div>
                            <div class="order-date">${order.date}</div>
                        </div>
                        <div class="order-status status-${order.status.toLowerCase().replace(/ /g, '-')}">${order.statusText}</div>
                    </div>
                    <div class="order-body">
                        <div class="order-items">
                            ${order.items.slice(0, 2).map(item => `
                                <div class="order-item">
                                    <div class="item-image">
                                        <img src="${item.image}" alt="${item.name}">
                                    </div>
                                    <div class="item-details">
                                        <div class="item-name">${item.name}</div>
                                        <div class="item-specs">${item.specs}</div>
                                        <div class="item-quantity">Quantity: ${item.quantity}</div>
                                    </div>
                                    <div class="item-price">₹${item.price.toLocaleString('en-IN')}</div>
                                </div>
                            `).join('')}
                            ${order.items.length > 2 ? `<div style="text-align: center; padding: 10px; color: var(--vintage-gold); font-weight: 600;">
                                +${order.items.length - 2} more item${order.items.length - 2 > 1 ? 's' : ''}
                            </div>` : ''}
                        </div>
                        <div class="order-summary">
                            <div class="summary-row">
                                <span>Subtotal</span>
                                <span>₹${order.subtotal.toLocaleString('en-IN')}</span>
                            </div>
                            <div class="summary-row">
                                <span>Shipping</span>
                                <span>${order.shipping === 0 ? 'FREE' : `₹${order.shipping.toLocaleString('en-IN')}`}</span>
                            </div>
                            <div class="summary-row">
                                <span>Tax</span>
                                <span>₹${order.tax.toLocaleString('en-IN')}</span>
                            </div>
                            <div class="summary-row total">
                                <span>Total</span>
                                <span>₹${order.total.toLocaleString('en-IN')}</span>
                            </div>
                        </div>
                    </div>
                    <div class="order-footer">
                        <div class="tracking-info">
                            <i class="fas fa-shipping-fast"></i>
                            ${order.tracking}
                        </div>
                        <div class="order-actions">
                            <div class="btn-icon" title="View Details" onclick="viewOrderDetails('${order.id}')">
                                <i class="fas fa-eye"></i>
                            </div>

                        </div>
                    </div>
                `;
                ordersGrid.appendChild(orderCard);
            });
        }

        // Filter orders function

        // View order details
        function viewOrderDetails(orderId) {
            const order = orders.find(o => o.id === orderId);
            if (!order) return;

            modalOrderId.textContent = order.id;

            modalBody.innerHTML = `
                <div style="margin-bottom: 30px;">
                    <h4 style="margin-bottom: 15px; color: var(--vintage-dark);">Order Summary</h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 25px;">
                        <div>
                            <strong>Order Date:</strong><br>
                            <span style="color: var(--vintage-brown);">${order.date}</span>
                        </div>
                        <div>
                            <strong>Order Status:</strong><br>
                            <span class="order-status status-${order.status}" style="display: inline-block; margin-top: 5px;">${order.statusText}</span>
                        </div>
                        <div>
                            <strong>Payment Method:</strong><br>
                            <span style="color: var(--vintage-brown);">${order.paymentMethod}</span>
                        </div>
                        <div>
                            <strong>Tracking Number:</strong><br>
                            <span style="color: var(--vintage-brown);">${order.tracking}</span>
                        </div>
                    </div>
                </div>

                <div style="margin-bottom: 30px;">
                    <h4 style="margin-bottom: 15px; color: var(--vintage-dark);">Items Ordered</h4>
                    <div class="order-items" style="max-height: none;">
                        ${order.items.map(item => `
                            <div class="order-item">
                                <div class="item-image">
                                    <img src="${item.image}" alt="${item.name}">
                                </div>
                                <div class="item-details">
                                    <div class="item-name">${item.name}</div>
                                    <div class="item-specs">${item.specs}</div>
                                    <div class="item-quantity">Quantity: ${item.quantity}</div>
                                </div>
                                <div class="item-price">₹${(item.price * item.quantity).toLocaleString('en-IN')}</div>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px;">
                    <div>
                        <h4 style="margin-bottom: 15px; color: var(--vintage-dark);">Shipping Address</h4>
                        <div style="background: var(--vintage-cream); padding: 20px; border-radius: 2px; border: 1px solid var(--vintage-light);">
                            <p style="color: var(--vintage-brown); white-space: pre-line;">${order.shippingAddress}</p>
                        </div>
                    </div>
                    <div>
                        <h4 style="margin-bottom: 15px; color: var(--vintage-dark);">Order Total</h4>
                        <div style="background: var(--vintage-cream); padding: 20px; border-radius: 2px; border: 1px solid var(--vintage-light);">
                            <div class="summary-row">
                                <span>Subtotal</span>
                                <span>₹${order.subtotal.toLocaleString('en-IN')}</span>
                            </div>
                            <div class="summary-row">
                                <span>Shipping</span>
                                <span>${order.shipping === 0 ? 'FREE' : `₹${order.shipping.toLocaleString('en-IN')}`}</span>
                            </div>
                            <div class="summary-row">
                                <span>Tax</span>
                                <span>₹${order.tax.toLocaleString('en-IN')}</span>
                            </div>
                            <div class="summary-row" style="font-weight: 700; color: var(--vintage-gold); padding-top: 10px; border-top: 1px solid var(--vintage-light); margin-top: 10px;">
                                <span>Total</span>
                                <span>₹${order.total.toLocaleString('en-IN')}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div style="margin-top: 30px; display: flex; gap: 15px; justify-content: center;">
                    <button class="btn btn-outline" onclick="printOrder('${order.id}')">
                        <i class="fas fa-print"></i> Print Invoice
                    </button>
                    <button class="btn btn-gold" onclick="reorder('${order.id}')">
                        <i class="fas fa-redo"></i> Reorder Items
                    </button>
                    ${order.status === 'delivered' ? `
                    <button class="btn btn-outline" onclick="requestReturn('${order.id}')">
                        <i class="fas fa-undo"></i> Request Return
                    </button>
                    ` : ''}
                </div>
            `;

            orderModal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        // Close modal
        closeModal.addEventListener('click', () => {
            orderModal.classList.remove('active');
            document.body.style.overflow = 'auto';
        });

        // Close modal when clicking outside
        orderModal.addEventListener('click', (e) => {
            if (e.target === orderModal) {
                orderModal.classList.remove('active');
                document.body.style.overflow = 'auto';
            }
        });

        // Demo functions
        window.printOrder = function (orderId) {
            alert(`Printing invoice for order ${orderId}`);
        };

        window.reorder = function (orderId) {
            alert(`Adding items from order ${orderId} to cart`);
        };

        window.requestReturn = function (orderId) {
            alert(`Initiating return process for order ${orderId}`);
        };

        // Event listeners for filters

        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            renderOrders(orders);

            // Update cart count from localStorage
            const cart = JSON.parse(localStorage.getItem('classicPartsCart')) || [];
            const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
            document.getElementById('cartCount').textContent = totalItems || '3';
        });
    