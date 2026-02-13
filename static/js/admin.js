// Admin Panel JavaScript

$(document).ready(function() {
    // Initialize tooltips
    $('[data-bs-toggle="tooltip"]').tooltip();
    
    // Initialize popovers
    $('[data-bs-toggle="popover"]').popover();
    
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        $('.alert:not(.alert-permanent)').alert('close');
    }, 5000);
    
    // Initialize file upload
    initFileUpload();
    
    // Initialize image gallery
    initImageGallery();
    
    // Initialize analytics charts if on analytics page
    if ($('#analyticsChart').length) {
        initAnalyticsChart();
    }
});

// File Upload Functions
function initFileUpload() {
    const $uploadArea = $('.file-upload-area');
    const $fileInput = $('#fileInput');
    
    if ($uploadArea.length && $fileInput.length) {
        // Click upload area to trigger file input
        $uploadArea.on('click', function() {
            $fileInput.click();
        });
        
        // Drag and drop
        $uploadArea.on('dragover', function(e) {
            e.preventDefault();
            $(this).addClass('dragover');
        });
        
        $uploadArea.on('dragleave', function() {
            $(this).removeClass('dragover');
        });
        
        $uploadArea.on('drop', function(e) {
            e.preventDefault();
            $(this).removeClass('dragover');
            
            const files = e.originalEvent.dataTransfer.files;
            if (files.length > 0) {
                uploadFiles(files);
            }
        });
        
        // File input change
        $fileInput.on('change', function() {
            if (this.files.length > 0) {
                uploadFiles(this.files);
            }
        });
    }
}

function uploadFiles(files) {
    const formData = new FormData();
    
    // Add all files to form data
    for (let i = 0; i < files.length; i++) {
        formData.append('files[]', files[i]);
    }
    
    // Show loading
    const $uploadArea = $('.file-upload-area');
    const originalContent = $uploadArea.html();
    $uploadArea.html(`
        <div class="spinner-container">
            <div class="spinner"></div>
        </div>
        <p>Uploading ${files.length} file(s)...</p>
    `);
    
    // Send AJAX request
    $.ajax({
        url: $uploadArea.data('upload-url') || '/admin/upload',
        method: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            showToast('Files uploaded successfully!', 'success');
            location.reload(); // Reload to show new files
        },
        error: function(xhr, status, error) {
            showToast('Error uploading files: ' + error, 'error');
            $uploadArea.html(originalContent);
            initFileUpload(); // Re-initialize
        }
    });
}

// Image Gallery Functions
function initImageGallery() {
    // Image selection
    $('.image-selector-card').on('click', function() {
        const imageUrl = $(this).data('url');
        selectImage(imageUrl);
    });
    
    // Image deletion confirmation
    $('.delete-image-btn').on('click', function(e) {
        e.preventDefault();
        const imageId = $(this).data('id');
        const imageName = $(this).data('name');
        
        if (confirm(`Are you sure you want to delete "${imageName}"?`)) {
            deleteImage(imageId);
        }
    });
}

function selectImage(imageUrl) {
    // This function is called when an image is selected from the gallery
    // The actual implementation depends on where it's being used
    if (typeof window.parent !== 'undefined' && window.parent.selectImageCallback) {
        window.parent.selectImageCallback(imageUrl);
    } else if (window.opener && window.opener.selectImageCallback) {
        window.opener.selectImageCallback(imageUrl);
    } else {
        // Default behavior: copy URL to clipboard
        navigator.clipboard.writeText(imageUrl).then(function() {
            showToast('Image URL copied to clipboard!', 'success');
        });
    }
}

function deleteImage(imageId) {
    $.ajax({
        url: `/admin/delete-file/${imageId}`,
        method: 'GET',
        success: function(response) {
            showToast('Image deleted successfully!', 'success');
            $(`[data-id="${imageId}"]`).closest('.col').remove();
        },
        error: function() {
            showToast('Error deleting image', 'error');
        }
    });
}

