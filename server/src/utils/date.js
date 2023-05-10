module.exports.getIsoDate = (date) => {
    const isoDate = !date? null: new Date(date);

    if (isoDate && isNaN(isoDate.getTime())) {
        return {
            "error": "invalid date parameter",
        };
    }

    return isoDate;
};

module.exports.isoDateNow = () => {
    return new Date().toISOString();
}

module.exports.isoDateEpoch = () => {
    return new Date("1900/01/01").toISOString();
}