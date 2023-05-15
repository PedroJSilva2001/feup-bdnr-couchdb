const db = require("../couchdb/db.js");

const patientInfo = [
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

module.exports.findPatientWithSpecificCondition = async (condition) => {
    const q = {
        "selector": {
           "doc_type": "patient",
           "conditions": {
              "$elemMatch": {
                "description": {
                    "$regex": `.*${condition}.*`
                }
              }
           }
        },
        "fields": [
           ...patientInfo
        ],
        "limit": 50,
    };

    const response = await db.get().find(q);

    return {
        results: response.docs
    }
}

module.exports.findPatientByName = async (first, last) => {
    const q = {
        "selector": {
           "doc_type": "patient",
           "first": {
              "$regex": `.*${first}.*`
            },
            "last": {
                "$regex": `.*${last}.*`
            }
        },
        "fields": [
           ...patientInfo
        ],
        "limit": 50,
    }

    const response = await db.get().find(q);

    /*if (response.docs.length == 0) {
        return {
            error: "provider with that id doesn't exist",
        }
    }

    return {
        provider: response.docs[0],
    };*/

    return {
        results: response.docs
    }

}