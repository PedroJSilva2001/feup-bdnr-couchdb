const Router = require("express").Router;
const StatusCodes = require("http-status-codes").StatusCodes;

const keywordSearchController = require("../../controllers/keywordSearch.js");

const router = Router();

router.get("/patient-by-name", async (req, res, next) => {
    const first = req.query.first;
    const last = req.query.last;

    if (!first) {
        res.status(400).send({
            error: "missing patient first name",
        })
        return;
    }
    if (!last) {
        res.status(400).send({
            error: "missing patient last name",
        })
        return;
    }

    const searchRes = await keywordSearchController.findPatientByName(first, last);

    res.send(searchRes);
});

router.get("/patient-by-condition", async (req, res, next) => {
    const condition = req.query.condition;

    if (!condition) {
        res.status(400).send({
            error: "missing patient condition",
        })
        return;
    }

    const searchRes = await keywordSearchController.findPatientWithSpecificCondition(condition);

    res.send(searchRes);
});

module.exports = (app) => {
    app.use("/keyword-search", router);
};