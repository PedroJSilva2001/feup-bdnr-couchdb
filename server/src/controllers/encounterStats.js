const db = require("../couchdb/db.js");
const viewUtils = require("../utils/view.js");

module.exports.getAllergyIncidenceByKey = async (key) => {
    return await viewUtils.getByKey("encounter-stats-view-ddoc", "allergy_frequency", key);
}

module.exports.getAllergyIncidenceBetweenKeys = async (startKey, endKey) => {
    return await viewUtils.getBetweenKeys("encounter-stats-view-ddoc", "allergy_frequency", 3, startKey, endKey);
}

module.exports.getPayerCoverageByKey = async (key) => {
    return await viewUtils.getByKeyNumberValue("encounter-stats-view-ddoc", "payer_coverage", key);
}

module.exports.getPayerCoverageBetweenKeys = async (startKey, endKey) => {
    return await viewUtils.getBetweenKeys("encounter-stats-view-ddoc", "payer_coverage", 2, startKey, endKey);
}

module.exports.getPatientEvolutionByKey = async (key) => {
    return await viewUtils.getByKeyNumberValue("encounter-stats-view-ddoc", "patient_evolution", key);
}

module.exports.getPatientEvolutionBetweenKeys = async (startKey, endKey) => {
    return await viewUtils.getBetweenKeys("encounter-stats-view-ddoc", "patient_evolution", 4, startKey, endKey);
}