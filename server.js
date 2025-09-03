const express = require('express');
const nodemailer = require('nodemailer');
const cors = require('cors');
const app = express();
const port = 3000;

// Middleware
app.use(express.json());
app.use(cors({ origin: '*' })); // Allow all origins for development; restrict in production

// Configure Nodemailer transporter
const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: 'fdodinuth@gmail.com',
        pass: 'cvgt jwog kckt zpcq'
    }
});

// Input validation middleware
const validateApplication = (req, res, next) => {
    const { name, email, phone, age, gender, address, education, experience, details, date } = req.body;
    if (!name || !email || !phone || !age || !gender || !address || !education || !experience || !date) {
        return res.status(400).json({ error: 'All application fields are required' });
    }
    if (!/^\S+@\S+\.\S+$/.test(email)) {
        return res.status(400).json({ error: 'Invalid email format' });
    }
    if (age < 18) {
        return res.status(400).json({ error: 'Age must be 18 or older' });
    }
    next();
};

const validateSupport = (req, res, next) => {
    const { name, email, message } = req.body;
    if (!name || !email || !message) {
        return res.status(400).json({ error: 'All support fields are required' });
    }
    if (!/^\S+@\S+\.\S+$/.test(email)) {
        return res.status(400).json({ error: 'Invalid email format' });
    }
    next();
};

// Endpoint for job applications
app.post('/send-application', validateApplication, async (req, res) => {
    const { name, email, phone, age, gender, address, education, experience, details, date } = req.body;

    const mailOptions = {
        from: '"JobForSLSG" <fdodinuth@gmail.com>',
        to: 'fdodinuth@gmail.com',
        subject: `New Job Application from ${name}`,
        text: `Name: ${name}\nEmail: ${email}\nPhone: ${phone}\nAge: ${age}\nGender: ${gender}\nAddress: ${address}\nEducation: ${education}\nExperience: ${experience}\nDetails: ${details}\nApplied On: ${date}`,
        html: `
            <h2>New Job Application</h2>
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
        console.error('Error sending application email:', error);
        res.status(500).json({ error: 'Failed to send email' });
    }
});

// Endpoint for support messages
app.post('/send-support', validateSupport, async (req, res) => {
    const { name, email, message } = req.body;

    const mailOptions = {
        from: '"JobForSLSG" <fdodinuth@gmail.com>',
        to: 'fdodinuth@gmail.com',
        subject: `Support Request from ${name}`,
        text: `Name: ${name}\nEmail: ${email}\nMessage: ${message}`,
        html: `
            <h2>Support Request</h2>
            <p><strong>Name:</strong> ${name}</p>
            <p><strong>Email:</strong> ${email}</p>
            <p><strong>Message:</strong> ${message}</p>
        `
    };

    try {
        const info = await transporter.sendMail(mailOptions);
        res.status(200).json({ message: 'Email sent successfully', response: info.response });
    } catch (error) {
        console.error('Error sending support email:', error);
        res.status(500).json({ error: 'Failed to send email' });
    }
});

// Serve frontend statically
app.use(express.static(__dirname));

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Internal server error' });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
