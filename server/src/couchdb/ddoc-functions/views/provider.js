module.exports.info = function(doc) {
    if (doc.doc_type == "provider") {
        emit([
                doc.id, doc.speciality, doc.state, doc.city, 
                doc.organization.id, doc.organization.state, doc.organization.city
            ], {
                id: doc.id,
                name: doc.name,
                gender: doc.gender,
                speciality: doc.speciality,
                address: doc.address,
                city: doc.city,
                state: doc.state,
                zip: doc.zip,
                lat: doc.lat,
                lon: doc.lon,
                organization: doc.organization 
        });
    }
};

module.exports.encountersBasic = function(doc) {
    if (doc.doc_type == "encounter") {
        const start = doc.start;
        const dateFields = start.split(/[-T:Z]/);
        const year = parseInt(dateFields[0]);
        const month = parseInt(dateFields[1]);
        const day = parseInt(dateFields[2]);
        emit([
                doc.provider.id,
                doc.id,
                year,
                month,
                day,
                doc.patient.id,
                doc.encounter_class,
                doc.code,
                doc.payer.id
            ], {
                id: doc.id,
                start: doc.start,
                stop: doc.stop,
                encounter_class: doc.encounter_class,
                code: doc.code,
                description: doc.description,
                base_encounter_cost: doc.base_encounter_cost,
                total_claim_cost: doc.total_claim_cost,
                payer_coverage: doc.payer_coverage,
                reason_code: doc.reason_code,
                reason_description: doc.reason_description,
                patient: doc.patient,
                organization: doc.organization,
                payer: doc.payer
        });
    }
};

/*
module.exports.encountersComplete = function(doc) {
    if (doc.doc_type = "encounter") {
        const start = doc.start;
        const dateFields = start.split(/[-T:Z]/);
        const year = dateFields[0];
        const month = dateFields[1];
        const day = dateFields[2];
        emit([
                doc.provider.id,
                doc.id,
                year,
                month,
                day,
                doc.patient.id,
                doc.payer.id,
                doc.encounter_class,
                doc.code
        ], doc);
    }
}

*/