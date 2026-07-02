"""生成虚拟测试数据"""

import asyncio
import random
import sys
from datetime import datetime, timedelta

from sqlalchemy import select, delete

from app.core.database import AsyncSessionLocal, init_db
from app.core.security import get_password_hash
from app.models.user import User
from app.models.project import Project
from app.models.test_case import TestCase
from app.models.issue import Issue

USERS = [
    {"email": "admin@test.com", "full_name": "系统管理员", "role": "admin", "password": "123456"},
    {"email": "zhangwei@test.com", "full_name": "张伟", "role": "user", "password": "123456"},
    {"email": "lina@test.com", "full_name": "李娜", "role": "user", "password": "123456"},
    {"email": "wangfang@test.com", "full_name": "王芳", "role": "user", "password": "123456"},
    {"email": "liuyang@test.com", "full_name": "刘洋", "role": "user", "password": "123456"},
]

PROJECTS = [
    {"name": "智能家居控制系统 V2.0", "description": "基于物联网的智能家居控制平台，支持灯光、空调、窗帘等设备的远程控制与场景联动", "status": "active"},
    {"name": "电商后台管理系统", "description": "包含商品管理、订单处理、用户管理、营销活动等模块的B端电商后台系统", "status": "active"},
    {"name": "移动端健康追踪App", "description": "iOS/Android双端健康数据追踪应用，支持步数、心率、睡眠等数据记录与分析", "status": "active"},
    {"name": "企业ERP管理系统", "description": "集成财务、人力资源、供应链、生产管理的综合ERP系统", "status": "draft"},
    {"name": "在线教育平台", "description": "支持直播授课、录播回放、在线考试、作业管理的K12在线教育平台", "status": "active"},
    {"name": "物流配送追踪系统", "description": "实时追踪快递包裹状态，支持路径规划、签收确认、异常上报", "status": "archived"},
]

TEST_CASE_TITLES = [
    "登录功能验证", "注册流程测试", "密码重置功能", "首页加载性能测试",
    "数据列表分页验证", "搜索功能准确性测试", "表单输入校验测试", "文件上传功能测试",
    "文件下载功能测试", "权限控制验证", "数据导出功能测试", "消息通知推送测试",
    "接口响应时间测试", "并发操作冲突测试", "数据一致性校验", "离线模式功能测试",
    "弱网环境表现测试", "跨浏览器兼容性测试", "移动端适配测试", "安全性测试-SQL注入防护",
    "安全性测试-XSS防护", "数据备份恢复测试", "批量操作功能测试", "筛选条件组合测试",
    "排序功能验证",
]

ISSUE_TITLES = [
    "登录页面在Chrome下偶现白屏", "提交表单后页面未跳转", "导出Excel文件数据缺失",
    "移动端搜索框被键盘遮挡", "批量删除操作无响应", "日期选择器时区显示错误",
    "上传文件超过5MB时接口超时", "列表分页第二页数据重复", "富文本编辑器图片无法居中",
    "夜间模式切换后图表颜色异常", "WebSocket连接频繁断开重连", "搜索结果排序不正确",
    "密码强度校验规则不生效", "用户头像上传后显示模糊", "下拉框选项过多时无法滚动",
    "页面加载时控制台报错", "验证码邮件延迟严重", "数据图表X轴标签重叠",
    "表单回车键提交不生效", "多语言切换部分文案未翻译",
]

SEVERITIES = ["low", "medium", "high", "critical"]
ISSUE_STATUSES = ["open", "in_progress", "resolved", "closed"]
PRIORITIES = ["low", "medium", "high"]
CASE_STATUSES = ["draft", "active", "deprecated"]
ASSIGNEES = ["张伟", "李娜", "王芳", "刘洋"]
PRECONDITIONS = [
    "已登录系统，拥有对应模块的操作权限",
    "数据库中存在测试数据，网络连接正常",
    "使用Chrome浏览器，分辨率1920x1080",
    "已创建测试项目，项目状态为进行中",
    "账号已绑定手机号，可接收验证码",
]
STEP_TEMPLATES = [
    [("打开登录页面", "显示登录表单"), ("输入正确的账号密码", "输入框显示掩码内容"), ("点击登录按钮", "跳转到首页，显示用户信息")],
    [("进入数据列表页面", "默认显示第一页数据"), ("修改每页显示条数为50", "列表刷新显示50条数据"), ("点击第三页", "显示第三页的数据内容")],
    [("打开搜索框", "搜索框获得焦点"), ("输入关键词并回车", "显示搜索结果列表"), ("点击清空按钮", "搜索框清空，列表恢复全部")],
    [("进入文件上传页面", "显示上传区域"), ("选择一个有效文件", "文件名显示在上传列表"), ("点击上传按钮", "提示上传成功，列表刷新")],
    [("进入设置页面", "显示设置选项"), ("修改主题为暗黑模式", "页面切换为暗色主题"), ("刷新页面", "主题设置保持不变")],
]


