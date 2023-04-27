const nano = require("nano");

const config = require("../config/env.js");

const db = nano(
    `http://${config.couchdb_user}:${config.couchdb_password}@${config.couchdb_host}:${config.couchdb_port}`
).use("healthtracks");

module.exports = db;

