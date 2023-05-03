const expressLoader = require("./express.js");
const couchdbLoader = require("./couchdb.js");

module.exports = async ( { expressApp }) => {
    console.info("Initializing Express..");
    expressLoader(expressApp);
    console.info("Express was initialized");

    console.info("Connecting to couchdb server..");
    await couchdbLoader()
    console.info("Connected to couchdb server");
};
