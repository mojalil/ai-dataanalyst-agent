CREATE TABLE IF NOT EXISTS "users" (
    "Id" SERIAL PRIMARY KEY,
    "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "authed" BOOLEAN NOT NULL,
    "plan" ENUM('Basic', 'Premium', 'Enterprise') NOT NULL,
    "name" VARCHAR(255),
    "email" VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS "jobs" (
    "Id" SERIAL PRIMARY KEY,
    "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "parentUserId" INTEGER REFERENCES "users"("Id"),
    "status" ENUM('Completed', 'Running', 'Failed', 'Pending') NOT NULL,
    "totalDurationMs" BIGINT
);