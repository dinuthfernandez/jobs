const express = require('express');
const nodemailer = require('nodemailer');
const cors = require('cors');
const app = express();
const port = 3000;

app.use(express.json());
app.use(cors()); // Allow cross-origin requests from frontend

// Configure Nodemailer transporter (use your Gmail credentials)
// IMPORTANT: Replace 'your-email@gmail.com' and 'your-app-password' with actual values.
// If using Gmail with 2FA, generate an App Password: https://myaccount.google.com/apppasswords
const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: 'your-email@gmail.com', // Your Gmail address
        pass: 'your-app-password'     // App password (not your regular password)
    }
});

// Endpoint for job applications
app.post('/send-application', (req, res) => {
    const { name, email, phone, age, gender, address, education, experience, details, date } = req.body;

    const mailOptions = {
        from: 'your-email@gmail.com', // Sender address (must match auth user)
        to: 'fdodinuth@gmail.com',    // Receiver (your email)
        subject: `New Job Application from ${name}`,
        text: `Name: ${name}\nEmail: ${email}\nPhone: ${phone}\nAge: ${age}\nGender: ${gender}\nAddress: ${address}\nEducation: ${education}\nExperience: ${experience}\nDetails: ${details}\nApplied On: ${date}`
    };

    transporter.sendMail(mailOptions, (error, info) => {
        if (error) {
            console.error(error);
            return res.status(500).send('Error sending email');
        }
        res.send('Email sent: ' + info.response);
    });
});

// Endpoint for support messages
app.post('/send-support', (req, res) => {
    const { name, email, message } = req.body;

    const mailOptions = {
        from: 'your-email@gmail.com', // Sender address
        to: 'fdodinuth@gmail.com',    // Receiver
        subject: `Support Request from ${name}`,
        text: `Name: ${name}\nEmail: ${email}\nMessage: ${message}`
    };

    transporter.sendMail(mailOptions, (error, info) => {
        if (error) {
            console.error(error);
            return res.status(500).send('Error sending email');
        }
        res.send('Email sent: ' + info.response);
    });
});

// Optional: Serve the frontend statically (if you want to host HTML from the same server)
app.use(express.static(__dirname)); // Serves index.html at http://localhost:3000/index.html

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});