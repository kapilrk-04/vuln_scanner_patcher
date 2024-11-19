const express = require('express');
const connectDB = require('./config/db');
const analyzeRoutes = require('./routes/analyze');

const app = express();
app.use(express.json());

// Connect to DB
connectDB();

// Routes
app.use(analyzeRoutes);

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
