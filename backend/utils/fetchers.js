const axios = require('axios');
const RateLimiter = require('./rateLimiter');

const nvdRateLimiter = new RateLimiter(600); // 0.6 seconds

async function fetchCPEsFromNVD(product, version) {
  return nvdRateLimiter.makeRequest(async () => {
    try {
      const apiKey = process.env.NVD_API_KEY;
      const response = await axios.get(
        `https://services.nvd.nist.gov/rest/json/cpes/2.0?keywordSearch=${encodeURIComponent(product)}`,
        { headers: { apiKey } }
      );

      return response.data.products.map(product => ({
        cpe23Uri: product.cpe.cpeName,
        versionStartExcluding: product.cpe.versionStartExcluding,
        versionEndExcluding: product.cpe.versionEndExcluding,
        versionEndIncluding: product.cpe.versionEndIncluding,
        versionStartIncluding: product.cpe.versionStartIncluding,
        cpe_name: product.cpe.cpe23Uri ? [{ cpe23Uri: product.cpe.cpe23Uri }] : []
      }));
    } catch (error) {
      console.error(`Error fetching CPEs for ${product} ${version}:`, error);
      return [];
    }
  });
}

async function fetchCVEsFromNVD(cpe23Uri) {
  return nvdRateLimiter.makeRequest(async () => {
    try {
      const apiKey = process.env.NVD_API_KEY;
      const response = await axios.get(
        `https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName=${encodeURIComponent(cpe23Uri)}`,
        { headers: { apiKey } }
      );

      return response.data.vulnerabilities.map(vuln => ({
        id: vuln.cve.id,
        description: vuln.cve.descriptions[0]?.value || '',
        cvssScore: vuln.cve.metrics?.cvssMetricV31?.[0]?.cvssData?.baseScore || 0,
        publishedDate: vuln.cve.published,
        lastModifiedDate: vuln.cve.lastModified
      }));
    } catch (error) {
      console.error(`Error fetching CVEs for ${cpe23Uri}:`, error);
      return [];
    }
  });
}

module.exports = { fetchCPEsFromNVD, fetchCVEsFromNVD };
