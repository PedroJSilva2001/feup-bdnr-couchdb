const db = require("../couchdb/db.js");
const providerIndex = require("../couchdb/ddoc-functions/indexes/provider.js");

const info = [
    "id",
    "name",
    "gender",
    "speciality",
    "address",
    "city",
    "state",
    "zip",
    "lat",
    "lon",
    "organization",
];

module.exports.exists = async (id) => {
    return !(await this.find(id)).error;
};

module.exports.find = async (id) => {
    const q = {
        selector: {
          doc_type: "provider",
          id: id
        },
        //fields: [ "_id", ...info ],
        use_index: [`_design/${providerIndex.idIndex.ddoc}`, providerIndex.idIndex.name]
    };

    const response = await db.get().find(q);

    if (response.docs.length == 0) {
        return {
            error: "provider with that id doesn't exist",
        }
    }

    return {
        provider: response.docs[0],
    };
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

module.exports.findMany = async (opts) => {
    const q = {
        selector: {
          doc_type: "provider",
        },
        //fields: [ "_id", ...info ],
        use_index: [`_design/${providerIndex.idIndex.ddoc}`, providerIndex.idIndex.name]
    };

    if (opts.gender) {
        q.selector.gender = opts.gender;
    }

    if (opts.speciality) {
        q.selector.speciality = opts.speciality;
    }

    if (opts.city) {
        q.selector.city = opts.city;
    }

    if (opts.state) {
        q.selector.state = opts.state;
    }

    const response = await db.get().find(q);

    return {
        providers: response.docs,
    };
}

module.exports.findEncounters = async (id, opts) => {
    const providerRes = await this.find(id);
    if (providerRes.error) {
        return providerRes;
    }

    console.log(opts)
    if (opts.patient) {
        const q = {
            selector: {
                doc_type: "encounter",
                "provider.id": id,
                "patient.id": opts.patient
            },
            //fields: [ "_id", ...info ],
            use_index: [
                        `_design/${providerIndex.encountersSpecificPatientIndex.ddoc}`, 
                        providerIndex.encountersSpecificPatientIndex.name
            ]
        };
        return await db.get().find(q).docs;
    } else {
        const q = {
            selector: {
                doc_type: "encounter",
                "provider.id": id,
                "start": {
                    "$gte": opts.start,
                    "$lte": opts.end

                },
            },
            //fields: [ "_id", ...info ],
            use_index: [
                        `_design/${providerIndex.encountersFiltersIndex.ddoc}`, 
                        providerIndex.encountersFiltersIndex.name
            ]
        };

        if (opts.code) {
            q.selector.code = parseInt(opts.code);
        }

        if (opts.class) {
            q.selector.encounter_class = opts.class;
        }

        if (opts.payer) {
            q.selector.payer = opts.payer;
        }
        
        console.log(q);
        return (await db.get().find(q)).docs;
    }
};

module.exports.update = async (id, provider) => {
    provider["doc_type"] = "provider";
    provider["id"] = id;

    const providerRes = await this.find(id);

    if (providerRes.error) {
        provider["_id"] = id;
        const res = await db.get().insert(provider);
        console.log(res);
        return {};
    }

    provider["_id"] = providerRes.provider._id;
    provider["_rev"] = providerRes.provider._rev;

    const res = await db.get().insert(provider);
    console.log(res);
    return {};
};

module.exports.delete = async (id) => {
    const providerRes = await this.find(id);

    if (providerRes.error) {
        return providerRes;
    }

    const res = await db.get().destroy(providerRes.provider._id, providerRes.provider._rev);
    console.log(res);
    return {};
};