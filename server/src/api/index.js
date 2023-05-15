const Router = require("express").Router;
const patient = require("./routes/patient.js");
const provider = require("./routes/provider.js");
const encounterStats = require("./routes/encounterStats.js");
const keywordSearch = require("./routes/keywordSearch.js");

module.exports = () => {
    const app = Router();

    patient(app);

    provider(app);
    encounterStats(app);
    keywordSearch(app);
    return app;
};