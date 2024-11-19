const mongoose = require('mongoose');
const { Schema } = mongoose;

const cveSchema = new Schema({
  cpe23Uri: { type: String, required: true },
  cves: [{
    id: String,
    description: String,
    cvssScore: Number,
    publishedDate: Date,
    lastModifiedDate: Date
  }],
  lastUpdated: { type: Date, default: Date.now }
});

cveSchema.index({ cpe23Uri: 1 }, { unique: true });

module.exports = mongoose.model('CVECache', cveSchema);
