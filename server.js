// server.js
// Express backend for JobForSLSG with CORS + email sending
require('dotenv').config();
const express = require('express');
const cors = require('cors');
const nodemailer = require('nodemailer');

const app = express();
const PORT = process.env.PORT || 3000;

// ---- In-memory storage for pending orders ----
let applications = [];

// --- CORS ---
// In production, you can restrict origins to your frontend domain(s).
app.use(cors({
  origin: true, // allow all origins for now
  methods: ['GET', 'POST', 'OPTIONS'],
  allowedHeaders: ['Content-Type'],
}));

// --- JSON parsing ---
app.use(express.json({ limit: '1mb' }));

// --- Health check ---
app.get('/', (_req, res) => {
  res.json({ ok: true, service: 'JobForSLSG backend', time: new Date().toISOString() });
});

// --- Email transport ---
// Configure SMTP via environment variables on Render dashboard.
const transporter = nodemailer.createTransport({
  host: process.env.SMTP_HOST,
  port: Number(process.env.SMTP_PORT || 587),
  secure: process.env.SMTP_SECURE === 'true', // true for port 465
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS,
  },
});

async function sendMail({ subject, html }) {
  if (!process.env.SMTP_HOST || !process.env.SMTP_USER || !process.env.SMTP_PASS || !process.env.TO_EMAIL) {
    console.warn('Email not configured. Set SMTP_HOST, SMTP_USER, SMTP_PASS, TO_EMAIL in environment.');
    return { ok: false, skipped: true };
  }
  const fromEmail = process.env.FROM_EMAIL || process.env.SMTP_USER;
  await transporter.sendMail({
    from: fromEmail,
    to: process.env.TO_EMAIL,
    subject,
    html,
  });
  return { ok: true };
}

// --- Routes ---
app.post('/send-application', async (req, res) => {
  try {
    const { name, email, phone, age, gender, address, education, experience, details, date } = req.body || {};
    if (!name || !email || !phone) {
      return res.status(400).json({ ok: false, error: 'Missing required fields (name, email, phone).' });
    }

    // Save to in-memory list with Pending status
    const application = {
      name,
      email,
      phone,
      age,
      gender,
      address,
      education,
      experience,
      details,
      date: date || new Date().toLocaleString(),
      status: 'Pending',
    };
    applications.push(application);

    const subject = `New Job Application from ${name}`;
    const html = `
      <h2>New Job Application</h2>
      <p><strong>Name:</strong> ${name}</p>
      <p><strong>Email:</strong> ${email}</p>
      <p><strong>Phone:</strong> ${phone}</p>
      <p><strong>Age:</strong> ${age || ''}</p>
      <p><strong>Gender:</strong> ${gender || ''}</p>
      <p><strong>Address:</strong> ${address || ''}</p>
      <p><strong>Education:</strong> ${education || ''}</p>
      <p><strong>Experience:</strong> ${experience || ''}</p>
      <p><strong>Details:</strong> ${details || ''}</p>
      <p><strong>Applied On:</strong> ${application.date}</p>
    `;

    const mailResult = await sendMail({ subject, html });
    if (mailResult.ok) {
      return res.json({ ok: true, sent: true });
    } else if (mailResult.skipped) {
      return res.status(501).json({ ok: false, error: 'Email not configured on server.' });
    } else {
      return res.status(500).json({ ok: false, error: 'Failed to send email.' });
    }
  } catch (err) {
    console.error('send-application error:', err);
    return res.status(500).json({ ok: false, error: 'Server error.' });
  }
});

app.post('/send-support', async (req, res) => {
  try {
    const { name, email, message } = req.body || {};
    if (!name || !email || !message) {
      return res.status(400).json({ ok: false, error: 'Missing required fields (name, email, message).' });
    }

    const subject = `Support Message from ${name}`;
    const html = `
      <h2>Support Message</h2>
      <p><strong>Name:</strong> ${name}</p>
      <p><strong>Email:</strong> ${email}</p>
      <p><strong>Message:</strong></p>
      <p>${String(message).replace(/</g, '&lt;')}</p>
    `;

    const mailResult = await sendMail({ subject, html });
    if (mailResult.ok) {
      return res.json({ ok: true, sent: true });
    } else if (mailResult.skipped) {
      return res.status(501).json({ ok: false, error: 'Email not configured on server.' });
    } else {
      return res.status(500).json({ ok: false, error: 'Failed to send email.' });
    }
  } catch (err) {
    console.error('send-support error:', err);
    return res.status(500).json({ ok: false, error: 'Server error.' });
  }
});

// --- New route to get all pending applications ---
app.get('/applications', (req, res) => {
  res.json({ ok: true, applications });
});

// --- Start server ---
app.listen(PORT, () => {
  console.log('Server running on port', PORT);
});
