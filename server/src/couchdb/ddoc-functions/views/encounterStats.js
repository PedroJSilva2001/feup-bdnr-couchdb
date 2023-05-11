module.exports.payerCoverageMap = function(doc) {
    if (doc.doc_type === "encounter") {
        emit([doc.reason_code, doc.payer.id], doc.payer_coverage);
    }
};

module.exports.payerCoverageReduce = function(keys, values, rereduce) {
    return sum(values)/values.length;
}

module.exports.allergyMap = function(doc) {
    if (doc.doc_type === "encounter") {
        for (const allergy of doc.allergies) {
            if (allergy.type === "allergy") {
                emit([allergy.code, doc.patient.state, doc.patient.city], {
                    description: allergy.description,
                    category: allergy.category,
                    count: 1
              });
            }    
        }
    }
}

module.exports.allergyReduce = function(keys, values, rereduce) {
    if (rereduce) {
        return values;
    } else {
        return values.reduce((a, b) => {
                return {
                    description: a.description,
                    category: a.category,
                    count: a.count + b.count
                };
        });
    }
}


module.exports.patientEvolutionMap = function(doc) {
    if (doc.doc_type === "patient") {
        for (const condition of doc.conditions) {
            const start = new Date(condition.start);
            const stop = new Date(condition.stop);
            const duration = (stop.getTime() - start.getTime())/(1000 * 60 * 60 * 24);
            
            emit([doc.ssn, condition.code, condition.start, condition.stop], {
                code: condition.code,
                description: condition.description,
                earliest: condition.start,
                latest: condition.start,
                start: condition.start,
                stop: condition.stop,
                count: 1,
                incidenceDuration: duration,
                maxIncidenceDuration: duration
            });
        }
    }
}

module.exports.patientEvolutionReduce = function(keys, values, rereduce) {
    const result = {
        count: 0, 
        earliest: null, 
        latest: null, 
        incidenceDuration: 0,
        maxIncidenceDuration: 0
    };
      
    for (var i = 0; i < values.length; i++) {
        const value = values[i];
        result.code = value.code;
        result.description = value.description;
        result.count += value.count;
    
        if (!result.earliest || value.earliest < result.earliest) {
          result.earliest = value.earliest;
        }
    
        if (!result.latest || value.latest > result.latest) {
          result.latest = value.latest;
        }
        
        result.incidenceDuration += value.incidenceDuration ;
          
        result.maxIncidenceDuration = Math.max(value.maxIncidenceDuration, result.maxIncidenceDuration);        
    }
    return result;
}

