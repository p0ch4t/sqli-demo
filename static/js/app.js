// JavaScript for SQL Injection Demo

document.addEventListener('DOMContentLoaded', function() {
    
    // Auto-resize textarea
    const textarea = document.getElementById('query');
    if (textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    }

    // Clear button functionality
    const clearBtn = document.getElementById('clearBtn');
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            const queryTextarea = document.getElementById('query');
            const databaseSelect = document.getElementById('database');
            
            if (queryTextarea) {
                queryTextarea.value = '';
                queryTextarea.style.height = 'auto';
            }
            
            if (databaseSelect) {
                databaseSelect.selectedIndex = 0;
            }
        });
    }

    // Form submission with loading state
    const queryForm = document.getElementById('queryForm');
    if (queryForm) {
        queryForm.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            // Show loading state
            submitBtn.innerHTML = '<span class="loading"></span> Ejecutando...';
            submitBtn.disabled = true;
            
            // Re-enable after a delay (in case of error)
            setTimeout(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 10000);
        });
    }

    // Copy to clipboard functionality
    document.querySelectorAll('code').forEach(function(codeElement) {
        codeElement.addEventListener('click', function() {
            const text = this.textContent;
            navigator.clipboard.writeText(text).then(function() {
                // Show success message
                const originalText = codeElement.textContent;
                codeElement.textContent = '¡Copiado!';
                codeElement.style.backgroundColor = '#d4edda';
                codeElement.style.color = '#155724';
                
                setTimeout(() => {
                    codeElement.textContent = originalText;
                    codeElement.style.backgroundColor = '#f8f9fa';
                    codeElement.style.color = '#e83e8c';
                }, 2000);
            }).catch(function(err) {
                console.error('Error copying text: ', err);
            });
        });
        
        // Add cursor pointer
        codeElement.style.cursor = 'pointer';
        codeElement.title = 'Click para copiar';
    });

    // Database connection status check
    function checkDatabaseStatus() {
        const databases = ['mysql', 'postgresql', 'sqlserver', 'oracle'];
        
        databases.forEach(function(db) {
            fetch('/api/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    database: db,
                    query: 'SELECT 1'
                })
            })
            .then(response => response.json())
            .then(data => {
                const statusElement = document.querySelector(`[data-db="${db}"]`);
                if (statusElement) {
                    if (data.error && data.error.includes('Could not connect')) {
                        statusElement.classList.remove('online');
                        statusElement.classList.add('offline');
                        statusElement.title = 'Offline';
                    } else {
                        statusElement.classList.remove('offline');
                        statusElement.classList.add('online');
                        statusElement.title = 'Online';
                    }
                }
            })
            .catch(error => {
                console.error(`Error checking ${db} status:`, error);
            });
        });
    }

    // Check database status on page load
    if (window.location.pathname === '/') {
        setTimeout(checkDatabaseStatus, 1000);
    }

    // Auto-complete for common SQL keywords
    const sqlKeywords = [
        'SELECT', 'FROM', 'WHERE', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE',
        'UNION', 'OR', 'AND', 'ORDER BY', 'GROUP BY', 'HAVING', 'JOIN', 'LEFT JOIN',
        'RIGHT JOIN', 'INNER JOIN', 'OUTER JOIN', 'DISTINCT', 'COUNT', 'SUM', 'AVG',
        'MAX', 'MIN', 'LIKE', 'IN', 'BETWEEN', 'IS NULL', 'IS NOT NULL'
    ];

    if (textarea) {
        textarea.addEventListener('keydown', function(e) {
            if (e.key === 'Tab') {
                e.preventDefault();
                
                const start = this.selectionStart;
                const end = this.selectionEnd;
                const value = this.value;
                
                // Insert tab
                this.value = value.substring(0, start) + '    ' + value.substring(end);
                this.selectionStart = this.selectionEnd = start + 4;
            }
        });
    }

    // Syntax highlighting for SQL
    function highlightSQL(text) {
        const keywords = sqlKeywords.join('|');
        const regex = new RegExp(`\\b(${keywords})\\b`, 'gi');
        return text.replace(regex, '<span class="sql-keyword">$1</span>');
    }

    // Add syntax highlighting to textarea (optional)
    if (textarea) {
        textarea.addEventListener('input', function() {
            // This is a simplified version - in a real app you'd use a proper syntax highlighter
            const value = this.value;
            // You could add a preview div that shows highlighted SQL
        });
    }

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl+Enter to submit form
        if (e.ctrlKey && e.key === 'Enter') {
            const form = document.getElementById('queryForm');
            if (form) {
                form.submit();
            }
        }
        
        // Ctrl+L to clear
        if (e.ctrlKey && e.key === 'l') {
            e.preventDefault();
            const clearBtn = document.getElementById('clearBtn');
            if (clearBtn) {
                clearBtn.click();
            }
        }
    });

    // Tooltip initialization
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add some visual feedback for form interactions
    const formElements = document.querySelectorAll('.form-control, .form-select');
    formElements.forEach(element => {
        element.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        element.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });

    // Add CSS for focused state
    const style = document.createElement('style');
    style.textContent = `
        .focused {
            transform: scale(1.02);
            transition: transform 0.2s ease;
        }
        
        .sql-keyword {
            color: #007bff;
            font-weight: bold;
        }
        
        .form-control:focus, .form-select:focus {
            transform: scale(1.01);
        }
    `;
    document.head.appendChild(style);
}); 