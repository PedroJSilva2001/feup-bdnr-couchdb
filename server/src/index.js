const config = require("./config/env.js")
const loaders = require("./loaders/index.js")
const express = require("express");
const http = require("http");

const app = express();

const startServer = async () => {
    await loaders({ expressApp: app });

    app.set('port', config.port);

    const server = http.createServer(app);

    server.listen(config.port, (err) => {
        if (err) {
            console.error(err);
            return;
        }

        console.info(`Server listening on port ${config.port}`);
    });
}

startServer();