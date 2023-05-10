const Router = require("express").Router;
const StatusCodes = require("http-status-codes").StatusCodes;

const providerController = require("../../controllers/provider.js");
const date = require("../../utils/date.js");

const router = Router();

router.get("/", async (req, res, next) => {

    const opts = {
        gender: req.query.gender,
        speciality: req.query.speciality,
        city: req.query.city,
        state: req.query.state,
    }

    const providersRes = await providerController.findMany(opts);

    res.send(providersRes);
});

router.get("/:providerID", async (req, res, next) => {
    const id = req.params.providerID;

    if (!id) {
        res.status(400).send({
            error: "missing provider ID",
        })
        return;
    }

    const providerRes = await providerController.find(id);
    return res.send(providerRes);
});

router.put("/:providerID", async (req, res, next) => {
    const id = req.params.providerID;

    if (!id) {
        res.status(400).send({
            error: "missing provider ID",
        })
        return;
    }

    const providerRes = await providerController.update(id, req.body);
    return res.send(providerRes);
});

router.delete("/:providerID", async (req, res, next) => {
    const id = req.params.providerID;

    if (!id) {
        res.status(400).send({
            error: "missing provider ID",
        })
        return;
    }

    const providerRes = await providerController.delete(id);
    return res.send(providerRes);
});

router.get("/:providerID/encounters", async (req, res, next) => {
    const id = req.params.providerID;

    if (!id) {
        res.status(400).send({
            error: "missing provider ID",
        })
        return;
    }

    const startRes = date.getIsoDate(req.query.start);

    if (startRes && startRes.error) {
        res.status(400).send(startRes);
        return;
    }

    const endRes = date.getIsoDate(req.query.end);

    if (endRes && endRes.error) {
        res.status(400).send(endRes);
        return;
    }

    const opts = {
        start: startRes? startRes : date.isoDateEpoch(),
        end: endRes? endRes : date.isoDateNow(),
        patient: req.params.patient,
        class: req.params.class,
        code: req.params.code,
        payer: req.params.payer,
    }

    const encounters = await providerController.findEncounters(id, opts);

    if (encounters.error) {
        res.status(404).send(encounters);
        return;
    }
    res.send(encounters);

});

module.exports = (app) => {
    app.use("/provider", router);
};