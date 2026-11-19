// Function to check if element is in viewport
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return rect.top < window.innerHeight && rect.bottom >= 0;
}

// Function to trigger animation when elements are visible
function handleScrollAnimation() {
    const image = document.querySelector('.animate-image');
    const text = document.querySelector('.animate-text');

    if (isInViewport(image)) {
        image.style.opacity = '1';
        image.style.transform = 'translateX(0)';
    }

    if (isInViewport(text)) {
        text.style.opacity = '1';
        text.style.transform = 'translateY(0)';
    }
}

// Event listener for scroll
window.addEventListener('scroll', handleScrollAnimation);

// Run function once on page load
handleScrollAnimation();






// Function to trigger animation when elements come into view
function revealOnScroll() {
    let elements = document.querySelectorAll('.fade-in');
    let windowHeight = window.innerHeight;

    elements.forEach(el => {
        let position = el.getBoundingClientRect().top;

        if (position < windowHeight - 150) {  // Increased sensitivity for better triggering
            el.classList.add('show');
        }
    });
}

// Run function on scroll
window.addEventListener('scroll', revealOnScroll);

// Run once on page load to check initial position
document.addEventListener("DOMContentLoaded", revealOnScroll);




/* <Feature section> */

document.addEventListener("DOMContentLoaded", function() {
    function revealOnScroll() {
        let elements = document.querySelectorAll('.tryOn-section, .tryOn-box');
        let windowHeight = window.innerHeight;

        elements.forEach(el => {
            let position = el.getBoundingClientRect().top;
            if (position < windowHeight - 100) {
                el.classList.add('show');
            }
        });
    }

    window.addEventListener('scroll', revealOnScroll);
    revealOnScroll(); // Run on load to ensure visibility
});




// Ensure all modals are hidden on page load
window.onload = function () {
    const modals = document.getElementsByClassName('modal');
    for (let modal of modals) {
        modal.classList.remove('show'); // Ensure modals are hidden
    }
};

// Open modal
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.add('show');  // Apply class to make it visible
}

// Close modal
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.remove('show'); // Remove class to hide it
}

// Switch between modals
function switchModal(currentModalId, newModalId) {
    closeModal(currentModalId);
    openModal(newModalId);
}

// Close modal when clicking outside
window.onclick = function (event) {
    if (event.target.classList.contains('modal')) {
        closeModal(event.target.id);
    }
};

// Handle form submissions
 document.getElementById('signup-form').onsubmit = async function (e) {
    e.preventDefault();

    const form = e.target;
    const data = {
      username: form.username.value,
      email: form.email.value,
      password: form.password.value
    };

    try {
      const response = await fetch('/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });

      const result = await response.json();

      if (result.success) {
        alert('Sign Up Successful! Please log in.');
        switchModal('signup-modal', 'login-modal');
        form.reset(); // Optional: clear form
      } else {
        alert('Signup failed: ' + result.message);
      }
    } catch (error) {
      console.error('Signup error:', error);
      alert('An error occurred. Please try again later.');
    }
  };


  document.getElementById('login-form').onsubmit = async function (e) {
    e.preventDefault();
    const form = e.target;
  
    const data = {
      email: form.email.value,
      password: form.password.value
    };
  
    try {
      const response = await fetch('/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });
  
      const result = await response.json();
  
      if (result.success) {
        alert('Login Successful!');
        // Check for redirect URL and navigate if it exists
        if (result.redirect) {
          window.location.href = result.redirect; // Redirect to the admin dashboard
        } else {
          closeModal('login-modal');
          window.location.reload();  // Reload the page to update UI based on the session
        }
      } else {
        alert('Login failed: ' + result.message);
      }
    } catch (error) {
      console.error('Login error:', error);
      alert('An error occurred during login.');
    }
  };

// Close modal with ESC key
document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
        const modals = document.getElementsByClassName('modal');
        for (let modal of modals) {
            closeModal(modal.id);
        }
    }
});



// Testimonial.

document.addEventListener("DOMContentLoaded", function() {
    function revealTestimonials() {
        let cards = document.querySelectorAll(".testimonial-card");
        let windowHeight = window.innerHeight;

        cards.forEach(card => {
            let position = card.getBoundingClientRect().top;
            if (position < windowHeight - 100) {
                card.classList.add("show");
            }
        });
    }

    window.addEventListener("scroll", revealTestimonials);
    revealTestimonials(); // Run on load
});


document.addEventListener("DOMContentLoaded", function () {
    // Load Header
    fetch('header.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('header').innerHTML = data;
        });

    // Load Footer
    fetch('footer.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('footer').innerHTML = data;
        });
});



