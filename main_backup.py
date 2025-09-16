from flask import Flask, render_template_string, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'fdodinuth@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'cvgt jwog kckt zpcq')

mail = Mail(app)

# Single Warehouse Job Application (Original)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🇱🇰🇸🇬 JobForSLSG - Warehouse Job Application</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        :root {
            --primary: #0066CC;
            --primary-dark: #004499;
            --secondary: #6366F1;
            --success: #059669;
            --warning: #D97706;
            --danger: #DC2626;
            --dark: #1F2937;
            --dark-light: #374151;
            --light: #F9FAFB;
            --white: #FFFFFF;
            --gray-100: #F3F4F6;
            --gray-200: #E5E7EB;
            --gray-300: #D1D5DB;
            --gray-600: #4B5563;
            --gray-700: #374151;
            --gray-800: #1F2937;
            --glass-bg: rgba(255, 255, 255, 0.95);
            --glass-border: rgba(255, 255, 255, 0.2);
            --shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            --shadow-hover: 0 20px 40px rgba(0, 0, 0, 0.15);
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, 
                #667eea 0%, 
                #764ba2 25%, 
                #f093fb 50%, 
                #f5576c 75%, 
                #4facfe 100%);
            background-size: 400% 400%;
            animation: gradientShift 20s ease infinite;
            min-height: 100vh;
            color: var(--dark);
            line-height: 1.6;
            position: relative;
            overflow-x: hidden;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Floating orbs */
        .orb {
            position: fixed;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            animation: float 6s ease-in-out infinite;
            z-index: 1;
        }
        
        .orb:nth-child(1) {
            width: 80px;
            height: 80px;
            top: 20%;
            left: 10%;
            animation-delay: 0s;
        }
        
        .orb:nth-child(2) {
            width: 120px;
            height: 120px;
            top: 60%;
            right: 15%;
            animation-delay: 2s;
        }
        
        .orb:nth-child(3) {
            width: 60px;
            height: 60px;
            bottom: 20%;
            left: 20%;
            animation-delay: 4s;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            33% { transform: translateY(-20px) rotate(120deg); }
            66% { transform: translateY(10px) rotate(240deg); }
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 2;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 40px;
            box-shadow: var(--shadow);
            position: relative;
            overflow: hidden;
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
        }
        
        .header h1 {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
            letter-spacing: -1px;
        }
        
        .header .subtitle {
            font-size: 1.2rem;
            color: var(--gray-600);
            font-weight: 500;
        }
        
        .job-card {
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: var(--shadow);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .job-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-hover);
        }
        
        .job-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--success), var(--primary));
        }
        
        .job-title {
            font-size: 2rem;
            font-weight: 700;
            color: var(--dark);
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .job-meta {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 25px 0;
        }
        
        .meta-item {
            text-align: center;
            padding: 20px;
            background: rgba(255, 255, 255, 0.7);
            border-radius: 16px;
            border: 1px solid var(--gray-200);
            transition: all 0.3s ease;
        }
        
        .meta-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }
        
        .meta-label {
            font-size: 0.9rem;
            color: var(--gray-600);
            margin-bottom: 5px;
            font-weight: 500;
        }
        
        .meta-value {
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--dark);
        }
        
        .salary {
            color: var(--success) !important;
            font-size: 1.4rem !important;
        }
        
        .job-description {
            font-size: 1.1rem;
            color: var(--gray-700);
            line-height: 1.8;
            margin: 25px 0;
        }
        
        .requirements {
            margin: 30px 0;
        }
        
        .requirements h3 {
            font-size: 1.3rem;
            color: var(--dark);
            margin-bottom: 15px;
            font-weight: 700;
        }
        
        .requirements ul {
            list-style: none;
            padding: 0;
        }
        
        .requirements li {
            padding: 12px 0;
            border-bottom: 1px solid var(--gray-200);
            font-size: 1rem;
            color: var(--gray-700);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .requirements li::before {
            content: '✓';
            color: var(--success);
            font-weight: 700;
            font-size: 1.2rem;
        }
        
        .urgent-notice {
            background: rgba(220, 38, 38, 0.1);
            border: 1px solid rgba(220, 38, 38, 0.3);
            border-radius: 12px;
            padding: 20px;
            margin: 25px 0;
            color: var(--danger);
            font-weight: 600;
        }
        
        .application-form {
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 40px;
            margin-top: 30px;
            box-shadow: var(--shadow);
            position: relative;
            overflow: hidden;
        }
        
        .application-form::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
        }
        
        .form-title {
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--dark);
            margin-bottom: 25px;
            text-align: center;
        }
        
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group.full-width {
            grid-column: 1 / -1;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: var(--gray-700);
            font-size: 0.95rem;
        }
        
        input, textarea, select {
            width: 100%;
            padding: 16px 20px;
            background: var(--white);
            border: 2px solid var(--gray-200);
            border-radius: 12px;
            font-size: 1rem;
            color: var(--dark);
            transition: all 0.3s ease;
            font-family: inherit;
        }
        
        input:focus, textarea:focus, select:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
            transform: translateY(-2px);
        }
        
        .required {
            color: var(--danger);
        }
        
        .submit-btn {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: var(--white);
            padding: 18px 40px;
            border: none;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: inherit;
            position: relative;
            overflow: hidden;
            width: 100%;
            margin-top: 20px;
        }
        
        .submit-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(0, 102, 204, 0.4);
        }
        
        .submit-btn:disabled {
            background: var(--gray-300);
            cursor: not-allowed;
            transform: none;
        }
        
        .contact-info {
            background: linear-gradient(135deg, var(--dark), var(--dark-light));
            color: var(--white);
            padding: 30px;
            border-radius: 16px;
            text-align: center;
            margin-top: 30px;
        }
        
        .contact-info h3 {
            margin-bottom: 20px;
            font-size: 1.4rem;
        }
        
        .contact-links {
            display: flex;
            justify-content: center;
            gap: 15px;
            flex-wrap: wrap;
        }
        
        .contact-link {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 12px 24px;
            background: rgba(255, 255, 255, 0.1);
            color: var(--white);
            text-decoration: none;
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .contact-link:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
        }
        
        .message {
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
            font-weight: 600;
            text-align: center;
        }
        
        .success {
            background: rgba(5, 150, 105, 0.1);
            color: var(--success);
            border: 1px solid rgba(5, 150, 105, 0.3);
        }
        
        .error {
            background: rgba(220, 38, 38, 0.1);
            color: var(--danger);
            border: 1px solid rgba(220, 38, 38, 0.3);
        }
        
        .hidden {
            display: none;
        }
        
        .loading {
            position: relative;
        }
        
        .loading::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 20px;
            height: 20px;
            margin: -10px 0 0 -10px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-top: 2px solid var(--white);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 15px;
            }
            
            .header {
                padding: 30px 20px;
            }
            
            .header h1 {
                font-size: 2.2rem;
            }
            
            .job-card, .application-form {
                padding: 30px 20px;
            }
            
            .job-title {
                font-size: 1.6rem;
            }
            
            .form-grid {
                grid-template-columns: 1fr;
            }
            
            .job-meta {
                grid-template-columns: 1fr;
            }
            
            .contact-links {
                flex-direction: column;
                align-items: center;
            }
        }
    </style>
