# Medical Data Version-Aware Backup and Recovery System

## 项目概述

这是一个针对医疗数据库的版本化备份恢复系统，解决了传统全量备份在数据库 schema 变更时无法正确恢复的问题。

## 核心问题

在医疗信息系统（如联影医疗的系统）中，随着业务迭代：
- 数据库表字段会增加或删除
- 表之间的关系会变化
- 外键约束会调整
- 数据结构会演进

传统的全量备份方案在恢复到新版本数据库时会遇到：
- 字段不匹配导致的恢复失败
- 外键约束冲突
- 数据类型不兼容
- 手动编写 C# 代码维护成本高

## 解决方案

### 核心思想：Schema-Aware Differential Backup

1. **Schema 版本管理**
   - 为每个数据库版本维护 schema 定义
   - 记录版本间的变更（migration）

2. **智能数据映射**
   - 自动检测源版本和目标版本的差异
   - 生成字段映射规则
   - 处理数据类型转换

3. **增量恢复策略**
   - 只备份业务数据，不备份 schema
   - 恢复时根据目标版本 schema 动态适配
   - 自动处理缺失字段（默认值）和废弃字段（忽略）

## 技术架构

```
medical-data-version-backup/
├── src/
│   ├── schema_manager.py      # Schema 版本管理
│   ├── backup_engine.py       # 备份引擎
│   ├── restore_engine.py      # 恢复引擎
│   ├── mapper.py              # 数据映射器
│   └── migration_analyzer.py  # 变更分析器
├── schema_versions/           # Schema 版本定义
├── tests/                     # 测试用例
└── examples/                  # 使用示例
```

## 主要特性

- ✅ 自动检测 schema 版本差异
- ✅ 智能字段映射和数据转换
- ✅ 支持跨版本恢复
- ✅ 外键约束自动处理
- ✅ 增量备份，减少存储空间
- ✅ 可扩展的插件架构
