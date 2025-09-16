#!/usr/bin/env python3
"""
Email Test Script for JobForSLSG
Tests Gmail SMTP configuration before deployment
"""

import os
import sys
from flask import Flask
from flask_mail import Mail, Message

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Create test Flask app
app = Flask(__name__)

# Configure with your settings
app.config.update(
    MAIL_SERVER=os.environ.get('MAIL_SERVER', 'smtp.gmail.com'),
    MAIL_PORT=int(os.environ.get('MAIL_PORT', 587)),
    MAIL_USE_TLS=os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true',
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME', 'fdodinuth@gmail.com'),
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD', 'cvgt jwog kckt zpcq'),
    MAIL_DEFAULT_SENDER=os.environ.get('MAIL_DEFAULT_SENDER', 'fdodinuth@gmail.com')
)

mail = Mail(app)

def test_email():
    """Test email sending functionality"""
    try:
        with app.app_context():
            # Create test message
            msg = Message(
                subject="🧪 JobForSLSG Email Test",
                recipients=[app.config['MAIL_DEFAULT_SENDER']],
                html="""
                <h2>✅ Email Test Successful!</h2>
                <p>This is a test email from JobForSLSG application.</p>
                <p><strong>Configuration:</strong></p>
                <ul>
                    <li>MAIL_SERVER: {}</li>
                    <li>MAIL_PORT: {}</li>
                    <li>MAIL_USE_TLS: {}</li>
                    <li>MAIL_USERNAME: {}</li>
                </ul>
                <p>🎉 Your email configuration is working perfectly!</p>
                """.format(
                    app.config['MAIL_SERVER'],
                    app.config['MAIL_PORT'],
                    app.config['MAIL_USE_TLS'],
                    app.config['MAIL_USERNAME']
                )
            )
            
            # Send email
            mail.send(msg)
            print("✅ SUCCESS: Test email sent successfully!")
            print(f"📧 Email sent to: {app.config['MAIL_DEFAULT_SENDER']}")
            return True
            
    except Exception as e:
        print(f"❌ ERROR: Failed to send test email")
        print(f"Error details: {str(e)}")
        return False

if __name__ == '__main__':
    print("🧪 Testing JobForSLSG Email Configuration...")
    print("=" * 50)
    
    # Test email
    if test_email():
        print("=" * 50)
        print("🎉 Email configuration is ready for production!")
    else:
        print("=" * 50)
        print("⚠️  Please check your email configuration before deploying.")