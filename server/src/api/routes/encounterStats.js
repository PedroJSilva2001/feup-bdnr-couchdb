const Router = require("express").Router;
const StatusCodes = require("http-status-codes").StatusCodes;

const encounterStatsController = require("../../controllers/encounterStats.js");

const router = Router();

router.get("/allergy-incidence", async (req, res, next) => {
    const key = req.query.key? JSON.parse(req.query.key) : null;
    const startKey = req.query.startkey? JSON.parse(req.query.startkey) : null;
    const endKey = req.query.endkey? JSON.parse(req.query.endkey) : null;

    if (key && key.length != 3) {
        res.status(400).send({
            error: "allergy incidence key is incomplete",
        })
        return;
    }

    if (key && (startKey || endKey)) {
        res.status(400).send({
            error: "can't use allergy incidence key with start or end keys",
        })
        return;
    }

    if (key) {
        const statsRes = await encounterStatsController.getAllergyIncidenceByKey(key);
        res.send(statsRes);
        return
    }

    if (endKey && !startKey) {
        res.status(400).send({
            error: "missing incidence start key",
        })
        return;
    }


    const statsRes = await encounterStatsController.getAllergyIncidenceBetweenKeys(startKey, endKey);
    res.send(statsRes)
});

router.get("/payer-coverage", async (req, res, next) => {
    const key = req.query.key? JSON.parse(req.query.key) : null;
    const startKey = req.query.startkey? JSON.parse(req.query.startkey) : null;
    const endKey = req.query.endkey? JSON.parse(req.query.endkey) : null;

    if (key && key.length != 2) {
        res.status(400).send({
            error: "payer coverage key is incomplete",
        })
        return;
    }

    if (key && (startKey || endKey)) {
        res.status(400).send({
            error: "can't use payer coverage key with start or end keys",
        })
        return;
    }

    if (key) {
        const statsRes = await encounterStatsController.getPayerCoverageByKey(key);
        res.send(statsRes);
        return
    }

    if (endKey && !startKey) {
        res.status(400).send({
            error: "missing payer coverage start key",
        })
        return;
    }


    const statsRes = await encounterStatsController.getPayerCoverageBetweenKeys(startKey, endKey);
    res.send(statsRes)
});

router.get("/patient-evolution", async (req, res, next) => {
    const key = req.query.key? JSON.parse(req.query.key) : null;
    const startKey = req.query.startkey? JSON.parse(req.query.startkey) : null;
    const endKey = req.query.endkey? JSON.parse(req.query.endkey) : null;

    if (key && key.length != 4) {
        res.status(400).send({
            error: "patient evolution key is incomplete",
        })
        return;
    }

    if (key && (startKey || endKey)) {
        res.status(400).send({
            error: "can't use patient evolution key with start or end keys",
        })
        return;
    }

    if (key) {
        const statsRes = await encounterStatsController.getPatientEvolutionByKey(key);
        res.send(statsRes);
        return
    }

    if (endKey && !startKey) {
        res.status(400).send({
            error: "missing patient evolution start key",
        })
        return;
    }


    const statsRes = await encounterStatsController.getPatientEvolutionBetweenKeys(startKey, endKey);
    res.send(statsRes)
});

module.exports = (app) => {
    app.use("/encounter-stats", router);
};