module.exports.idIndex = {
    "index": {
        "fields": [
            "id",
            "doc_type"
        ]
    },
    "ddoc": "providers-ddoc",
    "name": "providers-id-index",
    "type": "json",
    "partitioned": false
};

module.exports.filtersIndex = {
    "index": {
        "fields": [
            "doc_type",
            "gender",
            "speciality",
            "city",
            "state",
        ]
    },
    "ddoc": "providers-ddoc",
    "name": "providers-filters-index",
    "type": "json",
    "partitioned": false
};

module.exports.encountersFiltersIndex = {
    "index": {
        "fields": [
            "doc_type",
            "provider.id",
            "start",
            "code",
            "encounter_class",
            "payer.id",  
        ]
    },
    "ddoc": "providers-ddoc",
    "name": "encounters-index",
    "type": "json",
    "partitioned": false
}

module.exports.encountersSpecificPatientIndex = {
    "index": {
        "fields": [
            "doc_type",
            "provider.id",
            "patient.id", 
        ]
    },
    "ddoc": "providers-ddoc",
    "name": "encounters-specific-patient-index",
    "type": "json",
    "partitioned": false
}