const db = require("../couchdb/db.js");

module.exports.exists = async (ssn) => {
    return !(await this.find(ssn)).error;
};

module.exports.find = async (ssn) => {
    const response = await db.get().view("patient-view-ddoc", "basic", {
        key: ssn,
        reduce: false
    });

    if (response.rows.length == 0) {
        return {
            error: "patient with that ssn doesn't exist",
        }
    }

    return {
        patient: response.rows[0].value
    };
};

// Assumes the patient exists
module.exports.findEncounters = async (ssn, start, end) => {
    const response = await db.get().view("patient-view-ddoc", "encounters", {
        start_key: [ssn, null, ...start],
        end_key: [ssn, {}, ...end],
        reduce: false
    });

    return {
        encounters: response.rows.map((row) => {
            return row.value;
        }),
    };
};

// Assumes the patient exists
module.exports.findEncounter = async (ssn, encounterID) => {
    console.log(encounterID)
    const response = await db.get().view("patient-view-ddoc", "encounters", {
        start_key: [ssn, encounterID],
        end_key: [ssn, encounterID, {}, {}, {}],
        reduce: false
    });

    if (response.rows.length == 0) {
        return {
            encounter: null,
        }
    }
    // Only an encounter should be returned
    return {
        encounter: response.rows[0],
    };
};