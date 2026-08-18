# MCP安全威胁参考

来源：教红队的Des（抖音博主，红队教学）

## MCP是新的攻击面

### 数据
- 40.55%的远程MCP服务器**无需认证**
- CVSS 9.6 RCE漏洞存在于广泛使用的MCP包中
- 数百万用户受Chrome扩展MCP漏洞影响

### 三大攻击向量

#### 1. MCP工具投毒（Tool Poisoning）
恶意指令隐藏在工具描述/schema/响应中。
在发现时（调用前/批准前）就激活。
**防御：** mcp-scan、版本锁定、哈希工具描述、白名单、沙箱

#### 2. Chrome扩展 = MCP后门
任何Chrome扩展都能利用本地MCP服务器，不需要特殊权限。
攻击方式：HTTP POST + SSE到本地MCP端点。
沙箱逃逸：扩展通过MCP主机访问绕过浏览器沙箱。
**受影响服务：** 文件系统、Slack、WhatsApp等

#### 3. 供应链攻击
- Typosquatting（域名欺骗）
- Rug pulls（工具在批准后更改定义）
- 恶意MCP服务器伪装成合法服务

### 防御清单
- 只安装验证过的MCP服务器
- 定期运行 mcp-scan
- 使用独立浏览器配置文件
- 签名清单 + 版本锁定 + 白名单
- 细粒度OAuth token + 激进轮换
- 沙箱环境

## 工具推荐
| 工具 | 用途 | 来源 |
|------|------|------|
| mcp-scan | MCP安全扫描 | 检测MCP漏洞 |
| VulnClaw | AI渗透测试（含MCP） | Unclecheng-li/VulnClaw |
| Shannon | AI自动化渗透 | KeygraphHQ/shannon |
| pentestMCP | MCP安全工具桥 | ramkansal/pentestMCP |
| All-Defense-Tool | 攻防一体化 | guchangan1/All-Defense-Tool |
| awesome-mcp-zh | MCP资源指南 | yzfly/awesome-mcp-zh |
