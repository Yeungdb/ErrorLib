CREATE TABLE IF NOT EXISTS "Error" (
    "ErrorIndex" SERIAL NOT NULL PRIMARY KEY,
    "ErrorTag" TEXT NOT NULL,
    "ErrorName" TEXT NOT NULL,
    "ErrorMessage" TEXT NOT NULL,
    "ReturnToUserMessage" TEXT NOT NULL,
    "AuthorName" TEXT NOT NULL,
    "Approved" BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS "ErrorLog" (
    "ErrorLogIndex" SERIAL NOT NULL PRIMARY KEY,
    "CurrentTime" DATE,
    "AppWhereErrorOccurred" TEXT,
    "ServerName" TEXT,
    "CodeWhereErrorFailed" TEXT,
    "VariableNameArray" TEXT,
    "VariableValueArray" TEXT
);

CREATE TABLE IF NOT EXISTS "Users" (
    "UserID" SERIAL NOT NULL PRIMARY KEY,
    "Password" TEXT NOT NULL,
    "UserRole" TEXT NOT NULL
);
