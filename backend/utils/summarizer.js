function summarizeVulnerabilities(cves) {
    const severityCounts = { critical: 0, high: 0, medium: 0, low: 0 };
    if (!cves || cves.length === 0) return { totalCount: 0, mostCritical: null, severityCounts };

    let mostCritical = cves[0];

    cves.forEach(cve => {
      const score = cve.cvssScore;
      if (score >= 9.0) severityCounts.critical++;
      else if (score >= 7.0) severityCounts.high++;
      else if (score >= 4.0) severityCounts.medium++;
      else if (score > 0) severityCounts.low++;

      if (score > mostCritical.cvssScore) mostCritical = cve;
    });

    return { totalCount: cves.length, most_critical: mostCritical, severity_counts: severityCounts };
}

module.exports = summarizeVulnerabilities;
