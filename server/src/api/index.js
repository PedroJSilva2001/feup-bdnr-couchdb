const Router = require("express").Router;
const patient = require("./routes/patient.js");

module.exports = () => {
    const app = Router();

    patient(app);

    return app;
};