# 用户价格分享平台

UGC 用户价格分享平台 - 用户录入商品价格，算法加权后展示给所有人。

## 项目结构

```
price-platform/
├── backend/          # Python Flask 后端
├── frontend/         # Vue 3 + Vant UI 前端 H5
└── docs/             # 产品需求文档
```

## 功能特性

- 商品多级分类
- 用户极简价格录入（默认参数，只输价格即可）
- 用户等级积分体系，权重校准算法
- 管理员维护价格优先展示
- 积分解锁付费内容，支持后续货币化
- 自选商品列表，价格走势查看

## 快速开始

### 后端
```bash
cd backend
pip install -r requirements.txt
flask run --host=0.0.0.0
```

### 前端
```bash
cd frontend
npm install
npm run dev
```

## 文档

- [产品需求文档](./docs/PRD.md)
