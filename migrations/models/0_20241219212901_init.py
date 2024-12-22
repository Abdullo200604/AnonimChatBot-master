from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "user_id" BIGINT NOT NULL UNIQUE,
    "full_name" VARCHAR(255) NOT NULL,
    "username" VARCHAR(100) NOT NULL UNIQUE,
    "is_connected" BOOL NOT NULL  DEFAULT False
);
CREATE TABLE IF NOT EXISTS "plans" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "user_id" BIGINT NOT NULL,
    "plan_time" VARCHAR(20),
    "plan_text" VARCHAR(500) NOT NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
