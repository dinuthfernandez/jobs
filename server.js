const express = require('express');
const nodemailer = require('nodemailer');
const cors = require('cors');
const app = express();
const port = process.env.PORT || 3000; // Use environment variable for port

// Middleware
app.use(express.json());
app.use(cors({
    origin: process.env.FRONTEND_URL || 'http://localhost:3000', // Restrict CORS to specific origin
    methods: ['POST'], // Allow only POST requests
    credentials: true // Allow credentials if needed
}));

// Configure Nodemailer transporter
const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: process.env.EMAIL_USER || 'fdodinuth@gmail.com', // Use environment variable for email
        pass: process.env.EMAIL_PASS || 'cvgt jwog kckt zpcq' // Use environment variable for app password
    }
});

// Input validation middleware
const validateApplication = (req, res, next) => {
    const { name, email, phone, age, gender, address, education, experience, details, date } = req.body;
    if (!name || !email || !phone || !age || !gender || !address || !education || !experience || !details || !date) {
        return res.status(400).json({ error: 'All fields are required' });
    }
    if (!/\S+@\S+\.\S+/.test(email)) {
        return res.status(400).json({ error: 'Invalid email format' });
    }
    next();
};

const validateSupport = (req, res, next) => {
    const { name, email, message } = req.body;
    if (!name || !email || !message) {
        return res.status(400).json({ error: 'All fields are required' });
    }
    if (!/\S+@\S+\.\S+/.test(email)) {
        return res.status(400).json({ error: 'Invalid email format' });
    }
    next();
};

// Endpoint for job applications
app.post('/send-application', validateApplication, async (req, res) => {
    const { name, email, phone, age, gender, address, education, experience, details, date } = req.body;

    const mailOptions = {
        from: `"Job Application" <${process.env.EMAIL_USER || 'fdodinuth@gmail.com'}>`, // Formatted sender
        to: process.env.EMAIL_USER || 'fdodinuth@gmail.com', // Receiver
        subject: `New Job Application from ${name}`,
        text: `Name: ${name}\nEmail: ${email}\nPhone: ${phone}\nAge: ${age}\nGender: ${gender}\nAddress: ${address}\nEducation: ${education}\nExperience: ${experience}\nDetails: ${details}\nApplied On: ${date}`,
        html: `
            <h3>New Job Application</h3>
            <p><strong>Name:</strong> ${name}</p>
            <p><strong>Email:</strong> ${email}</p>
            <p><strong>Phone:</strong> ${phone}</p>
            <p><strong>Age:</strong> ${age}</p>
            <p><strong>Gender:</strong> ${gender}</p>
            <p><strong>Address:</strong> ${address}</p>
            <p><strong>Education:</strong> ${education}</p>
            <p><strong>Experience:</strong> ${experience}</p>
            <p><strong>Details:</strong> ${details}</p>
            <p><strong>Applied On:</strong> ${date}</p>
        `
    };

    try {
        const info = await transporter.sendMail(mailOptions);
        res.status(200).json({ message: 'Email sent successfully', response: info.response });
    } catch (error) {
        console.error('Error sending email:', error);
        res.status(500).json({ error: 'Failed to send email' });
    }
});

// Endpoint for support messages
app.post('/send-support', validateSupport, async (req, res) => {
    const { name, email, message } = req.body;

    const mailOptions = {
        from: `"Support Request" <${process.env.EMAIL_USER || 'fdodinuth@gmail.com'}>`, // Formatted sender
        to: process.env.EMAIL_USER || 'fdodinuth@gmail.com', // Receiver
        subject: `Support Request from ${name}`,
        text: `Name: ${name}\nEmail: ${email}\nMessage: ${message}`,
        html: `
            <h3>New Support Request</h3>
            <p><strong>Name:</strong> ${name}</p>
            <p><strong>Email:</strong> ${email}</p>
            <p><strong>Message:</strong> ${message}</p>
        `
    };

    try {
        const info = await transporter.sendMail(mailOptions);
        res.status(200).json({ message: 'Email sent successfully', response: info.response });
    } catch (error) {
        console.error('Error sending email:', error);
        res.status(500).json({ error: 'Failed to send email' });
    }
});

// Serve static files (if hosting frontend)
app.use(express.static(__dirname));

// Error handling middleware
app.use((err, req, res, next) => {
    console.error('Server error:', err.stack);
    res.status(500).json({ error: 'Something went wrong on the server' });
});

// Start server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});