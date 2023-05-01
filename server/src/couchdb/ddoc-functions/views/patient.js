module.exports.nonAggregatedInfo = function(doc) {
    if (doc.doc_type == "patient") {
        emit(doc.ssn, {
            id: doc.id,
            birthdate: doc.birthdate,
            deathdate: doc.deathdate,
            drivers: doc.drivers,
            passport: doc.passport,
            prefix: doc.prefix,
            first: doc.first,
            last: doc.last,
            suffix: doc.suffix,
            maiden: doc.maiden,
            marital: doc.marital,
            race: doc.race,
            ethnicity: doc.ethnicity,
            gender: doc.gender,
            birthplace: doc.birthplace,
            address: doc.address,
            city: doc.city,
            state: doc.state,
            county: doc.county,
            fips: doc.fips,
            zip: doc.zip,
            lat: doc.lat,
            lon: doc.lon,
        });
    }
};

module.exports.encounters = function(doc) {
    if (doc.doc_type == "patient") {
        for (const encounter of doc.encounters) {
            const start = encounter.start;
            const dateFields = start.split(/[-T:Z]/);
            const year = dateFields[0];
            const month = dateFields[1];
            const day = dateFields[2];
            emit([doc.ssn, encounter.id, year, month, day], encounter);
        }
    }
};