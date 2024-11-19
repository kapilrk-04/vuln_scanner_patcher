const mongoose = require('mongoose');
const { Schema } = mongoose;

const cpeSchema = new Schema({
  searchKey: { type: String, required: true },
  matches: [{
    cpe23Uri: { type: String, required: true },
    versionStartExcluding: String,
    versionEndExcluding: String,
    versionEndIncluding: String,
    versionStartIncluding: String,
    cpe_name: [{
      cpe23Uri: String
    }]
  }],
  lastUpdated: { type: Date, default: Date.now }
});

cpeSchema.index({ searchKey: 1 }, { unique: true });

module.exports = mongoose.model('CPECache', cpeSchema);
