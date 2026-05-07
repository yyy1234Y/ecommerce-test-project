-- scripts/init.sql (精简版)
PRAGMA foreign_keys = OFF;

-- 商品表
DROP TABLE IF EXISTS "product";
CREATE TABLE "product" (
  "id" INTEGER PRIMARY KEY,
  "name" VARCHAR(100) NOT NULL,
  "price" FLOAT NOT NULL,
  "description" VARCHAR(500),
  "stock" INTEGER,
  "category" VARCHAR(50)
);

-- 测试商品
INSERT INTO "product" VALUES (1, '测试商品1', 99.9, '这是一个测试商品', 100, '电子');
INSERT INTO "product" VALUES (2, '测试商品2', 199.0, '另一个商品', 50, '服装');

-- 用户表
DROP TABLE IF EXISTS "user";
CREATE TABLE "user" (
  "id" INTEGER PRIMARY KEY,
  "email" VARCHAR(100) NOT NULL UNIQUE,
  "password" VARCHAR(200) NOT NULL,
  "address" VARCHAR(200)
);

-- 测试用户（密码都是 test123）
INSERT INTO "user" VALUES (1, 'test@example.com', 'scrypt:32768:8:1$6AnQPSSvYwy4nahh$c1ef49cc50ab92c68bd3d4c2169581f18ab5d42424bf1158dd6c6b40617235ae2317a9d7c265f1259be96f6a61d421d156af817947ab9998367a52e6ecb78258', '');
INSERT INTO "user" VALUES (2, 'wrong@example.com', 'scrypt:32768:8:1$WfCYnlF2bgjcnGpw$863660d5571a9c0a691a2fc52e796198ea24d0d6f27917b4957f9a7f9bca3c27f41d02435b0a6a341cd8b58b8c777789c0ddc9324ce92bf65bb5623f636223fe', '');

-- 其他表（空表）
DROP TABLE IF EXISTS "cart";
CREATE TABLE "cart" (
  "id" INTEGER PRIMARY KEY,
  "user_id" INTEGER NOT NULL,
  "product_id" INTEGER NOT NULL,
  "quantity" INTEGER
);

DROP TABLE IF EXISTS "order";
CREATE TABLE "order" (
  "id" INTEGER PRIMARY KEY,
  "user_id" INTEGER NOT NULL,
  "total_amount" FLOAT NOT NULL,
  "status" VARCHAR(20),
  "address" VARCHAR(200) NOT NULL,
  "created_at" DATETIME
);

DROP TABLE IF EXISTS "order_item";
CREATE TABLE "order_item" (
  "id" INTEGER PRIMARY KEY,
  "order_id" INTEGER NOT NULL,
  "product_id" INTEGER NOT NULL,
  "product_name" VARCHAR(100),
  "price" FLOAT,
  "quantity" INTEGER
);

PRAGMA foreign_keys = ON;