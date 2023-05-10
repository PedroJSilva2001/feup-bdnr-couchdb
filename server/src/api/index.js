const Router = require("express").Router;
const patient = require("./routes/patient.js");
const provider = require("./routes/provider.js");

module.exports = () => {
    const app = Router();

    patient(app);

    provider(app);

    return app;
};