const expressLoader = require("./express.js");

module.exports = ( { expressApp }) => {
    console.info("Initializing Express..");
    expressLoader(expressApp);
    console.info("Express was initialized");
};
