-- 用户价格分享平台 数据库初始化 SQL

CREATE DATABASE IF NOT EXISTS price_platform DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE price_platform;

-- 分类表（已经会被 SQLAlchemy 创建，这里留空）
-- 初始插入几个默认一级分类

INSERT INTO categories (name, parent_id, level, sort, status) VALUES
('房地产', 0, 1, 1, 'approved'),
('金融资产', 0, 1, 2, 'approved'),
('汽车', 0, 1, 3, 'approved'),
('食品生鲜', 0, 1, 4, 'approved'),
('日用品', 0, 1, 5, 'approved'),
('奢侈品', 0, 1, 6, 'approved'),
('医药健康', 0, 1, 7, 'approved'),
('服务', 0, 1, 8, 'approved');