</head>
<body>
    <!-- Floating orbs -->
    <div class="orb"></div>
    <div class="orb"></div>
    <div class="orb"></div>

    <div class="container">
        <div class="header">
            <h1>🇱🇰🇸🇬 JobForSLSG</h1>
            <p class="subtitle">Connecting Sri Lankan talent with Singapore opportunities</p>
        </div>

        <div class="job-card">
            <div class="job-title">
                🏭 Warehouse Staff (Night Shift) - Immediate Opening
            </div>
            
            <div class="job-meta">
                <div class="meta-item">
                    <div class="meta-label">Monthly Salary</div>
                    <div class="meta-value salary">SGD 2,400</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Job Type</div>
                    <div class="meta-value">Full Time</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Location</div>
                    <div class="meta-value">West Singapore</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Shift Hours</div>
                    <div class="meta-value">8:00 PM - 6:00 AM</div>
                </div>
            </div>

            <div class="job-description">
                Join our dynamic warehouse team in Singapore! We're looking for dedicated individuals to handle inventory management, order fulfillment, and logistics operations. This is a permanent position with excellent growth opportunities within our expanding logistics network. Full training provided for all new employees.
            </div>

            <div class="urgent-notice">
                <strong>⚠️ Important Note:</strong> There is a SGD 100 fee for the company security card which will be deducted from your first salary.
            </div>

            <div class="requirements">
                <h3>📋 Job Requirements</h3>
                <ul>
                    <li>Age between 18-55 years old</li>
                    <li>Physically fit and able to lift up to 25kg</li>
                    <li>Basic English communication skills</li>
                    <li>Reliable and punctual</li>
                    <li>No previous experience required - training provided</li>
                    <li>Able to work night shifts</li>
                </ul>
            </div>
        </div>

        <div class="application-form">
            <h2 class="form-title">📝 Apply for This Position</h2>
            
            <form id="applicationForm">
                <div class="form-grid">
                    <div class="form-group">
                        <label for="name">Full Name <span class="required">*</span></label>
                        <input type="text" id="name" name="name" required placeholder="Enter your full name">
                    </div>
                    
                    <div class="form-group">
                        <label for="email">Email Address <span class="required">*</span></label>
                        <input type="email" id="email" name="email" required placeholder="your.email@example.com">
                    </div>
                    
                    <div class="form-group">
                        <label for="phone">Phone Number <span class="required">*</span></label>
                        <input type="tel" id="phone" name="phone" required placeholder="+94 71 234 5678">
                    </div>
                    
                    <div class="form-group">
                        <label for="age">Age <span class="required">*</span></label>
                        <input type="number" id="age" name="age" min="18" max="55" required placeholder="25">
                    </div>
                    
                    <div class="form-group">
                        <label for="gender">Gender <span class="required">*</span></label>
                        <select id="gender" name="gender" required>
                            <option value="">Select Gender</option>
                            <option value="Male">Male</option>
                            <option value="Female">Female</option>
                            <option value="Other">Other</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="nationality">Nationality <span class="required">*</span></label>
                        <input type="text" id="nationality" name="nationality" required placeholder="e.g., Sri Lankan">
                    </div>
                    
                    <div class="form-group full-width">
                        <label for="address">Complete Address <span class="required">*</span></label>
                        <textarea id="address" name="address" rows="3" required placeholder="Your complete address (include city, province/state)"></textarea>
                    </div>
                    
                    <div class="form-group full-width">
                        <label for="experience">Work Experience</label>
                        <textarea id="experience" name="experience" rows="4" placeholder="Describe your previous work experience, skills, and relevant qualifications (optional but recommended)"></textarea>
                    </div>
                    
                    <div class="form-group full-width">
                        <label for="availability">When can you start? <span class="required">*</span></label>
                        <select id="availability" name="availability" required>
                            <option value="">Select availability</option>
                            <option value="Immediately">Immediately</option>
                            <option value="Within 1 week">Within 1 week</option>
                            <option value="Within 2 weeks">Within 2 weeks</option>
                            <option value="Within 1 month">Within 1 month</option>
                        </select>
                    </div>
                </div>
                
                <button type="submit" class="submit-btn" id="submitBtn">
                    🚀 Submit Application
                </button>
            </form>
            
            <div id="message" class="message hidden"></div>
        </div>

        <div class="contact-info">
            <h3>📞 Contact Information</h3>
            <div class="contact-links">
                <a href="tel:+94761244231" class="contact-link">
                    📱 Call: +94 76 124 4231
                </a>
                <a href="https://wa.link/eh4ehx" target="_blank" class="contact-link">
                    💬 WhatsApp
                </a>
                <a href="mailto:fdodinuth@gmail.com" class="contact-link">
                    📧 Email Us
                </a>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('applicationForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitBtn = document.getElementById('submitBtn');
            const messageDiv = document.getElementById('message');
            
            // Show loading state
            submitBtn.disabled = true;
            submitBtn.textContent = 'Submitting Application...';
            submitBtn.classList.add('loading');
            messageDiv.className = 'message hidden';
            
            // Get form data
            const formData = {
                name: document.getElementById('name').value.trim(),
                email: document.getElementById('email').value.trim(),
                phone: document.getElementById('phone').value.trim(),
                age: document.getElementById('age').value,
                gender: document.getElementById('gender').value,
                nationality: document.getElementById('nationality').value.trim(),
                address: document.getElementById('address').value.trim(),
                experience: document.getElementById('experience').value.trim(),
                availability: document.getElementById('availability').value
            };
            
            try {
                const response = await fetch('/submit-application', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    messageDiv.textContent = '✅ Application submitted successfully! We will contact you within 24 hours.';
                    messageDiv.className = 'message success';
                    document.getElementById('applicationForm').reset();
                    
                    // Scroll to message
                    messageDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
                } else {
                    messageDiv.textContent = '❌ ' + (result.error || 'Failed to submit application');
                    messageDiv.className = 'message error';
                }
            } catch (error) {
                console.error('Submission error:', error);
                messageDiv.textContent = '❌ Network error. Please check your connection and try again.';
                messageDiv.className = 'message error';
            }
            
            // Reset button state
            setTimeout(() => {
                submitBtn.disabled = false;
                submitBtn.textContent = '🚀 Submit Application';
                submitBtn.classList.remove('loading');
            }, 2000);
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Serve the main application"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/submit-application', methods=['POST'])
def submit_application():
    """Handle form submission and send email"""
    try:
        from markupsafe import escape

        data = request.json or {}

        # Safely extract and escape all fields
        name = escape(data.get('name', 'N/A'))
        email_addr = escape(data.get('email', 'N/A'))
        phone = escape(data.get('phone', 'N/A'))
        age = escape(str(data.get('age', 'N/A')))
        gender = escape(data.get('gender', 'N/A'))
        nationality = escape(data.get('nationality', 'N/A'))
        address = escape(data.get('address', 'N/A'))
        availability = escape(data.get('availability', 'N/A'))
        experience = escape(data.get('experience', 'No experience provided'))

        # Create email content
        subject = f"🎯 New Job Application - JobForSLSG"

        # Email body with all the details
        body = f"""
        <h2>🎯 New Job Application - JobForSLSG</h2>
        
        <h3>📋 Applicant Information:</h3>
        <ul>
            <li><strong>Name:</strong> {name}</li>
            <li><strong>Email:</strong> {email_addr}</li>
            <li><strong>Phone:</strong> {phone}</li>
            <li><strong>Age:</strong> {age}</li>
            <li><strong>Gender:</strong> {gender}</li>
            <li><strong>Nationality:</strong> {nationality}</li>
            <li><strong>Address:</strong> {address}</li>
            <li><strong>Availability:</strong> {availability}</li>
        </ul>
        
        <h3>💼 Work Experience:</h3>
        <p>{experience}</p>
        
        <hr>
        <p><em>Application submitted through JobForSLSG platform</em></p>
        """

        # Send email
        msg = Message(subject, recipients=['fdodinuth@gmail.com'])
        msg.html = body
        mail.send(msg)

        return jsonify({'success': True, 'message': 'Application submitted successfully!'})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to submit application'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)