// Analytics Chart
function initAnalyticsChart() {
    const ctx = document.getElementById('analyticsChart').getContext('2d');
    
    // Sample data - you would replace this with actual data from your backend
    const data = {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [{
            label: 'Page Views',
            data: [65, 59, 80, 81, 56, 55, 40],
            backgroundColor: 'rgba(67, 97, 238, 0.2)',
            borderColor: 'rgba(67, 97, 238, 1)',
            borderWidth: 2,
            tension: 0.4,
            fill: true
        }, {
            label: 'Unique Visitors',
            data: [28, 48, 40, 19, 86, 27, 90],
            backgroundColor: 'rgba(76, 201, 240, 0.2)',
            borderColor: 'rgba(76, 201, 240, 1)',
            borderWidth: 2,
            tension: 0.4,
            fill: true
        }]
    };
    
    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        drawBorder: false
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    };
    
    new Chart(ctx, config);
}

// Toast Notification System
function showToast(message, type = 'info') {
    // Create toast element
    const toastId = 'toast-' + Date.now();
    const toastHtml = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${getToastBg(type)} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-${getToastIcon(type)} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    // Add to container
    const $container = $('#toastContainer');
    if (!$container.length) {
        $('body').append('<div id="toastContainer" class="toast-container position-fixed top-0 end-0 p-3"></div>');
    }
    
    $('#toastContainer').append(toastHtml);
    
    // Initialize and show
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, {
        delay: 3000
    });
    
    toast.show();
    
    // Remove after hide
    toastElement.addEventListener('hidden.bs.toast', function() {
        $(this).remove();
    });
}

function getToastBg(type) {
    switch(type) {
        case 'success': return 'success';
        case 'error': return 'danger';
        case 'warning': return 'warning';
        default: return 'info';
    }
}

function getToastIcon(type) {
    switch(type) {
        case 'success': return 'check-circle';
        case 'error': return 'exclamation-circle';
        case 'warning': return 'exclamation-triangle';
        default: return 'info-circle';
    }
}

// Bulk Operations
function selectAllItems(checkbox) {
    const isChecked = $(checkbox).prop('checked');
    $('.item-checkbox').prop('checked', isChecked);
}

function performBulkAction(action) {
    const selectedIds = [];
    $('.item-checkbox:checked').each(function() {
        selectedIds.push($(this).val());
    });
    
    if (selectedIds.length === 0) {
        showToast('Please select at least one item', 'warning');
        return;
    }
    
    if (action === 'delete') {
        if (confirm(`Are you sure you want to delete ${selectedIds.length} item(s)?`)) {
            // Perform bulk deletion
            $.ajax({
                url: '/admin/bulk-delete',
                method: 'POST',
                data: JSON.stringify({ ids: selectedIds, type: 'contacts' }),
                contentType: 'application/json',
                success: function(response) {
                    showToast(`${selectedIds.length} item(s) deleted successfully!`, 'success');
                    location.reload();
                },
                error: function() {
                    showToast('Error deleting items', 'error');
                }
            });
        }
    }
}

// Search and Filter
function initSearch() {
    const $searchInput = $('#searchInput');
    const $tableRows = $('.table tbody tr');
    
    $searchInput.on('keyup', function() {
        const searchTerm = $(this).val().toLowerCase();
        
        $tableRows.each(function() {
            const rowText = $(this).text().toLowerCase();
            $(this).toggle(rowText.indexOf(searchTerm) > -1);
        });
    });
}

// Real-time Updates (WebSocket alternative using polling)
function initRealTimeUpdates() {
    // Check for new contacts every 30 seconds
    setInterval(checkNewContacts, 30000);
}

function checkNewContacts() {
    $.get('/admin/api/new-contacts-count', function(response) {
        if (response.count > 0) {
            // Update badge
            $('.contacts-badge').text(response.count).show();
            
            // Show notification
            if (Notification.permission === 'granted') {
                new Notification('New Contact Submission', {
                    body: `You have ${response.count} new contact submission(s)`,
                    icon: '/static/images/logo.png'
                });
            }
        }
    });
}

// Export Data
function exportData(type, format) {
    let url = `/admin/export/${type}`;
    
    if (format) {
        url += `?format=${format}`;
    }
    
    window.open(url, '_blank');
}

// Initialize on page load
$(document).ready(function() {
    initSearch();
    initRealTimeUpdates();
    
    // Request notification permission
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
    }
});