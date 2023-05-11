const Router = require("express").Router;
const patient = require("./routes/patient.js");
const provider = require("./routes/provider.js");
const encounterStats = require("./routes/encounterStats.js");

module.exports = () => {
    const app = Router();

    patient(app);

    provider(app);
    encounterStats(app);
    return app;
};