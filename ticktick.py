#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TickTick Skill - Query and manage your TickTick tasks
TickTick 技能 - 查询和管理你的滴答清单任务

Timezone / 时区说明:
- API returns dates in UTC time (+0000)
- API 返回的日期是 UTC 时间（+0000）
- Convert to your local timezone for display
- 需要转换为你的本地时区才是用户看到的日期

Configuration / 配置:
Modify ACCESS_TOKEN, PROJECT_ID, and TIMEZONE below
修改下方的 ACCESS_TOKEN, PROJECT_ID 和 TIMEZONE
"""

import requests
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

# ============== Configuration / 配置区域 ==============
# Your TickTick OAuth2 Token / 你的滴答清单 Token
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN_HERE"

# Your Project ID (from TickTick web URL) / 你的项目 ID（从滴答清单网页版获取）
PROJECT_ID = "YOUR_PROJECT_ID_HERE"

# Your Timezone / 你的时区
# Common timezones / 常见时区:
#   Asia/Shanghai    - Beijing / 北京时间
#   Asia/Tokyo       - Tokyo / 东京时间
#   America/New_York - New York / 纽约时间
#   Europe/London    - London / 伦敦时间
TIMEZONE = ZoneInfo("Asia/Shanghai")
# =====================================================

BASE_URL = "https://api.dida365.com/open/v1"


def get_headers():
    """Get request headers / 获取请求头"""
    return {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }


def parse_utc_date(date_str):
    """
    Parse UTC date string and convert to local timezone
    解析 UTC 日期字符串并转换为本地时区
    
    Args:
        date_str: API returned date, e.g. "2026-02-28T16:00:00.000+0000"
    
    Returns:
        Local timezone date string "YYYY-MM-DD"
    """
    if not date_str:
        return None
    
    try:
        if date_str.endswith('Z'):
            utc_dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        elif '+0000' in date_str:
            utc_dt = datetime.strptime(date_str[:19], '%Y-%m-%dT%H:%M:%S')
            utc_dt = utc_dt.replace(tzinfo=ZoneInfo('UTC'))
        else:
            utc_dt = datetime.fromisoformat(date_str)
        
        local_dt = utc_dt.astimezone(TIMEZONE)
        return local_dt.strftime('%Y-%m-%d')
    except Exception:
        return None


def get_project_tasks(project_id=None):
    """Get project task list / 获取项目任务列表"""
    pid = project_id or PROJECT_ID
    url = f"{BASE_URL}/project/{pid}/data"
    
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API request failed: {response.status_code}"}
    except Exception as e:
        return {"error": f"Request error: {e}"}


def filter_tasks_by_date(tasks, target_date_str):
    """
    Filter tasks by date
    按日期筛选任务
    
    Args:
        tasks: Task list / 任务列表
        target_date_str: Target date "YYYY-MM-DD" / 目标日期
    
    Returns:
        Task list for that date / 该日期的任务列表
    """
    result = []
    for task in tasks:
        due = task.get('dueDate', '')
        if not due:
            continue
        
        due_date = parse_utc_date(due)
        if due_date == target_date_str:
            result.append(task)
    
    return result


def get_today_tasks(project_id=None):
    """Get today's tasks / 获取今日任务"""
    data = get_project_tasks(project_id)
    
    if "error" in data:
        return data
    
    today_str = datetime.now(TIMEZONE).strftime('%Y-%m-%d')
    today_tasks = filter_tasks_by_date(data.get('tasks', []), today_str)
    
    return {"tasks": today_tasks, "date": today_str}


def get_tomorrow_tasks(project_id=None):
    """Get tomorrow's tasks / 获取明日任务"""
    data = get_project_tasks(project_id)
    
    if "error" in data:
        return data
    
    tomorrow_str = (datetime.now(TIMEZONE) + timedelta(days=1)).strftime('%Y-%m-%d')
    tomorrow_tasks = filter_tasks_by_date(data.get('tasks', []), tomorrow_str)
    
    return {"tasks": tomorrow_tasks, "date": tomorrow_str}


def get_overdue_tasks(project_id=None):
    """Get overdue tasks / 获取已过期任务"""
    data = get_project_tasks(project_id)
    
    if "error" in data:
        return data
    
    today_str = datetime.now(TIMEZONE).strftime('%Y-%m-%d')
    overdue_tasks = []
    
    for task in data.get('tasks', []):
        due = task.get('dueDate', '')
        if not due:
            continue
        
        due_date = parse_utc_date(due)
        if due_date and due_date < today_str:
            overdue_tasks.append(task)
    
    return {"tasks": overdue_tasks, "count": len(overdue_tasks)}


