"""
代码生成器模式 - Jinja2模板 + 分析结果 → Python爬虫代码

关键设计：
1. CodeTemplate dataclass 定义模板结构
2. 模板按功能分类：sign_function, crawler_class, test_code, environment_injection
3. generate_complete_crawler() 是主入口，串联所有模板

模板列表：
- sign_function: 签名函数（MD5/SHA256/HMAC）
- crawler_class: 爬虫类（session管理、签名、延迟、重试）
- test_code: pytest测试代码
- environment_injection: 浏览器环境注入代码
"""

# 模板变量映射
TEMPLATE_VARIABLES = {
    "sign_function": ["secret_key"],
    "crawler_class": ["class_name", "description", "base_url", "sign_function"],
    "test_code": ["module_name", "class_name"],
    "environment_injection": ["user_agent", "url", "host", "cookie", "title"],
}

# 签名算法实现片段
SIGN_ALGORITHMS = {
    "MD5": "hashlib.md5(sign_str.encode()).hexdigest()",
    "SHA256": "hashlib.sha256(sign_str.encode()).hexdigest()",
    "HMAC": "hmac.new(secret_key.encode(), sign_str.encode(), hashlib.sha256).hexdigest()",
}

# Jinja2陷阱记录
PITFALLS = """
1. 三引号嵌套：模板用'''包裹时，内部不能有'''
2. f-string冲突：Python f-string的{var}与Jinja2{{ var }}冲突
   → 模板中不用f-string，全部用Jinja2变量
3. 缩进问题：Jinja2不会自动处理Python缩进
   → 模板中的代码缩进要手动对齐
4. 特殊字符：JS中的反引号`和${}需要{% raw %}包裹
"""
