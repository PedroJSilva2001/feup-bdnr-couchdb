const nano = require("nano");
const fs = require("fs").promises;
const path = require('path');

const config = require("../config/env.js");
const db = require("../couchdb/db.js");
//const patientViewFunctions = require("../couchdb/ddoc-functions/views/patient.js");
//const providerViewFunctions = require("../couchdb/ddoc-functions/views/provider.js");
const encounterStats = require("../couchdb/ddoc-functions/views/encounterStats.js");
const patientIndexes = require("../couchdb/ddoc-functions/indexes/patient.js");
const providerIndexes = require("../couchdb/ddoc-functions/indexes/provider.js");

const server = nano(
    `http://${config.couchdb_user}:${config.couchdb_password}@${config.couchdb_host}:${config.couchdb_port}`
);


const loadDocuments = async (db) => {
    const batchesListFilename = (await fs.readdir("./datasets")).filter(file => {
        return path.extname(file).toLowerCase() === '.txt';
    })[0];

    const batchesInfo = (await fs.readFile(`./datasets/${batchesListFilename}`, "utf8"))
                        .split("\n")
                        .map(info => {
                            const split = info.split(" ");
                            return {
                                    timestamp: split[0],
                                    state: split[1],
                                }
                        });
    console.log(batchesInfo)
    
    for (const info of batchesInfo) {
        let batch = [];

        const patients = (await fs.readdir(`./datasets/${info.timestamp}_${info.state}/patients`, "utf8"));

        for (const patient of patients) {
            const data = await fs.readFile(`./datasets/${info.timestamp}_${info.state}/patients/${patient}`, 'utf8');
            batch.push(JSON.parse(data));
        }

        await db.bulk({docs: batch});

        batch = [];

        const encounters = (await fs.readdir(`./datasets/${info.timestamp}_${info.state}/encounters`, "utf8"));

        for (const encounter of encounters) {
            const data = await fs.readFile(`./datasets/${info.timestamp}_${info.state}/encounters/${encounter}`, 'utf8');
            batch.push(JSON.parse(data));
        }

        await db.bulk({docs: batch});

        batch = [];

        const providers = (await fs.readdir(`./datasets/${info.timestamp}_${info.state}/providers`, "utf8"));

        for (const provider of providers) {
            const data = await fs.readFile(`./datasets/${info.timestamp}_${info.state}/providers/${provider}`, 'utf8');
            batch.push(JSON.parse(data));
        }

        await db.bulk({docs: batch});
    }
};

const loadDesignDocuments = async (db) => {
    let res = await db.createIndex(patientIndexes.ssnIndex);
    console.log(res);

    res = await db.createIndex(providerIndexes.idIndex);
    console.log(res);
    
    res = await db.createIndex(providerIndexes.encountersFiltersIndex);
    console.log(res);

    res = await db.createIndex(providerIndexes.encountersSpecificPatientIndex);
    console.log(res);

    res = await db.insert({
        _id: "_design/encounter-stats-view-ddoc",
        views: {
            allergy_frequency: {
                map: encounterStats.allergyMap.toString(),
                reduce: encounterStats.allergyReduce.toString()
            },
            payer_coverage: {
                map: encounterStats.payerCoverageMap.toString(),
                reduce: encounterStats.payerCoverageReduce.toString()
            }
        }
    });

    /*
    const patientViewInsertResponse = await db.insert({
        _id: "_design/patient-view-ddoc",
        views: {
            basic: {
                map: patientViewFunctions.nonAggregatedInfo.toString(),
                reduce: "_count"
            },
            encounters: {
                map: patientViewFunctions.encounters.toString(),
                reduce: "_count"
            }
        }
    });
    console.log(patientViewInsertResponse);

    const providerViewInsertResponse = await db.insert({
        _id: "_design/provider-view-ddoc",
        views: {
            info: {
                map: providerViewFunctions.info.toString(),
                reduce: "_count"
            },
            encounters_basic: {
                map: providerViewFunctions.encountersBasic.toString(),
                reduce: "_count"
            }
        }
    });
    console.log(providerViewInsertResponse);*/
};

module.exports = async () => {
    try {
        const response = await server.db.create(config.couchdb_db);
        console.log(response);
        console.log("Didn't find Healthtracks database. Creating one..");
        const db_ = await server.use(config.couchdb_db)
        db.set(db_);
        await loadDesignDocuments(db_);
        await loadDocuments(db_);
    } catch (e) {
        console.log(e)
        if (e.error === "file_exists" ) {
            console.log("Database already exists");
            const db_ = await server.db.use(config.couchdb_db)
            db.set(db_)
        }
    }
};

