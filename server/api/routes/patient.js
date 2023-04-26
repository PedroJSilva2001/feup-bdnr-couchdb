const Router = require("express").Router;
const StatusCodes = require("http-status-codes").StatusCodes;

const router = Router();

router.get("/", (req, res, next) => {
    return res.status(StatusCodes.OK).json({
        ok: true,
    });
});

module.exports = (app) => {
    app.use("/patient", router);
};