module.exports = Object.freeze({
    // CouchDB
    couchdb_host: process.env.COUCHDB_HOST,
    couchdb_port: process.env.COUCHDB_HTTP_PORT,
    couchdb_user: process.env.COUCHDB_USER,
    couchdb_password: process.env.COUCHDB_PASSWORD,
    couchdb_db: process.env.COUCHDB_DB,

    // Server
    port: process.env.PORT || 8888,
});