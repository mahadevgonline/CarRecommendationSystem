
        // Sample favorites data
        const favoritesData = [
            
        {
            id: { { i.id } },
            cid: { { i.car.id } },
            make: "Nissan",
                model: "GTR R34",
                    year: { { i.car.year } },
            price: "₹51,00,000",
                category: "Coupe",
                    fuelType: "Gasoline",
                        description: "nvtrhsvhv",
                            engine: "2.6L twin turbo",
                                horsePower: "276",
                                    transmission: "Manual",
                                        mpgCity: "20",
                                            mpgHighway: "30",
                                                image: "/media/images/how\u002Dfast\u002Dis\u002Da\u002Dnissan\u002Dgtr_h2FfvTy.jpg",
            },
        
        ];

        // DOM Elements
        const emptyState = document.getElementById('emptyState');
        const favoritesGrid = document.getElementById('favoritesGrid');
        const comparisonActions = document.getElementById('comparisonActions');
        const compareFavorites = document.getElementById('compareFavorites');
        const clearAllFavorites = document.getElementById('clearAllFavorites');

        // Initialize the page
        document.addEventListener('DOMContentLoaded', function () {
            renderFavorites();
        });

        // Render favorites grid
        function renderFavorites() {
            // Clear the grid
            favoritesGrid.innerHTML = '';

            if (favoritesData.length === 0) {
                // Show empty state
                emptyState.style.display = 'block';
                comparisonActions.style.display = 'none';
                return;
            }

            // Hide empty state
            emptyState.style.display = 'none';
            comparisonActions.style.display = 'flex';

            // Add favorites to grid
            favoritesData.forEach(vehicle => {
                const favoriteCard = document.createElement('div');
                favoriteCard.className = 'favorite-card';
                favoriteCard.innerHTML = `
                    <div class="favorite-image">
                        <img src="${vehicle.image}" alt="${vehicle.make} ${vehicle.model}">
                        <div class="favorite-badge">${vehicle.badge}</div>
                        <div class="favorite-actions">
                            <div class="favorite-action remove" onclick="window.location.href='/remove-favorite/${vehicle.id}/'">
                                <i class="fas fa-times"></i>
                            </div>

                        </div>
                    </div>
                    <div class="favorite-content">
                        <div class="favorite-header">
                            <div class="favorite-title">
                                <h3>${vehicle.year} ${vehicle.make} ${vehicle.model}</h3>
                                <p>${vehicle.category} • ${vehicle.fuelType}</p>
                            </div>
                            <div class="favorite-price">${vehicle.price}</div>
                        </div>
                        <div class="favorite-specs">
                            <div class="spec-item">
                                <i class="fas fa-tachometer-alt"></i>
                                <span>${vehicle.engine}</span>
                            </div>
                            <div class="spec-item">
                                <i class="fas fa-horse-head"></i>
                                <span>${vehicle.horsePower}</span>
                            </div>
                            <div class="spec-item">
                                <i class="fas fa-cogs"></i>
                                <span>${vehicle.transmission}</span>
                            </div>
                            <div class="spec-item">
                                <i class="fas fa-gas-pump"></i>
                                <span>${vehicle.mpgCity}/${vehicle.mpgHighway} MPG</span>
                            </div>
                        </div>
                        <p class="favorite-description">${vehicle.description}</p>
                        <div class="favorite-footer">
                            <div class="favorite-date">
                                Added on ${formatDate(vehicle.addedDate)}
                            </div>
                            <a href="/car-detail/${vehicle.cid}/" class="btn btn-gold btn-sm">View Details</a>
                        </div>
                    </div>
                `;

                favoritesGrid.appendChild(favoriteCard);
            });

            // Add event listeners to action buttons
            document.querySelectorAll('.favorite-action.remove').forEach(button => {
                button.addEventListener('click', function (e) {
                    e.stopPropagation();
                    const vehicleId = parseInt(this.getAttribute('data-id'));
                    removeFromFavorites(vehicleId);
                });
            });

            document.querySelectorAll('.favorite-action.compare').forEach(button => {
                button.addEventListener('click', function (e) {
                    e.stopPropagation();
                    const vehicleId = parseInt(this.getAttribute('data-id'));
                    // In a real app, this would add to comparison
                    alert(`Added ${getVehicleName(vehicleId)} to comparison`);
                });
            });
        }

        // Remove vehicle from favorites
        function removeFromFavorites(vehicleId) {
            // In a real app, this would update the backend
            const index = favoritesData.findIndex(vehicle => vehicle.id === vehicleId);
            if (index !== -1) {
                const vehicleName = getVehicleName(vehicleId);
                favoritesData.splice(index, 1);
                renderFavorites();

                // Show confirmation message
                showNotification(`Removed ${vehicleName} from favorites`);
            }
        }

        // Compare selected favorites
        function compareSelectedFavorites() {
            if (favoritesData.length < 2) {
                alert('Please add at least 2 vehicles to favorites to compare');
                return;
            }

            // In a real app, this would redirect to comparison page with selected vehicles
            const vehicleIds = favoritesData.map(vehicle => vehicle.id);
            window.location.href = `compare.html?vehicles=${vehicleIds.join(',')}`;
        }

        // Clear all favorites
        function clearAllFavoritesHandler() {
            if (confirm('Are you sure you want to remove all vehicles from your favorites?')) {
                // In a real app, this would update the backend
                favoritesData.length = 0;
                renderFavorites();
                showNotification('All favorites cleared');
            }
        }

        // Helper function to get vehicle name
        function getVehicleName(vehicleId) {
            const vehicle = favoritesData.find(v => v.id === vehicleId);
            return vehicle ? `${vehicle.year} ${vehicle.make} ${vehicle.model}` : 'Vehicle';
        }

        // Helper function to format date
        function formatDate(dateString) {
            const options = { year: 'numeric', month: 'long', day: 'numeric' };
            return new Date(dateString).toLocaleDateString(undefined, options);
        }

        // Show notification
        function showNotification(message) {
            // Create notification element
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: var(--vintage-dark);
                color: var(--vintage-cream);
                padding: 15px 20px;
                border-radius: 3px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                z-index: 1000;
                font-family: 'Lora', serif;
                border-left: 4px solid var(--vintage-gold);
                transform: translateX(120%);
                transition: transform 0.3s ease;
            `;
            notification.textContent = message;

            document.body.appendChild(notification);

            // Animate in
            setTimeout(() => {
                notification.style.transform = 'translateX(0)';
            }, 100);

            // Animate out and remove
            setTimeout(() => {
                notification.style.transform = 'translateX(120%)';
                setTimeout(() => {
                    document.body.removeChild(notification);
                }, 300);
            }, 3000);
        }
    