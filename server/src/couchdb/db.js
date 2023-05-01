class DB {
    set(db) {
        this.db = db;
    }

    get() {
        return this.db;
    }
};

module.exports = new DB();