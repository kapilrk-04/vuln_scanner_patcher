const express = require('express');
const { fetchCPEsFromNVD, fetchCVEsFromNVD } = require('../utils/fetchers');
const summarizeVulnerabilities = require('../utils/summarizer');
const CPECache = require('../models/cpe');
const CVE = require('../models/cve');

const router = express.Router();

router.post('/api/analyze', async (req, res) => {
  try {
    const { applications } = req.body;
    const results = [];

    for (const app of applications) {
      const { vendor, product, version } = app;
      const searchKey = `${product}:${version}`;

      let cpeCache = await CPECache.findOne({ searchKey });
      if (!cpeCache || Date.now() - cpeCache.lastUpdated > 24 * 60 * 60 * 1000) {
        const cpes = await fetchCPEsFromNVD(product, version);
        if (cpeCache) {
          cpeCache.matches = cpes;
          cpeCache.lastUpdated = Date.now();
          await cpeCache.save();
        } else {
          cpeCache = await CPECache.create({ searchKey, matches: cpes });
        }
      }

      const matchingCPE = cpeCache.matches[0];
      if (!matchingCPE) continue;

      let cveData = await CVE.findOne({ cpe23Uri: matchingCPE.cpe23Uri });
      if (!cveData || Date.now() - cveData.lastUpdated > 24 * 60 * 60 * 1000) {
        const cves = await fetchCVEsFromNVD(matchingCPE.cpe23Uri);
        if (cveData) {
          cveData.cves = cves;
          cveData.lastUpdated = Date.now();
          await cveData.save();
        } else {
          cveData = await CVE.create({ cpe23Uri: matchingCPE.cpe23Uri, cves });
        }
      }

      const vulnerabilitySummary = summarizeVulnerabilities(cveData.cves);
      if (vulnerabilitySummary.totalCount > 0) {
        results.push({ application: app, cpe: matchingCPE, vulnerability_summary: vulnerabilitySummary });
      }
    }

    res.json({ results });
  } catch (error) {
    console.error('Error processing request:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;
