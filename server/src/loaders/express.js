const express = require("express");
const StatusCodes = require("http-status-codes").StatusCodes;

const apiRoutes = require("../api/index.js");

module.exports = (app) => {
    app.use(express.json());

    // Heartbeat
    app.get("/", (_, res, next) => {
        res.status(StatusCodes.OK).json({ "up": true });
    });

    app.use(apiRoutes());
};