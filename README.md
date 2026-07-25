# AI 味雷达 (AI Flavor Radar)

> AI文风检测工具--告诉你哪里有AI味，v2.0新增Word修订标记，直接在文档里帮你标好改哪、怎么改。

## 这是什么

一个纯Python的命令行工具，扫描文本中的「AI味」特征。v1.0只标不改给你检测报告，v2.0新增Word修订标记模式--在原文位置插入Track Changes，你在Word里逐条接受/拒绝。

## 为什么需要它

市面上的「去AI味」工具分两类：

| 类型 | 代表 | 问题 |
|------|------|------|
| 检测端 | GPTZero、DetectGPT | 只告诉你「这段像AI写的」，不告诉你**哪里**像 |
| 改写端 | 各种「降AI率」工具 | 直接帮你改，但经常把正式文档改成大白话，专业术语也给你「口语化」了 |

**AI味雷达**填补中间空白：

- ✅ 精确到**哪句话、哪个词**有AI味
- ✅ 标注**AI味类型**（骈文/套话/对仗/空洞承诺……）
- ✅ 给出**修改方向建议**，但不替你改
- ✅ 区分场景：投标方案模式 vs 自媒体模式，不同场景规则不同
- ✅ **v2.0新增**：Word修订标记模式，在docx原文上标Track Changes，逐条接受/拒绝

## 快速开始

### 安装

```bash
# 从 GitHub 克隆
git clone https://github.com/charlotty2026/ai-flavor-radar.git

# 或从 Gitee 克隆（国内推荐）
git clone https://gitee.com/fenglinhuoshanmen/ai-flavor-radar-tool.git
cd ai-flavor-radar
```

零依赖（docx输出需要python-docx），Python 3.8+即可运行。

```bash
# 如需Word修订标记功能
pip install python-docx
```

### 使用

```bash
# 检测投标方案（终端报告）
python ai_flavor_radar.py your_bid.txt --mode bid

# 检测自媒体文章
python ai_flavor_radar.py your_article.txt --mode social

# JSON格式输出（方便程序处理）
python ai_flavor_radar.py your_file.txt --mode bid --format json

# Word修订标记模式（v2.0新功能）
python ai_flavor_radar.py your_bid.txt --mode bid --format docx -o 修订版.docx

# 直接扫描docx文件
python ai_flavor_radar.py 方案.docx --mode bid --format docx -o 方案_修订.docx
```

### Word修订标记效果

打开生成的docx文件，你会看到：
- 🔴 红色删除线：AI味命中的原文
- 🔵 蓝色下划线：AI味雷达的修改建议

在Word中右键「接受」或「拒绝」每条修订即可。

## 检测规则

### 通用规则（common.json）

| 规则 | 检测内容 | 示例 |
|------|----------|------|
| C01 | 起承转合套话 | 「众所周知」「不可否认的是」「值得注意的是」 |
| C02 | AI自我暴露 | 「作为一个AI」「根据我的分析」 |
| C03 | 万能助词 | 「的情况下」「的过程中」（过度使用） |
| C04 | 对仗AI招牌句式 | 「X而非Y」「适合X不适合Y」 |
| C05 | 清单符号陷阱 | ①②③跨段重复使用 |

### 投标方案专项（bid.json）

| 规则 | 检测内容 |
|------|----------|
| B01 | 骈文·假大空排比（「高效、专业、优质」三连） |
| B02 | 骈文·三段式口号（「以X为引领，以Y为支撑，以Z为保障」） |
| B03 | 空洞承诺（「建立完善的管理机制」但没说怎么建） |
| B04 | 长难句（单句超过60字/3个以上逗号/3个以上「的」） |
| B05 | 过度结构化（连续「首先…其次…再次…最后」） |
| B06 | 万能定语堆叠（「科学合理有效的管理」「高效运转协同」等形容词堆砌凑字数） |

### 自媒体专项（social.json）

| 规则 | 检测内容 |
|------|----------|
| S01 | 书面语过重（自媒体不该用「笔者认为」「不可否认」） |
| S02 | 段落过长（自媒体段落超过5行） |
| S03 | 万能转折堆叠（连续使用「然而」「不过」「但是」） |
| S04 | 总结句模板（「综上所述」「总而言之」收尾） |

## 评分机制

- 0-20 🟢 健康：基本无AI味
- 21-50 🟡 轻度：有少量AI味，局部修改即可
- 51-80 🟠 中度：AI味较明显，需要重点修改
- 81-100 🔴 重度：AI味浓重，建议通盘重写

## 输出格式

| 格式 | 命令 | 用途 |
|------|------|------|
| text | `--format text`（默认） | 终端彩色报告 |
| json | `--format json` | 程序处理/CI集成 |
| markdown | `--format markdown` | 文档嵌入 |
| docx | `--format docx` | Word修订标记，逐条接受/拒绝 |

## 项目结构

```
ai-flavor-radar/
├── ai_flavor_radar.py    # 核心检测脚本
├── rules/
│   ├── common.json       # 通用规则（5条）
│   ├── bid.json          # 投标方案专项规则（6条）
│   └── social.json       # 自媒体专项规则（4条）
├── examples/
│   ├── sample_bid.txt    # 投标方案示例
│   └── sample_social.txt # 自媒体示例
├── tests/
│   └── test_basic.py     # 基础测试（10项）
├── README.md
├── LICENSE
└── requirements.txt
```

## 自定义规则

规则文件是JSON格式，你可以自由编辑：

```json
{
  "id": "C01",
  "name": "起承转合套话",
  "severity": "high",
  "patterns": ["众所周知", "不可否认"],
  "suggestion": "直接删掉，或用具体事实替代"
}
```

## 适用场景

- ✅ 投标方案自审（提交前扫一遍AI味）
- ✅ 公众号文章去AI味（发布前检测）
- ✅ 论文/报告自查（避免被判定为AI生成）
- ✅ 团队协作（Word修订标记模式，给同事标好改哪）

## License

MIT License - 随便用，改了记得留个出处。
