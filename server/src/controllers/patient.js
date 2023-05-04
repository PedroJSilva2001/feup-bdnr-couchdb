const db = require("../couchdb/db.js");

const patientIndexes = require("../couchdb/ddoc-functions/indexes/patient.js");


const nonAggregatedInfo = [
    "ssn",
    "birthdate",
    "deathdate",
    "drivers",
    "passport",
    "prefix",
    "first",
    "last",
    "suffix",
    "maiden",
    "marital",
    "race",
    "ethnicity",
    "gender",
    "birthplace",
    "address",
    "city",
    "state",
    "county",
    "fips",
    "zip",
    "lat",
    "lon",
];

/*const aggregatedInfo = [
    "allergies",
    "careplans",
    "conditions",
    "devices",
    "imaging_studies",
    "immunizations",
    "medications",
    "observations",
    "procedures",
    "encounters",
    "payer_transitions",
    "claims",
];*/

module.exports.exists = async (ssn) => {
    return !(await this.find(ssn)).error;
};

module.exports.find = async (ssn) => {
    const q = {
        selector: {
          doc_type: "patient",
          ssn: ssn
        },
        fields: [ "_id", ...nonAggregatedInfo ],
        use_index: [`_design/${patientIndexes.ssnIndex.ddoc}`, patientIndexes.ssnIndex.name]
    };

    const response = await db.get().find(q);

    if (response.docs.length == 0) {
        return {
            error: "patient with that ssn doesn't exist",
        }
    }

    return {
        patient: response.docs[0],
    };
};

module.exports.findAggregations = async (ssn, aggregationName) => {
    const q = {
        selector: {
          doc_type: "patient",
          ssn: ssn
        },
        fields: [ "_id", aggregationName ],
        use_index: [`_design/${patientIndexes.ssnIndex.ddoc}`, patientIndexes.ssnIndex.name]
    };

    const response = await db.get().find(q);

    if (response.docs.length == 0) {
        return {
            error: "patient with that ssn doesn't exist",
        }
    }

    const res = {};

    res[aggregationName] = response.docs[0][aggregationName]

    return res;

};

/*
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
};*/

module.exports.findEncounter = async (ssn, encounterID) => {
    const q = {
        selector: {
          doc_type: "patient",
          ssn: ssn
        },
        fields: [ "encounters" ],
        use_index: [`_design/${patientIndexes.ssnIndex.ddoc}`, patientIndexes.ssnIndex.name]
    };

    const response = await db.get().find(q);

    if (response.docs.length == 0) {
        return {
            error: "patient with that ssn doesn't exist",
        }
    }

    return {
        patient: response.docs[0],
    };
    return response;
/*        return {
            error: "patient with that ssn doesn't exist",
        };
*/

    /*console.log(encounterID)
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
        encounter: response.rows[0].value,
    };*/
};