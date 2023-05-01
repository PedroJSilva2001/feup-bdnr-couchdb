const Router = require("express").Router;
const StatusCodes = require("http-status-codes").StatusCodes;

const patientController = require("../../controllers/patient.js");

const router = Router();

router.get("/:patientSSN", async (req, res, next) => {
    const ssn = req.params.patientSSN;
    const patient = await patientController.find(ssn);
    if (patient.error) {
        res.status(404).send(patient);
        return;
    }
    res.send(patient);
});

router.get("/:patientSSN/encounters", async (req, res, next) => {
    const ssn = req.params.patientSSN;

    if (!(await patientController.exists(ssn))) {
        res.status(404).send({
            error: "patient with that ssn doesn't exist",
        });
        return;
    }

    const startDate = !req.query.start? null : new Date(req.query.start);
    if (startDate && isNaN(startDate.getTime())) {
        res.status(400).send({
            "error": "invalid start date parameter",
        })
    }
    const start = !startDate? [null, null, null] : 
                    [
                        ""+startDate.getUTCFullYear(), 
                        (""+(startDate.getUTCMonth()+1)).padStart(2, "0"), 
                        (""+startDate.getUTCDate()).padStart(2, "0"),
                    ]

    const endDate = !req.query.end? null : new Date(req.query.end);
    if (endDate && isNaN(endDate.getTime())) {
        res.status(400).send({
            "error": "invalid end date parameter",
        })
    }

    const end = !endDate? 
                    [{}, {}, {}] : [
                        ""+endDate.getUTCFullYear(), 
                        (""+(endDate.getUTCMonth()+1)).padStart(2, "0"), 
                        (""+endDate.getUTCDate()).padStart(2, "0"),
                    ];

    const encounters = await patientController.findEncounters(ssn, start, end);
    res.send(encounters);
});

router.get("/:patientSSN/encounters/:encounterID", async (req, res, next) => {
    const ssn = req.params.patientSSN;
    const encounterID = req.params.encounterID;

    if (!(await patientController.exists(ssn))) {
        res.status(404).send({
            error: "patient with that ssn doesn't exist",
        });
        return;
    }

    const encounter = await patientController.findEncounter(ssn, encounterID);
    res.send(encounter);
});

module.exports = (app) => {
    app.use("/patient", router);
};