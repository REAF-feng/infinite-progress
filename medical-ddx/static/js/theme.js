// Theme Toggle Functionality
document.addEventListener("DOMContentLoaded", function () {
	const themeToggle = document.getElementById("themeToggle");
	const themeIcon = document.getElementById("themeIcon");

	// Check for saved theme preference or default to light mode
	const currentTheme = localStorage.getItem("theme") || "light";
	document.documentElement.setAttribute("data-theme", currentTheme);

	// Update icon based on current theme
	updateThemeIcon(currentTheme);

	// Theme toggle event listener
	themeToggle.addEventListener("click", function () {
		const currentTheme = document.documentElement.getAttribute("data-theme");
		const newTheme = currentTheme === "dark" ? "light" : "dark";

		document.documentElement.setAttribute("data-theme", newTheme);
		localStorage.setItem("theme", newTheme);
		updateThemeIcon(newTheme);

		// Add smooth transition effect
		document.body.style.transition = "all 0.3s ease";
		setTimeout(() => {
			document.body.style.transition = "";
		}, 300);
	});

	function updateThemeIcon(theme) {
		if (theme === "dark") {
			themeIcon.className = "fas fa-sun";
		} else {
			themeIcon.className = "fas fa-moon";
		}
	}
});

// Add particles to hero section
function createParticles() {
	const heroParticles = document.querySelector(".hero-particles");
	if (!heroParticles) return;

	for (let i = 0; i < 50; i++) {
		const particle = document.createElement("div");
		particle.className = "particle";
		particle.style.left = Math.random() * 100 + "%";
		particle.style.animationDelay = Math.random() * 20 + "s";
		particle.style.animationDuration = Math.random() * 10 + 10 + "s";
		heroParticles.appendChild(particle);
	}
}

// Initialize particles when DOM is loaded
document.addEventListener("DOMContentLoaded", createParticles);

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

// Add loading animation to forms
function addLoadingEffect(button, text = "Processing...") {
	const originalText = button.innerHTML;
	button.innerHTML = `<i class="fas fa-spinner fa-spin me-2"></i>${text}`;
	button.disabled = true;

	return function removeLoading() {
		button.innerHTML = originalText;
		button.disabled = false;
	};
}

// Add ripple effect to buttons
document.addEventListener("DOMContentLoaded", function () {
	const buttons = document.querySelectorAll(".btn");

	buttons.forEach((button) => {
		button.addEventListener("click", function (e) {
			const ripple = document.createElement("span");
			const rect = button.getBoundingClientRect();
			const size = Math.max(rect.width, rect.height);
			const x = e.clientX - rect.left - size / 2;
			const y = e.clientY - rect.top - size / 2;

			ripple.style.width = ripple.style.height = size + "px";
			ripple.style.left = x + "px";
			ripple.style.top = y + "px";
			ripple.classList.add("ripple");

			button.appendChild(ripple);

			setTimeout(() => {
				ripple.remove();
			}, 600);
		});
	});
});

// Add scroll animations
const observerOptions = {
	threshold: 0.1,
	rootMargin: "0px 0px -100px 0px",
};

const observer = new IntersectionObserver(function (entries) {
	entries.forEach((entry) => {
		if (entry.isIntersecting) {
			entry.target.style.opacity = "1";
			entry.target.style.transform = "translateY(0)";
		}
	});
}, observerOptions);

document.addEventListener("DOMContentLoaded", function () {
	const cards = document.querySelectorAll(".card, .medical-card");
	cards.forEach((card) => {
		card.style.opacity = "0";
		card.style.transform = "translateY(30px)";
		card.style.transition = "opacity 0.6s ease, transform 0.6s ease";
		observer.observe(card);
	});
});

// Enhanced form validation
function validateForm(formElement) {
	const inputs = formElement.querySelectorAll("input[required], textarea[required]");
	let isValid = true;

	inputs.forEach((input) => {
		const errorElement = input.parentNode.querySelector(".error-message");

		if (!input.value.trim()) {
			isValid = false;
			input.classList.add("is-invalid");

			if (!errorElement) {
				const error = document.createElement("div");
				error.className = "error-message text-danger mt-1";
				error.textContent = `${input.placeholder || "This field"} is required`;
				input.parentNode.appendChild(error);
			}
		} else {
			input.classList.remove("is-invalid");
			if (errorElement) {
				errorElement.remove();
			}
		}
	});

	return isValid;
}
