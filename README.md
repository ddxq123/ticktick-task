# TickTick Skill for OpenClaw

_Query and manage your TickTick tasks · 查询和管理你的滴答清单任务_

An OpenClaw skill that integrates with TickTick (滴答清单) to help you manage tasks with natural language commands.

一个 OpenClaw 技能，集成滴答清单，用自然语言命令帮你管理任务。

---

## ✨ 功能 Features

| 中文 | English |
|------|---------|
| 查询今日任务 | Query today's tasks |
| 查询明日任务 | Query tomorrow's tasks |
| 查询高优先级任务 | Query high priority tasks |
| 创建新任务 | Create new tasks |
| 标记任务完成 | Mark tasks as complete |

---

## 🚀 安装 Installation

### 方法 1：OpenClaw Skill Hub

```bash
# 在 OpenClaw 中运行
openclaw skills install ticktick-task
```

### 方法 2：手动安装 Manual Install

1. 克隆此仓库 / Clone this repo:
```bash
git clone https://github.com/YOUR_USERNAME/ticktick-task.git
```

2. 复制技能到你的 OpenClaw 技能目录 / Copy to your OpenClaw skills directory:
```bash
cp -r ticktick-task ~/.openclaw/workspace/skills/
```

---

## ⚙️ 配置 Configuration

### 1. 获取 TickTick OAuth2 Token

**浏览器授权 / Browser Authorization:**
```
https://dida365.com/oauth/authorize?client_id=YOUR_CLIENT_ID&scope=tasks:read+tasks:write&response_type=code&redirect_uri=YOUR_REDIRECT_URI
```

**或使用 curl:**
```bash
curl -X POST "https://dida365.com/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&code=YOUR_CODE&grant_type=authorization_code&redirect_uri=YOUR_REDIRECT_URI"
```

### 2. 编辑 ticktick.py

打开 `ticktick.py`，修改以下配置 / Edit `ticktick.py` and modify:

```python
# 你的滴答清单 Token / Your TickTick Token
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN_HERE"

# 你的项目 ID / Your Project ID
PROJECT_ID = "YOUR_PROJECT_ID_HERE"

# 你的时区 / Your Timezone
TIMEZONE = ZoneInfo("Asia/Shanghai")  # 修改为你的时区 / Change to your timezone
```

**获取项目 ID / Get Project ID:**
1. 登录滴答清单网页版 / Log in to TickTick web
2. 打开要使用的清单 / Open your list
3. URL 中的 `projectId` 参数即为项目 ID

**常见时区 / Common Timezones:**
- 北京 / Beijing: `ZoneInfo("Asia/Shanghai")`
- 东京 / Tokyo: `ZoneInfo("Asia/Tokyo")`
- 纽约 / New York: `ZoneInfo("America/New_York")`
- 伦敦 / London: `ZoneInfo("Europe/London")`

---

## 💬 使用 Usage

| 你说 / You say | 操作 / Action |
|--------|------|
| "今日任务" / "Today's tasks" | 查询今天任务 / Query today's tasks |
| "明天安排" / "Tomorrow's tasks" | 查询明天任务 / Query tomorrow's tasks |
| "有什么紧急的" / "What's urgent" | 高优先级任务 / High priority tasks |
| "过期任务" / "Overdue tasks" | 已过期任务 / Overdue tasks |
| "加个任务：XXX" / "Add task: XXX" | 创建任务 / Create task |
| "XXX 完成了" / "XXX is done" | 完成任务 / Complete task |

---

## 📁 文件结构 File Structure

```
ticktick-task/
├── SKILL.md          # OpenClaw skill metadata
├── ticktick.py       # Main Python script
└── README.md         # This file
```

---

## 🧪 测试 Testing

运行脚本测试配置 / Run script to test configuration:

```bash
cd ticktick-task
python3 ticktick.py
```

---

## ⚠️ 注意事项 Notes

1. **Token 安全** - 不要公开分享你的 access_token
2. **Token 有效期** - 约 180 天，过期需重新授权
3. **时区** - 根据你的所在地修改时区配置

---

## 📄 许可证 License

MIT License

---

## 🤝 贡献 Contributing

欢迎提交 Issue 和 Pull Request！

---

_Community Contributed Skill · 社区贡献技能_
