---
name: ticktick
description: Query and manage TickTick tasks with timezone support. Use when user asks about today's tasks, tomorrow's tasks, urgent tasks, or wants to create/complete tasks.
---

# TickTick Skill

_Query and manage your TickTick tasks · 查询和管理你的滴答清单任务_

---

## 🚀 快速开始 / Quick Start

### 1. 获取 OAuth2 Token / Get OAuth2 Token

**方法一：浏览器授权 / Method 1: Browser Authorization**

访问授权链接（替换 `YOUR_CLIENT_ID` 和 `YOUR_REDIRECT_URI`）/ Visit authorization URL:
```
https://dida365.com/oauth/authorize?client_id=YOUR_CLIENT_ID&scope=tasks:read+tasks:write&response_type=code&redirect_uri=YOUR_REDIRECT_URI
```

授权后复制 URL 中的 `code` 参数 / After authorization, copy the `code` from URL.

**方法二：curl 换取 Token / Method 2: Use curl**
```bash
curl -X POST "https://dida365.com/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&code=YOUR_CODE&grant_type=authorization_code&redirect_uri=YOUR_REDIRECT_URI"
```

返回示例 / Response example:
```json
{
  "access_token": "xxxxxxxxx",
  "token_type": "Bearer",
  "expires_in": 2592000
}
```

### 2. 配置技能 / Configure the Skill

编辑 `ticktick.py`，修改顶部的配置常量 / Edit `ticktick.py` and modify the configuration constants:

```python
# 你的滴答清单 Token / Your TickTick Token
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN_HERE"

# 你的项目 ID / Your Project ID
PROJECT_ID = "YOUR_PROJECT_ID_HERE"

# 你的时区 / Your Timezone
TIMEZONE = ZoneInfo("Asia/Shanghai")
```

**获取项目 ID / Get Project ID:**
1. 登录滴答清单网页版 / Log in to TickTick web version
2. 打开要使用的清单 / Open the list you want to use
3. URL 中的 `projectId` 参数即为项目 ID / The `projectId` in URL is your project ID

**常见时区 / Common Timezones:**
- 北京时间 / Beijing: `ZoneInfo("Asia/Shanghai")`
- 东京时间 / Tokyo: `ZoneInfo("Asia/Tokyo")`
- 纽约时间 / New York: `ZoneInfo("America/New_York")`
- 伦敦时间 / London: `ZoneInfo("Europe/London")`

---

## 🤖 触发关键词 / Trigger Keywords

| 用户说 / User says | 操作 / Action |
|--------|------|
| "今日任务" / "Today's tasks" | 查询今天到期的任务 / Query tasks due today |
| "明天安排" / "Tomorrow's tasks" | 查询明天到期的任务 / Query tasks due tomorrow |
| "有什么紧急的" / "What's urgent" | 查询高优先级任务 / Query high priority tasks |
| "过期任务" / "Overdue tasks" | 查询已过期任务 / Query overdue tasks |
| "加个任务：XXX" / "Add task: XXX" | 创建新任务 / Create new task |
| "XXX 完成了" / "XXX is done" | 标记任务完成 / Mark task complete |

---

## 🌍 时区说明 / Timezone

API 返回的日期是 UTC 时间，脚本会自动转换为你的本地时区 / API returns dates in UTC, the script converts to your local timezone automatically.

修改 `ticktick.py` 中的 `TIMEZONE` 变量即可 / Change the `TIMEZONE` variable in `ticktick.py`.

---

## 🐍 测试 / Testing

运行脚本测试配置是否正确 / Run the script to test configuration:

```bash
cd ticktick-task
python3 ticktick.py
```

---

## ⚠️ 注意事项 / Notes

1. **Token 安全 / Token Security** - 不要公开分享 / Do not share publicly
2. **Token 有效期 / Token Validity** - 约 180 天 / About 180 days
3. **时区 / Timezone** - 根据所在地修改 / Change based on your location

---

_Community Contributed Skill · 社区贡献技能_
