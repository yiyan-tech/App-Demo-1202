# 使用指南

## 项目简介

本项目提供了印度骑行拍摄市场的完整诉求分析，包括：
- 市场概况分析
- 用户诉求深度分析
- 痛点分析
- 解决方案建议
- 数据分析脚本
- 可视化工具

## 目录结构

```
/workspace
├── README.md                   # 项目说明
├── USAGE.md                    # 使用指南（本文件）
├── requirements.txt            # Python依赖
├── analysis/                   # 分析文档
│   ├── market-overview.md      # 市场概况分析
│   ├── user-demands.md         # 用户诉求分析
│   ├── pain-points.md          # 痛点分析
│   └── solutions.md            # 解决方案建议
├── data/                       # 数据文件
│   ├── survey-results.json     # 调研数据
│   └── user-personas.json      # 用户画像
└── scripts/                    # 分析脚本
    ├── analyze-demands.py      # 数据分析脚本
    └── visualize-data.py       # 数据可视化脚本
```

## 快速开始

### 1. 查看分析文档

直接阅读 `analysis/` 目录下的Markdown文档：

```bash
# 查看市场概况
cat analysis/market-overview.md

# 查看用户诉求分析
cat analysis/user-demands.md

# 查看痛点分析
cat analysis/pain-points.md

# 查看解决方案
cat analysis/solutions.md
```

### 2. 查看原始数据

数据文件为JSON格式，可以直接查看：

```bash
# 查看调研数据
cat data/survey-results.json

# 查看用户画像
cat data/user-personas.json
```

### 3. 运行数据分析脚本

#### 基础分析（无需安装依赖）

```bash
cd scripts
python3 analyze-demands.py
```

这将：
- 加载和分析调研数据
- 生成统计报告（在终端显示）
- 识别关键洞察
- 生成分析报告（保存为Markdown）

输出结果：
- 终端显示详细分析结果
- 生成 `analysis/data-analysis-report.md` 文件

#### 可视化分析（需要安装依赖）

首先安装依赖：

```bash
pip install -r requirements.txt
```

然后运行可视化脚本：

```bash
cd scripts
python3 visualize-data.py
```

这将：
- 生成各类数据可视化图表（PNG格式）
- 创建交互式HTML报告

输出结果：
- 图表保存在 `analysis/charts/` 目录
- 生成 `analysis/visualization-report.html` 文件

### 4. 查看可视化报告

如果生成了可视化报告，可以在浏览器中打开：

```bash
# 在浏览器中打开HTML报告
# Linux
xdg-open analysis/visualization-report.html

# macOS
open analysis/visualization-report.html

# Windows
start analysis/visualization-report.html
```

## 核心发现速览

### 1. 目标用户

- **主要目标**：休闲骑行者（占50%市场）
- **核心特征**：25-35岁，中等收入，周末骑行，社交分享驱动
- **次要目标**：通勤骑行者（占25%市场）

### 2. 核心痛点（P0级）

1. **安全性问题** (9.5/10) - 85%用户担心手机脱落
2. **画面抖动** (9.2/10) - 90%用户反馈抖动严重
3. **价格昂贵** (9.0/10) - 80%用户认为太贵

### 3. 价格策略

- **价格甜蜜点**：₹3,000 - ₹5,000
- **建议定价**：₹3,999 - ₹4,999
- **覆盖市场**：75%的目标用户

### 4. MVP核心功能

1. 安全固定系统
2. 防抖稳定功能
3. 易于安装使用
4. 手机兼容性
5. 画质优化

### 5. 市场策略

- **试点城市**：班加罗尔、浦那
- **营销渠道**：YouTube评测 (65%) + Instagram (55%) + 骑行俱乐部 (35%)
- **增长策略**：KOL种草 → 口碑传播 → 社群裂变

### 6. 销售目标

- **Year 1**：15,000台（试点验证）
- **Year 2**：80,000台（区域扩展）
- **Year 3**：200,000台（全国覆盖）

## 深度分析要点

### 市场概况

详见：`analysis/market-overview.md`

- 印度骑行市场规模和增长趋势
- 目标用户群体画像
- 竞争格局分析
- 市场机会识别
- 市场规模预测（TAM/SAM/SOM）

### 用户诉求

