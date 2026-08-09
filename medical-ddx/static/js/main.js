// Main JavaScript for Medical Diagnosis Assistant

document.addEventListener("DOMContentLoaded", function () {
	// Initialize tooltips if Bootstrap is available
	if (typeof bootstrap !== "undefined") {
		var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
		var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
			return new bootstrap.Tooltip(tooltipTriggerEl);
		});
	}

	// Smooth scrolling for anchor links
	document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
		anchor.addEventListener("click", function (e) {
			e.preventDefault();
			const target = document.querySelector(this.getAttribute("href"));
			if (target) {
				target.scrollIntoView({
					behavior: "smooth",
					block: "start",
				});
			}
		});
	});

	// Auto-resize textarea
	const textarea = document.getElementById("symptoms");
	if (textarea) {
		textarea.addEventListener("input", function () {
			this.style.height = "auto";
			this.style.height = this.scrollHeight + "px";
		});
	}

	// Form validation
	const forms = document.querySelectorAll(".needs-validation");
	Array.prototype.slice.call(forms).forEach(function (form) {
		form.addEventListener(
			"submit",
			function (event) {
				if (!form.checkValidity()) {
					event.preventDefault();
					event.stopPropagation();
				}
				form.classList.add("was-validated");
			},
			false
		);
	});

	// Loading state management
	function showLoading(button) {
		const originalText = button.innerHTML;
		button.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Loading...';
		button.disabled = true;
		button.dataset.originalText = originalText;
	}

	function hideLoading(button) {
		if (button.dataset.originalText) {
			button.innerHTML = button.dataset.originalText;
			button.disabled = false;
		}
	}

	// Copy to clipboard functionality
	window.copyToClipboard = function (text) {
		navigator.clipboard.writeText(text).then(
			function () {
				showToast("Copied to clipboard!", "success");
			},
			function (err) {
				console.error("Could not copy text: ", err);
				showToast("Failed to copy text", "error");
			}
		);
	};

	// Toast notification system
	window.showToast = function (message, type = "info") {
		// Create toast container if it doesn't exist
		let toastContainer = document.getElementById("toast-container");
		if (!toastContainer) {
			toastContainer = document.createElement("div");
			toastContainer.id = "toast-container";
			toastContainer.className = "position-fixed top-0 end-0 p-3";
			toastContainer.style.zIndex = "1055";
			document.body.appendChild(toastContainer);
		}

		// Create toast element
		const toastId = "toast-" + Date.now();
		const toastHtml = `
            <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="toast-header bg-${type === "error" ? "danger" : type} text-white">
                    <i class="fas fa-${type === "success" ? "check-circle" : type === "error" ? "exclamation-circle" : "info-circle"} me-2"></i>
                    <strong class="me-auto">Notification</strong>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
                </div>
                <div class="toast-body">
                    ${message}
                </div>
            </div>
        `;

		toastContainer.insertAdjacentHTML("beforeend", toastHtml);
		const toastElement = document.getElementById(toastId);
		const toast = new bootstrap.Toast(toastElement);
		toast.show();

		// Remove toast element after it's hidden
		toastElement.addEventListener("hidden.bs.toast", function () {
			toastElement.remove();
		});
	};

	// Print functionality
	window.printResults = function () {
		const resultsContent = document.getElementById("analysisResults");
		if (resultsContent) {
			const printWindow = window.open("", "_blank");
			printWindow.document.write(`
                <html>
                    <head>
                        <title>Medical Analysis Results</title>
                        <style>
                            body { font-family: Arial, sans-serif; margin: 20px; }
                            h1 { color: #0d6efd; }
                            .disclaimer { background: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0; }
                        </style>
                    </head>
                    <body>
                        <h1>Medical Analysis Results</h1>
                        <div>${resultsContent.innerHTML}</div>
                        <div class="disclaimer">
                            <strong>Disclaimer:</strong> This analysis is for educational purposes only. 
                            Always consult with qualified healthcare professionals for medical advice.
                        </div>
                        <p><em>Generated on: ${new Date().toLocaleString()}</em></p>
                    </body>
                </html>
            `);
			printWindow.document.close();
			printWindow.print();
		}
	};

	// Keyboard shortcuts
	document.addEventListener("keydown", function (e) {
		// Ctrl/Cmd + Enter to submit form
		if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
			const form = document.getElementById("symptomForm");
			if (form) {
				form.dispatchEvent(new Event("submit"));
			}
		}
	});

	// Auto-save to localStorage
	const symptomsInput = document.getElementById("symptoms");
	if (symptomsInput) {
		// Load saved content
		const savedSymptoms = localStorage.getItem("savedSymptoms");
		if (savedSymptoms && !symptomsInput.value) {
			symptomsInput.value = savedSymptoms;
		}

		// Save content as user types
		let saveTimeout;
		symptomsInput.addEventListener("input", function () {
			clearTimeout(saveTimeout);
			saveTimeout = setTimeout(() => {
				localStorage.setItem("savedSymptoms", this.value);
			}, 1000);
		});

		// Clear saved content when form is submitted
		const form = document.getElementById("symptomForm");
		if (form) {
			form.addEventListener("submit", function () {
				localStorage.removeItem("savedSymptoms");
			});
		}
	}

	// Dark mode toggle (if implemented)
	const darkModeToggle = document.getElementById("darkModeToggle");
	if (darkModeToggle) {
		darkModeToggle.addEventListener("click", function () {
			document.body.classList.toggle("dark-mode");
			const isDarkMode = document.body.classList.contains("dark-mode");
			localStorage.setItem("darkMode", isDarkMode);
		});

		// Load dark mode preference
		const savedDarkMode = localStorage.getItem("darkMode");
		if (savedDarkMode === "true") {
			document.body.classList.add("dark-mode");
		}
	}

	// Word count for textarea
	const wordCountDisplay = document.getElementById("wordCount");
	if (wordCountDisplay && symptomsInput) {
		function updateWordCount() {
			const text = symptomsInput.value.trim();
			const words = text ? text.split(/\s+/).length : 0;
			wordCountDisplay.textContent = `${words} words`;
		}

		symptomsInput.addEventListener("input", updateWordCount);
		updateWordCount(); // Initial count
	}

	// Enhanced error handling for API calls
	window.handleApiError = function (error) {
		console.error("API Error:", error);

		if (error.name === "NetworkError" || !navigator.onLine) {
			showToast("Network error. Please check your connection.", "error");
		} else if (error.status === 429) {
			showToast("Too many requests. Please wait a moment and try again.", "error");
		} else if (error.status >= 500) {
			showToast("Server error. Please try again later.", "error");
		} else {
			showToast("An unexpected error occurred. Please try again.", "error");
		}
	};

	// Performance monitoring
	if ("performance" in window) {
		window.addEventListener("load", function () {
			setTimeout(function () {
				const perfData = performance.getEntriesByType("navigation")[0];
				if (perfData.loadEventEnd - perfData.loadEventStart > 3000) {
					console.warn("Page load took longer than expected");
				}
			}, 0);
		});
	}

	// Accessibility improvements
	document.querySelectorAll("button, a, input, textarea").forEach((element) => {
		element.addEventListener("focus", function () {
			this.style.outline = "2px solid #0d6efd";
			this.style.outlineOffset = "2px";
		});

		element.addEventListener("blur", function () {
			this.style.outline = "";
			this.style.outlineOffset = "";
		});
	});

	console.log("Medical Diagnosis Assistant initialized successfully");
});
