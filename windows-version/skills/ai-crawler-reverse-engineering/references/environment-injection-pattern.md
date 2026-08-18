"""
EnvironmentInjector - 浏览器环境注入器
生成Navigator、Window、WebGL对象，注入到JS代码中补全浏览器环境。

关键设计：
1. BrowserEnvironment dataclass 管理配置
2. generate_* 方法生成各个浏览器对象
3. inject_into_js / inject_into_node 两种注入模式
4. 环境对象包含200+属性，需要按需裁剪
"""

# 核心类
class EnvironmentInjector:
    def __init__(self, environment: BrowserEnvironment = None):
        self.environment = environment or self._default_environment()
    
    def generate_navigator(self) -> dict:
        """30+属性: userAgent, platform, language, plugins, connection..."""
        
    def generate_window(self, url: str) -> dict:
        """200+属性: location, navigator, document, screen, history, crypto..."""
        
    def generate_webgl(self) -> dict:
        """WebGL信息: vendor, renderer, extensions..."""
    
    def inject_into_js(self, js_code: str, url: str) -> str:
        """将环境注入到JS代码前面（浏览器环境）"""
        
    def inject_into_node(self, js_code: str, url: str) -> str:
        """使用JSDOM注入（Node.js环境）"""

# 最重要的属性（按优先级）
CRITICAL_NAVIGATOR = [
    "userAgent", "platform", "language", "languages",
    "cookieEnabled", "hardwareConcurrency", "vendor",
    "appName", "appVersion", "plugins", "connection"
]

CRITICAL_WINDOW = [
    "location", "navigator", "document", "screen",
    "innerWidth", "innerHeight", "outerWidth", "outerHeight",
    "devicePixelRatio", "performance", "crypto", "history"
]

# 环境注入顺序（重要！）
# 1. navigator
# 2. window
# 3. document
# 4. location
# 5. screen
# 6. 其他全局变量
# 7. 原始JS代码
