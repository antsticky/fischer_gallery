db = db.getSiblingDB('admin');
print("Authenticating as root...");
db.auth(process.env.MONGO_INITDB_ROOT_USERNAME, process.env.MONGO_INITDB_ROOT_PASSWORD);
print("Authentication successful.");

db = db.getSiblingDB(process.env.MONGO_DB_NAME);
print("Creating collections...");
db.createCollection('stocks');
db.createCollection('logs');
db.createCollection('usersdb');
print("Collections created.");

print("Creating roles...");
db.createRole({
  role: "readStocksAndLogsCollections",
  privileges: [
    {
      resource: {
        db: process.env.MONGO_DB_NAME,
        collection: "stocks"
      },
      actions: ["find"]
    },
    {
      resource: {
        db: process.env.MONGO_DB_NAME,
        collection: "logs"
      },
      actions: ["find"]
    }
  ],
  roles: []
});

db.createRole({
  role: "readwriteStocksAndLogsCollections",
  privileges: [
    {
      resource: {
        db: process.env.MONGO_DB_NAME,
        collection: "stocks"
      },
      actions: ["find", "insert", "update", "remove"]
    },
    {
      resource: {
        db: process.env.MONGO_DB_NAME,
        collection: "logs"
      },
      actions: ["find", "insert", "update", "remove"]
    }
  ],
  roles: []
});

db.createRole({
  role: "readWriteUserCollections",
  privileges: [
    {
      resource: { 
        db: process.env.MONGO_DB_NAME,
        collection: "usersdb"
      },
      actions: ["find", "listCollections", "collStats", "insert", "update", "remove"]
    }
  ],
  roles: []
});

db.createRole({
  role: "readUserCollections",
  privileges: [
    {
      resource: { 
        db: process.env.MONGO_DB_NAME,
        collection: "usersdb"
      },
      actions: ["find"]
    }
  ],
  roles: []
});
print("Roles created.");

print("Creating users...");
db.createUser({
  user: process.env.MONGO_READ_WRITE_USER,
  pwd: process.env.MONGO_READ_WRITE_PASSWORD,
  roles: [
    {
      role: 'readwriteStocksAndLogsCollections',
      db: process.env.MONGO_DB_NAME,
    }
  ],
});

db.createUser({
  user: process.env.MONGO_READ_USERNAME,
  pwd: process.env.MONGO_READ_PASSWORD,
  roles: [
    {
      role: 'readStocksAndLogsCollections',
      db: process.env.MONGO_DB_NAME,
    }
  ],
});

db.createUser({
  user: process.env.MONGO_USER_READ_USERNAME,
  pwd: process.env.MONGO_USER_READ_PASSWORD,
  roles: [
    {
      role: "readUserCollections",
      db: "gallery"
    }
  ]
});

db.createUser({
  user: process.env.MONGO_USER_ADMIN_USERNAME,
  pwd: process.env.MONGO_USER_ADMIN_PASSWORD,
  roles: [
    {
      role: "readWriteUserCollections",
      db: "gallery"
    }
  ]
});
print("Users created.");