def get_high_priority_tasks(project_id=None, limit=10):
    """Get high priority tasks (priority=5) / 获取高优先级任务"""
    data = get_project_tasks(project_id)
    
    if "error" in data:
        return data
    
    high_priority = []
    for task in data.get('tasks', []):
        if task.get('priority') == 5 and task.get('status') == 0:
            high_priority.append(task)
            if len(high_priority) >= limit:
                break
    
    return {"tasks": high_priority, "count": len(high_priority)}


def create_task(title, project_id=None, content="", priority=0, due_date=None):
    """Create new task / 创建新任务"""
    pid = project_id or PROJECT_ID
    
    url = f"{BASE_URL}/task"
    data = {
        "title": title,
        "projectId": pid,
        "content": content,
        "priority": priority
    }
    
    if due_date:
        data["dueDate"] = due_date
    
    try:
        response = requests.post(url, json=data, headers=get_headers(), timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Create failed: {response.status_code}"}
    except Exception as e:
        return {"error": f"Request error: {e}"}


def complete_task(task_id, project_id=None):
    """Mark task as complete / 标记任务完成"""
    pid = project_id or PROJECT_ID
    
    url = f"{BASE_URL}/project/{pid}/task/{task_id}"
    data = {"status": 1}
    
    try:
        response = requests.put(url, json=data, headers=get_headers(), timeout=10)
        if response.status_code == 200:
            return {"success": True, "task_id": task_id}
        else:
            return {"error": f"Update failed: {response.status_code}"}
    except Exception as e:
        return {"error": f"Request error: {e}"}


def format_task_brief(task):
    """Format single task brief info / 格式化单个任务的简要信息"""
    priority = task.get('priority', 0)
    p_icon = '🔴' if priority == 5 else '🟡' if priority == 3 else '⚪'
    
    title = task.get('title', '')
    tags = task.get('tags', [])
    items = task.get('items', [])
    
    lines = [f"{p_icon} {title}"]
    
    if tags:
        lines.append(f"   Tags / 标签：{', '.join(tags)}")
    
    if items:
        lines.append("   Subtasks / 子任务:")
        for item in items:
            item_status = '✅' if item.get('status') == 1 else '⬜'
            item_title = item.get('title', '')
            lines.append(f"     {item_status} {item_title}")
    
    return '\n'.join(lines)


def format_tasks_report(today_data, tomorrow_data, overdue_data):
    """Format task report / 格式化任务报告"""
    lines = []
    
    # Today's tasks / 今日任务
    today_tasks = today_data.get('tasks', [])
    today_date = today_data.get('date', '')
    lines.append(f"📅 Today's Tasks / 今日任务 ({today_date})")
    lines.append("=" * 50)
    
    if today_tasks:
        for task in today_tasks:
            lines.append(format_task_brief(task))
    else:
        lines.append("✅ No tasks / 没有任务")
    
    lines.append(f"Total / 总计：{len(today_tasks)} tasks / 个任务\n")
    
    # Overdue tasks / 已过期任务
    overdue_tasks = overdue_data.get('tasks', [])
    if overdue_tasks:
        lines.append("⚠️ Overdue Tasks / 已过期任务")
        lines.append("=" * 50)
        for task in overdue_tasks:
            lines.append(format_task_brief(task))
        lines.append(f"Total / 总计：{len(overdue_tasks)} tasks / 个任务\n")
    
    # Tomorrow's tasks / 明日任务
    tomorrow_tasks = tomorrow_data.get('tasks', [])
    tomorrow_date = tomorrow_data.get('date', '')
    if tomorrow_tasks:
        lines.append(f"📌 Tomorrow's Tasks / 明日任务 ({tomorrow_date})")
        lines.append("=" * 50)
        for task in tomorrow_tasks:
            lines.append(format_task_brief(task))
        lines.append(f"Total / 总计：{len(tomorrow_tasks)} tasks / 个任务\n")
    
    return '\n'.join(lines)


# Command line test / 命令行测试
if __name__ == "__main__":
    print("🔍 Testing TickTick API... / 测试滴答清单 API...\n")
    
    # Check configuration / 检查配置
    if ACCESS_TOKEN == "YOUR_ACCESS_TOKEN_HERE":
        print("⚠️  Please configure ACCESS_TOKEN and PROJECT_ID in ticktick.py first / 请先在 ticktick.py 中配置 ACCESS_TOKEN 和 PROJECT_ID\n")
        exit(1)
    
    today = get_today_tasks()
    tomorrow = get_tomorrow_tasks()
    overdue = get_overdue_tasks()
    
    report = format_tasks_report(today, tomorrow, overdue)
    print(report)
