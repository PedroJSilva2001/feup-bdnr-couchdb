const express = require("express");
//import { StatusCodes, HTTPStatus } from "http-status-codes";
const session = require("express-session");

const StatusCodes = require("http-status-codes").StatusCodes;
const apiRoutes = require("../api/index.js");
const defaultErrorHandler = require("../api/middleware/errorHandler.js").defaultErrorHandler;

module.exports = (app) => {
    app.use(express.json());

    // Heartbeat
    app.get("/", (_, res, next) => {
        res.status(StatusCodes.OK).json({ "up": true });
    });

    app.use(apiRoutes());

    //app.use(defaultErrorHandler);
};