async def generate_data():
    print("开始生成虚拟测试数据...", flush=True)
    await init_db()

    async with AsyncSessionLocal() as db:
        # 清空旧数据
        result = await db.execute(select(User).limit(1))
        if result.scalar_one_or_none():
            print("检测到已有数据，先清空旧数据...", flush=True)
            await db.execute(delete(Issue))
            await db.execute(delete(TestCase))
            await db.execute(delete(Project))
            await db.execute(delete(User))
            await db.commit()

        # 1. 创建用户
        print("正在创建用户...", flush=True)
        user_map = {}
        for u in USERS:
            user = User(
                email=u["email"],
                hashed_password=get_password_hash(u["password"]),
                full_name=u["full_name"],
                role=u["role"],
                is_active=True,
            )
            db.add(user)
            await db.flush()
            user_map[u["email"]] = user
            print(f"  - 用户: {u['email']} ({u['full_name']})", flush=True)

        # 2. 创建项目
        print("正在创建项目...", flush=True)
        project_list = []
        for p in PROJECTS:
            project = Project(
                name=p["name"],
                description=p["description"],
                status=p["status"],
                created_by=random.choice(list(user_map.values())).id,
            )
            db.add(project)
            await db.flush()
            project_list.append(project)
            print(f"  - 项目: {p['name']} [{p['status']}]", flush=True)

        # 3. 创建测试用例
        print("正在创建测试用例...", flush=True)
        case_count = 0
        for project in project_list:
            num_cases = random.randint(4, 8)
            titles = random.sample(TEST_CASE_TITLES, min(num_cases, len(TEST_CASE_TITLES)))
            for title in titles:
                steps = random.choice(STEP_TEMPLATES)
                steps_data = [
                    {"step_no": i + 1, "action": s[0], "expected_result": s[1]}
                    for i, s in enumerate(steps)
                ]
                creator = random.choice(list(user_map.values()))
                tc = TestCase(
                    project_id=project.id,
                    title=title,
                    description=f"针对「{project.name}」项目的{title}用例",
                    preconditions=random.choice(PRECONDITIONS),
                    steps=steps_data,
                    priority=random.choice(PRIORITIES),
                    status=random.choices(CASE_STATUSES, weights=[2, 6, 2])[0],
                    created_by=creator.id,
                    created_by_name=creator.full_name,
                )
                db.add(tc)
                case_count += 1
        await db.flush()
        print(f"  - 共创建 {case_count} 个测试用例", flush=True)

        # 4. 创建问题记录
        print("正在创建问题记录...", flush=True)
        issue_count = 0
        for project in project_list:
            num_issues = random.randint(3, 7)
            titles = random.sample(ISSUE_TITLES, min(num_issues, len(ISSUE_TITLES)))
            for title in titles:
                reporter = random.choice(["张伟", "李娜", "王芳", "刘洋", "系统管理员"])
                status = random.choices(ISSUE_STATUSES, weights=[3, 3, 2, 2])[0]
                issue = Issue(
                    project_id=project.id,
                    title=title,
                    description=f"在「{project.name}」项目中发现：{title}。请相关人员排查处理。",
                    severity=random.choice(SEVERITIES),
                    status=status,
                    reporter=reporter,
                    assignee=random.choice(ASSIGNEES) if status != "open" else "",
                    created_by=random.choice(list(user_map.values())).id,
                )
                db.add(issue)
                issue_count += 1
        await db.flush()
        print(f"  - 共创建 {issue_count} 个问题记录", flush=True)

        await db.commit()

    print(f"\n虚拟数据生成完成！用户 {len(USERS)} | 项目 {len(PROJECTS)} | 用例 {case_count} | 问题 {issue_count}", flush=True)
    print("管理员: admin@test.com / 123456", flush=True)


if __name__ == "__main__":
    asyncio.run(generate_data())
