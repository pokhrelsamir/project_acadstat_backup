<script>
        // Wait for DOM to be ready
        document.addEventListener('DOMContentLoaded', function() {
            // Theme toggle setup
            const themeToggle = document.getElementById('themeToggle');
            const html = document.documentElement;
            
            updateThemeIcon(html.getAttribute('data-theme'));
            
            themeToggle.addEventListener('click', function() {
                const currentTheme = html.getAttribute('data-theme');
                const newTheme = currentTheme === 'light' ? 'dark' : 'light';
                
                html.setAttribute('data-theme', newTheme);
                localStorage.setItem('theme', newTheme);
                updateThemeIcon(newTheme);
            });

            function updateThemeIcon(theme) {
                const sunIcon = themeToggle.querySelector('.sun-icon');
                const moonIcon = themeToggle.querySelector('.moon-icon');
                
                if (theme === 'dark') {
                    sunIcon.style.display = 'inline';
                    moonIcon.style.display = 'none';
                } else {
                    sunIcon.style.display = 'none';
                    moonIcon.style.display = 'inline';
                }
            }

            // File upload handling
            const uploadArea = document.getElementById('uploadArea');
            const fileInput = document.getElementById('excelFileInput');
            const fileInfo = document.getElementById('fileInfo');
            const fileName = document.getElementById('fileName');
            const submitBtn = document.getElementById('submitBtn');
            const uploadForm = document.getElementById('uploadForm');

            if (fileInput) {
                fileInput.addEventListener('change', function(e) {
                    handleFileSelect(e.target.files[0]);
                });
            }

            // Drag and drop
            if (uploadArea) {
                uploadArea.addEventListener('dragover', function(e) {
                    e.preventDefault();
                    uploadArea.classList.add('dragover');
                });

                uploadArea.addEventListener('dragleave', function(e) {
                    e.preventDefault();
                    uploadArea.classList.remove('dragover');
                });

                uploadArea.addEventListener('drop', function(e) {
                    e.preventDefault();
                    uploadArea.classList.remove('dragover');
                    
                    const files = e.dataTransfer.files;
                    if (files.length > 0) {
                        handleFileSelect(files[0]);
                    }
                });
            }

            function handleFileSelect(file) {
                if (!file) return;

                // Validate file type
                const validExtensions = ['.xlsx', '.xls'];
                const fileExt = '.' + file.name.split('.').pop().toLowerCase();
                
                if (!validExtensions.includes(fileExt)) {
                    alert('Please select a valid Excel file (.xlsx or .xls)');
                    fileInput.value = '';
                    return;
                }

                // Show file info
                fileName.textContent = file.name + ' (' + formatFileSize(file.size) + ')';
                fileInfo.classList.add('show');
                submitBtn.disabled = false;
            }

            function formatFileSize(bytes) {
                if (bytes < 1024) return bytes + ' B';
                if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
                return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
            }

            // Toast notification function
            function showToast(message, type = 'success') {
                const toast = document.getElementById('toast-notification');
                const toastMsg = document.getElementById('toast-message');
                const toastTitle = document.querySelector('.toast-title');
                const toastIcon = document.querySelector('.toast-icon');
                
                if (!toast || !toastMsg) return;
                
                let config = {
                    success: { color: 'var(--success-color)', title: 'Success', icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>' },
                    warning: { color: 'var(--warning-color)', title: 'Warning', icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>' },
                    error: { color: 'var(--error-color)', title: 'Error', icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>' }
                };
                
                const cfg = config[type] || config.success;
                
                toast.style.borderLeftColor = cfg.color;
                toastIcon.style.background = cfg.color;
                toastIcon.innerHTML = cfg.icon;
                toastTitle.textContent = cfg.title;
                toastMsg.textContent = message;
                
                toast.style.bottom = '20px';
                setTimeout(() => { toast.style.bottom = '-100px'; }, 5000);
            }

            // Show toasts for Django messages on page load
            const messages = document.querySelectorAll('.success-message, .warning-box, .error-banner');
            messages.forEach(msg => {
                let text = msg.textContent.trim();
                let type = 'success';
                if (msg.classList.contains('warning-box')) type = 'warning';
                else if (msg.classList.contains('error-banner')) type = 'error';
                else if (msg.classList.contains('success-message')) type = 'success';
                
                // Clean up message text
                text = text.replace(/^Success[!:\s]*/i, '');
                text = text.replace(/^⚠️\s*/, '');
                
                if (text) showToast(text, type);
            });

            // Form submission
            if (uploadForm) {
                uploadForm.addEventListener('submit', function(e) {
                    e.preventDefault();
                    
                    const formData = new FormData(this);
                    const submitBtn = document.getElementById('submitBtn');
                    
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="animate-spin" style="animation: spin 1s linear infinite;"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg> Uploading...';
                    
                    // Add CSS animation for spinner if not present
                    if (!document.getElementById('spin-style')) {
                        const style = document.createElement('style');
                        style.id = 'spin-style';
                        style.textContent = '@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }';
                        document.head.appendChild(style);
                    }
                    
                    fetch('{% url "core:upload_marks_excel" %}', {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                        }
                    })
                    .then(response => {
                        if (response.ok) {
                            // Reload page to reflect changes and show messages
                            window.location.reload();
                        } else {
                            return response.text().then(text => {
                                console.error('Server error:', text);
                                throw new Error('Upload failed');
                            });
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        showToast('Upload failed! Please check your file format.', 'error');
                        submitBtn.disabled = false;
                        submitBtn.innerHTML = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                            <polyline points="7 10 12 15 17 10"/>
                            <line x1="12" y1="15" x2="12" y2="3"/>
                        </svg> Upload Marks`;
                    });
                });
            }
    