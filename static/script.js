// Login page functionality
document.addEventListener('DOMContentLoaded', function() {
    const showSignupBtn = document.getElementById('showSignupBtn');
    const backToLoginBtn = document.getElementById('backToLoginBtn');
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    
    // Password visibility toggle for login form
    const togglePassword = document.getElementById('togglePassword');
    const passwordField = document.getElementById('password');
    const togglePasswordIcon = document.getElementById('togglePasswordIcon');
    
    // Password visibility toggle for signup form
    const toggleSignupPassword = document.getElementById('toggleSignupPassword');
    const signupPasswordField = document.getElementById('signup_password');
    const toggleSignupPasswordIcon = document.getElementById('toggleSignupPasswordIcon');
    
    if (showSignupBtn) {
        showSignupBtn.addEventListener('click', function() {
            loginForm.style.display = 'none';
            signupForm.style.display = 'block';
            showSignupBtn.style.display = 'none';
        });
    }
    
    if (backToLoginBtn) {
        backToLoginBtn.addEventListener('click', function() {
            signupForm.style.display = 'none';
            loginForm.style.display = 'block';
            showSignupBtn.style.display = 'block';
        });
    }
    
    // Toggle password visibility for login form
    if (togglePassword && passwordField && togglePasswordIcon) {
        togglePassword.addEventListener('click', function() {
            const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);
            
            // Toggle icon
            if (type === 'text') {
                togglePasswordIcon.classList.remove('fa-eye');
                togglePasswordIcon.classList.add('fa-eye-slash');
            } else {
                togglePasswordIcon.classList.remove('fa-eye-slash');
                togglePasswordIcon.classList.add('fa-eye');
            }
        });
    }
    
    // Toggle password visibility for signup form
    if (toggleSignupPassword && signupPasswordField && toggleSignupPasswordIcon) {
        toggleSignupPassword.addEventListener('click', function() {
            const type = signupPasswordField.getAttribute('type') === 'password' ? 'text' : 'password';
            signupPasswordField.setAttribute('type', type);
            
            // Toggle icon
            if (type === 'text') {
                toggleSignupPasswordIcon.classList.remove('fa-eye');
                toggleSignupPasswordIcon.classList.add('fa-eye-slash');
            } else {
                toggleSignupPasswordIcon.classList.remove('fa-eye-slash');
                toggleSignupPasswordIcon.classList.add('fa-eye');
            }
        });
    }
    
    // Job roles page functionality
    const jobRoleBtns = document.querySelectorAll('.job-role-btn');
    const skillsContainer = document.getElementById('skillsContainer');
    const skillsSection = document.getElementById('skillsSection');
    const selectedRoleName = document.getElementById('selectedRoleName');
    const selectedSkillsContainer = document.getElementById('selectedSkills');
    const clearBtn = document.getElementById('clearBtn');
    
    let selectedSkills = new Set();
    let currentRole = null;
    
    // Handle job role selection
    jobRoleBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // Remove active class from all buttons
            jobRoleBtns.forEach(b => b.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            const role = this.dataset.role;
            currentRole = role;
            
            // Update the selected role name
            selectedRoleName.textContent = role;
            
            // Fetch skills for this role
            fetchSkillsForRole(role);
        });
    });
    
    // Fetch skills from API
    async function fetchSkillsForRole(role) {
        try {
            const response = await fetch(`/api/skills/${encodeURIComponent(role)}`);
            const data = await response.json();
            
            // Clear existing skills
            skillsContainer.innerHTML = '';
            
            // Create container for category boxes
            const categoriesContainer = document.createElement('div');
            categoriesContainer.className = 'row g-3';
            
            // Create a box for each category
            Object.keys(data.skills).forEach(category => {
                const categoryBox = document.createElement('div');
                categoryBox.className = 'col-md-6 col-lg-4';
                
                const card = document.createElement('div');
                card.className = 'card category-card h-100';
                
                // Category header
                const cardHeader = document.createElement('div');
                cardHeader.className = 'card-header category-header';
                cardHeader.innerHTML = `<h6 class="mb-0">${category}</h6>`;
                
                // Category body with skills
                const cardBody = document.createElement('div');
                cardBody.className = 'card-body p-2';
                
                const skillsGrid = document.createElement('div');
                skillsGrid.className = 'skills-grid';
                
                // Add skills as clickable badges
                data.skills[category].forEach(skill => {
                    const skillBadge = document.createElement('span');
                    skillBadge.className = 'skill-badge-item';
                    skillBadge.dataset.skill = skill;
                    skillBadge.textContent = skill;
                    skillBadge.style.cursor = 'pointer';
                    
                    // Add click handler
                    skillBadge.addEventListener('click', function() {
                        if (!selectedSkills.has(skill)) {
                            addSkill(skill);
                            this.classList.add('selected');
                            this.style.cursor = 'default';
                        }
                    });
                    
                    skillsGrid.appendChild(skillBadge);
                });
                
                cardBody.appendChild(skillsGrid);
                card.appendChild(cardHeader);
                card.appendChild(cardBody);
                categoryBox.appendChild(card);
                categoriesContainer.appendChild(categoryBox);
            });
            
            skillsContainer.appendChild(categoriesContainer);
            
            // Show skills section
            skillsSection.style.display = 'block';
            
        } catch (error) {
            console.error('Error fetching skills:', error);
        }
    }
    
    // Add skill to selected skills
    function addSkill(skill) {
        if (!selectedSkills.has(skill)) {
            selectedSkills.add(skill);
            renderSelectedSkills();
        }
    }
    
    // Remove skill from selected skills
    function removeSkill(skill) {
        selectedSkills.delete(skill);
        renderSelectedSkills();
        
        // Reset the skill badge state
        const skillBadge = skillsContainer.querySelector(`[data-skill="${skill}"]`);
        if (skillBadge) {
            skillBadge.classList.remove('selected');
            skillBadge.style.cursor = 'pointer';
        }
    }
    
    // Render selected skills as badges
    function renderSelectedSkills() {
        selectedSkillsContainer.innerHTML = '';
        
        selectedSkills.forEach(skill => {
            const badge = document.createElement('span');
            badge.className = 'skill-badge';
            badge.innerHTML = `
                ${skill}
                <span class="remove-skill" data-skill="${skill}">&times;</span>
            `;
            
            // Add click handler for remove button
            const removeBtn = badge.querySelector('.remove-skill');
            removeBtn.addEventListener('click', function() {
                removeSkill(this.dataset.skill);
            });
            
            selectedSkillsContainer.appendChild(badge);
        });
    }
    
    // Clear all selections
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            // Clear selected skills
            selectedSkills.clear();
            renderSelectedSkills();
            
            // Clear job role selection
            jobRoleBtns.forEach(btn => btn.classList.remove('active'));
            
            // Reset all skill badges
            const skillBadges = skillsContainer.querySelectorAll('.skill-badge-item');
            skillBadges.forEach(badge => {
                badge.classList.remove('selected');
                badge.style.cursor = 'pointer';
            });
            
            // Hide skills section
            skillsSection.style.display = 'none';
            
            currentRole = null;
        });
    }
});