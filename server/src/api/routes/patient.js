const Router = require("express").Router;
const StatusCodes = require("http-status-codes").StatusCodes;

const patientController = require("../../controllers/patient.js");

const router = Router();

router.get("/:patientSSN", async (req, res, next) => {
    const ssn = req.params.patientSSN;
    const patient = await patientController.find(ssn);
    /*if (patient.error) {
        res.status(404).send(patient);
        return;
    }*/
    res.send(patient);
});

router.put("/:patientSSN", async (req, res, next) => {
    const ssn = req.params.patientSSN;

    if (!ssn) {
        res.status(400).send({
            error: "missing patient SSN",
        })
        return;
    }

    const patientRes = await patientController.update(ssn);
    return res.send(patientRes);
});

router.delete("/:patientSSN", async (req, res, next) => {
    const ssn = req.params.patientSSN;

    if (!ssn) {
        res.status(400).send({
            error: "missing patient SSN",
        })
        return;
    }

    const patientRes = await patientController.delete(ssn);
    return res.send(patientRes);
});

router.get("/:patientSSN/encounters", async (req, res, next) => {
    const ssn = req.params.patientSSN;

    const response = await patientController.findAggregations(ssn, "encounters");
    res.send(response);
});

router.get("/:patientSSN/allergies", async (req, res, next) => {
    const ssn = req.params.patientSSN;

    const response = await patientController.findAggregations(ssn, "allergies");
    res.send(response);
});

router.get("/:patientSSN/careplans", async (req, res, next) => {
    const ssn = req.params.patientSSN;

    const response = await patientController.findAggregations(ssn, "careplans");
    res.send(response);
});

router.get("/:patientSSN/conditions", async (req, res, next) => {
    const ssn = req.params.patientSSN;

    const response = await patientController.findAggregations(ssn, "conditions");
    res.send(response);
});

router.get("/:patientSSN/devices", async (req, res, next) => {
    const ssn = req.params.patientSSN;

    const response = await patientController.findAggregations(ssn, "devices");
    res.send(response);
});

router.get("/:patientSSN/imaging-studies", async (req, res, next) => {
    const ssn = req.params.patientSSN;

    const response = await patientController.findAggregations(ssn, "imaging_studies");
    res.send(response);
});

router.get("/:patientSSN/immunizations", async (req, res, next) => {
    const ssn = req.params.patientSSN;

    const response = await patientController.findAggregations(ssn, "immunizations");
    res.send(response);
});

router.get("/:patientSSN/medications", async (req, res, next) => {
    const ssn = req.params.patientSSN;

    const response = await patientController.findAggregations(ssn, "medications");
    res.send(response);
});

router.get("/:patientSSN/observations", async (req, res, next) => {
    const ssn = req.params.patientSSN;

    const response = await patientController.findAggregations(ssn, "observations");
    res.send(response);
});

router.get("/:patientSSN/procedures", async (req, res, next) => {
    const ssn = req.params.patientSSN;

    const response = await patientController.findAggregations(ssn, "procedures");
    res.send(response);
});

router.get("/:patientSSN/payer-transitions", async (req, res, next) => {
    const ssn = req.params.patientSSN;

    const response = await patientController.findAggregations(ssn, "payer_transitions");
    res.send(response);
});

router.get("/:patientSSN/claims", async (req, res, next) => {
    const ssn = req.params.patientSSN;

    const response = await patientController.findAggregations(ssn, "claims");
    res.send(response);
});


module.exports = (app) => {
    app.use("/patient", router);
};