module.exports.ssnIndex = {
    "index": {
        "fields": [
            "ssn",
            "doc_type"
        ]
    },
    "ddoc": "patients-ddoc",
    "name": "patients-ssn-index",
    "type": "json",
    "partitioned": false
};

module.exports.demographicsIndex = {
    "index": {
        "fields": [
            "doc_type",
            "birthdate",
            "deathdate",
            "city",
            "state",
        ]
    },
    "ddoc": "patients-ddoc",
    "name": "patients-demographics-index",
    "type": "json",
    "partitioned": false
};