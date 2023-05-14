const express = require("express");
const StatusCodes = require("http-status-codes").StatusCodes;
const cors = require('cors');

const apiRoutes = require("../api/index.js");

module.exports = (app) => {
  // Enable CORS for all requests
  app.use(cors());

  app.use(function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header(
      "Access-Control-Allow-Methods", 
      "GET, POST, PUT, DELETE"
    );
    res.header(
      "Access-Control-Allow-Headers",
      "Origin, X-Requested-With, Content-Type, Accept"
    );
    next();
  });

  app.use(express.json());
  

  // Heartbeat
  app.get("/", (_, res, next) => {
    res.status(StatusCodes.OK).json({ up: true });
  });

  app.use(apiRoutes());

};
