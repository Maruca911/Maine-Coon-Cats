const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const app = express();

// Middleware
app.use(express.json());
app.use(express.static('public'));

// Database setup
const db = new sqlite3.Database('newsletter.db', (err) => {
    if (err) {
        console.error('Error opening database:', err);
    } else {
        console.log('Connected to newsletter database');
        // Create subscribers table if it doesn't exist
        db.run(`CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            subscribed_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )`);
    }
});

// Newsletter subscription endpoint
app.post('/api/subscribe', (req, res) => {
    const { email } = req.body;
    
    if (!email || !email.includes('@')) {
        return res.status(400).json({ 
            success: false, 
            message: 'Please provide a valid email address' 
        });
    }

    db.run('INSERT OR IGNORE INTO subscribers (email) VALUES (?)', [email], function(err) {
        if (err) {
            console.error('Database error:', err);
            return res.status(500).json({ 
                success: false, 
                message: 'An error occurred while processing your subscription' 
            });
        }

        if (this.changes === 0) {
            return res.status(200).json({ 
                success: true, 
                message: 'You are already subscribed to our newsletter!' 
            });
        }

        res.status(200).json({ 
            success: true, 
            message: 'Thank you for subscribing to our newsletter!' 
        });
    });
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
}); 