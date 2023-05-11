const db = require("../couchdb/db.js");

module.exports.getByKey = async (ddoc, view, key) => {
    const res = await db.get().view(ddoc, view, {
        key: key,
    });

    console.log(res)

    if (res.rows.length === 0) {
        return {
            "result": {}
        };
    }
    return {
        "result": res.rows[0].value[0]
    };
}

module.exports.getByKeyNumberValue = async (ddoc, view, key) => {
    const res = await db.get().view(ddoc, view, {
        key: key,
    });

    console.log(res)

    if (res.rows.length === 0) {
        return {
            "result": {}
        };
    }
    return {
        "result": res.rows[0].value
    };
}

module.exports.getBetweenKeys = async (ddoc, view, keyMaxSize, startKey, endKey) => {
    const groupLevel = startKey.length;
    endKey = endKey? endKey : [];
    endKey = endKey.concat(Array(keyMaxSize - endKey.length).fill({}));
    console.log(startKey)
    console.log(endKey)
    const res = await db.get().view(ddoc, view, {
        startkey: startKey,
        endkey: endKey,
        group: true,
        group_level: groupLevel
    });

    return {
        results: res.rows
    };
}