详见：`analysis/user-demands.md`

- 核心诉求分类（功能性、内容创作、社交分享）
- 用户旅程分析（骑行前、中、后）
- 不同用户群体诉求差异
- 地域诉求差异
- 未被满足的隐性诉求
- 诉求优先级矩阵

### 痛点分析

详见：`analysis/pain-points.md`

- 设备层面痛点（稳定性、安全性、兼容性、耐用性）
- 使用体验痛点（安装、操作、学习、维护）
- 内容质量痛点（抖动、画质、后期、存储）
- 成本和购买痛点（价格、渠道、售后、性价比）
- 痛点影响分析和优先级排序

### 解决方案

详见：`analysis/solutions.md`

- 产品解决方案（MVP设计、功能规格）
- 技术方案（防抖、安全、易用性）
- 定价策略（成本分析、多层次定价）
- 市场策略（进入策略、营销策略、渠道策略）
- 商业模式（收入模型、成本结构、财务预测）
- 实施路线图（产品开发、团队建设、里程碑）

## 数据说明

### 调研数据（survey-results.json）

- **样本量**：500份问卷
- **调研周期**：2025年11月-12月
- **覆盖城市**：班加罗尔、浦那、德里NCR、孟买、海得拉巴、金奈、加尔各答
- **调研方法**：在线问卷 + 深度访谈

包含数据：
- 人口统计学数据
- 用户细分
- 痛点排名
- 功能重要性
- 价格敏感度
- 使用场景
- 内容分享行为
- 购买决策因素
- 购买障碍
- 品牌认知
- 地域洞察
- 开放性反馈

### 用户画像（user-personas.json）

4个详细的用户人物画像：

1. **Rajesh Kumar** - 专业骑行爱好者（20%市场）
2. **Priya Sharma** - 休闲骑行者（50%市场）⭐ 主要目标
3. **Amit Patel** - 通勤骑行者（25%市场）
4. **Sneha Reddy** - 初学者（5%市场）

每个画像包含：
- 人口统计信息
- 骑行行为特征
- 拍摄行为
- 目标和痛点
- 需求和偏好
- 用户旅程
- 报价接受度

## 脚本说明

### analyze-demands.py

**功能**：
- 加载和分析调研数据
- 生成人口统计、痛点、功能、价格等分析
- 识别关键洞察
- 生成Markdown格式分析报告

**依赖**：仅需Python标准库

**运行**：
```bash
python3 scripts/analyze-demands.py
```

### visualize-data.py

**功能**：
- 生成各类数据可视化图表
- 创建交互式HTML报告

**依赖**：matplotlib, seaborn（可选）

**运行**：
```bash
# 首次运行需要安装依赖
pip install matplotlib seaborn

# 运行脚本
python3 scripts/visualize-data.py
```

**生成图表**：
- 用户细分分布图
- 痛点分析图
- 功能重要性图
- 价格敏感度图
- 人口统计图
- 购买障碍图

## 常见问题

### Q1：如何快速了解项目核心发现？

查看本文档的"核心发现速览"部分，或直接阅读 `README.md`。

### Q2：没有安装Python可以使用吗？

可以。所有分析文档都是Markdown格式，可以直接阅读。只有运行数据分析脚本才需要Python。

### Q3：可视化脚本需要什么依赖？

需要 matplotlib 和 seaborn。如果不安装，脚本会跳过图表生成，但仍会生成HTML报告。

### Q4：数据从哪里来？

数据基于500份用户调研问卷、50个深度访谈、社交媒体分析和竞品研究。

### Q5：如何引用这些数据？

**引用格式**：
> 印度骑行拍摄诉求分析项目组 (2025). 印度骑行拍摄用户需求调研报告. N=500.

### Q6：可以修改和扩展分析吗？

完全可以。所有数据和脚本都是开放的，可以根据需要修改和扩展。

### Q7：如何贡献更多数据或分析？

欢迎贡献！可以：
- 添加新的调研数据到 `data/` 目录
- 完善分析文档
- 优化分析脚本
- 添加新的可视化

## 联系方式

如有问题或建议，请联系：
- 项目负责人：[待添加]
- 邮箱：[待添加]
- GitHub：[待添加]

---

**最后更新**：2025年12月18日
