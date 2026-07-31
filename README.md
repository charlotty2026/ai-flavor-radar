# AI 味雷达 (AI Flavor Radar)

> AI文风检测工具——告诉你哪里有AI味、怎么改。v3.0新增5种场景模式、改前→改后示范、白名单误杀防护。

## 这是什么

一个纯Python的命令行工具，扫描文本中的「AI味」特征。

- **只标不改**：精确告诉你哪句话、哪个词有AI味，给出修改方向建议，但不替你改——你的语言审美不被AI替代
- **改前→改后示范**：每条规则配真实改写示例，从"知道改哪"升级到"知道怎么改"
- **Word修订标记**：直接在docx原文上标Track Changes，你在Word里逐条接受/拒绝
- **5种场景模式**：投标方案 / 自媒体 / 小红书 / 邮件 / 学术论文，规则按场景区分
- **白名单误杀防护**：行业术语、专有名词自动跳过，不误报
- **零依赖（docx输出需python-docx）**：纯规则引擎本地跑，不耗token，可批量

## 为什么需要它

市面上的「去AI味」工具分两类：

| 类型 | 代表 | 问题 |
|------|------|------|
| 检测端 | GPTZero、DetectGPT | 只告诉你「这段像AI写的」，不告诉你**哪里**像 |
| 改写端 | 各种「降AI率」工具 | 直接帮你改，但经常把正式文档改成大白话，专业术语也给你「口语化」了 |

**AI味雷达**填补中间空白：精确定位到词句级 + 给出修改方向 + 改前改后示范 + 你自己决定改不改。

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

### 使用

```bash
# 检测投标方案（默认模式）
python3 ai_flavor_radar.py 投标方案.md --mode bid

# 检测公众号文章
python3 ai_flavor_radar.py 公众号文章.md --mode social

# 小红书笔记
python3 ai_flavor_radar.py 笔记.md --mode xiaohongshu

# 商务邮件
python3 ai_flavor_radar.py 邮件.txt --mode email

# 学术论文
python3 ai_flavor_radar.py 论文.md --mode paper

# 生成Word修订标记（Word里逐条接受/拒绝）
python3 ai_flavor_radar.py 方案.docx --mode bid --format docx -o 方案_修订.docx

# 报告不显示示范
python3 ai_flavor_radar.py 文章.md --mode social --no-examples
```

### 输出格式

- `text`（默认）：终端彩色报告
- `json`：结构化输出，可接入流水线
- `markdown`：Markdown报告
- `docx`：Word修订标记（红色删除线标出命中文字，蓝色下划线给修改建议）

## 实测效果

一段AI生成的典型方案：

```bash
python3 ai_flavor_radar.py examples/sample_bid.txt --mode bid
```

输出长这样：

```
  AI味评分: 100/100  🔴 重度AI味
  命中: 25条 (致命2 / 高21 / 中2 / 低0)

  【致命】
  ▸ 第9行 [C02] AI自我暴露
    原文: 作为AI
    建议: 删除AI身份暗示，改为事实陈述
    示范:
      改前: 作为AI，我建议您先检查依赖配置
      改后: 先跑 pip list 看依赖装没装
```

## 规则体系（v3.0：51条规则）

| 模式 | 规则数 | 覆盖 |
|------|--------|------|
| common（通用） | 12 | 起承转合套话、AI自我暴露、万能助词、对仗招牌句式、清单符号、路标词、假互动、过度拔高、翻译腔、表演感、二元框架、AI式谦卑 |
| bid（投标） | 12 | 骈文排比、三段式口号、空洞承诺、长难句、过度结构化、万能定语、评标黑话、无数据承诺、动词口号、经验空转、术语堆砌、模板验收 |
| social（自媒体） | 10 | 书面语过重、长段落、转折堆叠、总结句、小红书信息块、标题党、营销CTA、口播腔、AI客套、划线金句 |
| xiaohongshu（小红书） | 6 | 老模板开场、emoji堆叠、夸张形容词、假分享真广告、信息块、收藏党结尾 |
| email（邮件） | 5 | 虚假客气、助手路标词、模板结束语、过度正式、空泛致谢 |
| paper（学术） | 6 | 模糊权威、填充短语、泛化结论、整齐编号、无来源数据、搬运式引用 |

每条规则都配了「改前→改后」示范示例。

## 白名单（误杀防护）

`rules/whitelist.json` 收录约200个行业术语和专有名词（安全生产许可证、数字化转型、智慧校园、ISO9001、招标文件……），命中白名单的文本自动跳过检测，不会误报。

## 对比竞品

市面上的去AI味工具（humanizer / Humanizer-zh / stop-slop / shuorenhua / ai-flavor-remover / nuwa-skill / writing-agent……）基本都是**改写端**：丢文本进去，吐一段改好的出来。它们的核心是一个给LLM用的提示词，必须靠模型执行，耗token且不可控。

AI味雷达的差异化：

- ✅ **纯规则引擎，本地跑**：不依赖LLM，零token消耗，可批量、可集成流水线
- ✅ **只标不改**：精确定位到词句级，改不改你决定
- ✅ **Word修订标记**：标书/报告场景刚需，竞品没有
- ✅ **场景区分**：5种模式，规则按场景定制
- ✅ **改前→改后示范**：教你怎么改，不是替你改

## License

MIT
