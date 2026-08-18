---
name: github-security-arsenal
description: GitHub攻防兼备安全工具库。覆盖漏洞扫描、WAF防护、蜜罐诱捕、OSINT情报、红队工具、应急响应等全链路。适用于antokex.com等Web中转站的安全建设和对抗能力构建。
triggers:
  - 需要安全工具推荐
  - 要部署蜜罐/WAF/入侵检测
  - 做渗透测试/漏洞扫描
  - OSINT情报收集
  - 红队/蓝队能力建设
  - 攻防演练
  - "安全加固"
  - "反黑客"
---

# GitHub 攻防兼备安全工具库

> 基于2026-05-11 GitHub搜索结果整理。按能力建设分类，覆盖攻防全链路。

---

## 一、漏洞扫描 & 渗透测试（侦察 → 发现 → 利用）

| 工具 | Stars | 语言 | 用途 |
|------|-------|------|------|
| [sqlmap](https://github.com/sqlmapproject/sqlmap) | 37K | Python | SQL注入自动检测+利用 |
| [nuclei](https://github.com/projectdiscovery/nuclei) | 28K+ | Go | 漏洞扫描器，YAML模板驱动 |
| [h4cker](https://github.com/The-Art-of-Hacking/h4cker) | 26K | Notebook | 攻防技术知识库，数千个渗透测试资源 |
| [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings) | 78K | Python | Web漏洞Payload大全，绕过技巧 |
| [Metasploit](https://github.com/rapid7/metasploit-framework) | 38K | Ruby | 最强渗透测试框架，漏洞利用+后渗透 |
| [OWASP ZAP](https://github.com/zaproxy/zaproxy) | 13K+ | Java | Web应用安全扫描代理 |
| [OWASP WSTG](https://github.com/OWASP/wstg) | 9K | - | Web安全测试指南（测试方法论） |
| [XSStrike](https://github.com/s0md3v/XSStrike) | 15K | Python | 最强XSS扫描器 |
| [PentestGPT](https://github.com/GreyDGL/PentestGPT) | 13K | Python | AI驱动的自动化渗透测试 |
| [naabu](https://github.com/projectdiscovery/naabu) | 6K | Go | 高速端口扫描器 |
| [katana](https://github.com/projectdiscovery/katana) | 17K | Go | 新一代Web爬虫+攻击面发现 |
| [Amass](https://github.com/owasp-amass/amass) | 15K | Go | 攻击面测绘+资产发现 |
| [masscan](https://github.com/robertdavidgraham/masscan) | 24K+ | C | 互联网级别高速端口扫描 |
| [Nettacker](https://github.com/OWASP/Nettacker) | 5K | Python | 自动化渗透测试+漏洞扫描 |
| [Hydra](https://github.com/vanhauser-thc/thc-hydra) | 9K+ | C | 暴力破解（SSH/HTTP/FTP等） |
| [fsociety](https://github.com/Manisso/fsociety) | 12K | Python | 渗透测试工具集打包 |

### antokex.com 适用场景
- **nuclei** + **sqlmap**：定期扫描antokex.com + new-api的SQL注入/XSS/SSRF
- **PentestGPT**：AI辅助做渗透测试，适合小团队
- **Hydra**：测试new-api登录接口的暴力破解防护

---

## 二、WAF & Web防护（被动防御）

| 工具 | Stars | 语言 | 用途 |
|------|-------|------|------|
| [SafeLine 长亭WAF](https://github.com/chaitin/SafeLine) | 21K+ | Go | 自托管WAF反向代理，Docker部署 |
| [ModSecurity](https://github.com/SpiderLabs/ModSecurity) | 9K+ | C++ | Nginx/Apache WAF模块 |
| [teler](https://github.com/teler-sh/teler) | 3K+ | Go | 实时HTTP入侵检测 |
| [bunkerweb](https://github.com/bunkerity/bunkerweb) | 10K+ | Python | 全功能Web应用防火墙 |
| [CrowdSec](https://github.com/crowdsecurity/crowdsec) | 9K+ | Go | 协作式IPS/IDS，众包威胁情报 |

### antokex.com 适用场景
- **SafeLine**：docker compose一键部署，防SQL注入/XSS/SSRF/暴力破解
- **CrowdSec**：众包IP黑名单，别的站被攻击过的IP自动屏蔽

---

## 三、蜜罐 & 欺骗防御（诱捕+溯源）

| 工具 | Stars | 语言 | 用途 |
|------|-------|------|------|
| [T-Pot](https://github.com/telekom-security/tpotce) | 9K | C | 全合一蜜罐平台，Docker部署 |
| [Cowrie](https://github.com/cowrie/cowrie) | 6K | Python | SSH/Telnet蜜罐，记录攻击者操作 |
| [beelzebub](https://github.com/beelzebub-labs/beelzebub) | 2K | Go | AI驱动低代码蜜罐框架 |
| [Ehoney](https://github.com/seccome/Ehoney) | 1K+ | Go | 企业级蜜罐管理系统（中文） |
| [HellPot](https://github.com/yunginnanet/HellPot) | 1K | Go | 惩罚恶意爬虫的无限循环陷阱 |

### antokex.com 适用场景
- **Cowrie**：部署SSH蜜罐，伪装成antokex的SSH端口，记录攻击者行为
- **T-Pot**：全功能蜜罐，一次性部署多种协议的诱捕
- **HellPot**：惩罚扫描antokex的恶意爬虫/扫描器

---

## 四、OSINT & 情报收集（知己知彼）

| 工具 | Stars | 语言 | 用途 |
|------|-------|------|------|
| [sherlock](https://github.com/sherlock-project/sherlock) | 83K | Python | 按用户名搜遍3000+社交平台 |
| [maigret](https:///github.com/soxoj/maigret) | 27K | Python | 高级OSINT，社交平台资料收集 |
| [social-analyzer](https://github.com/qeeqbox/social-analyzer) | 23K | JS | 社交媒体分析+人肉搜索 |
| [PhoneInfoga](https://github.com/sundowndev/phoneinfoga) | 16K | Go | 手机号码信息收集 |
| [theHarvester](https://github.com/laramies/theHarvester) | 16K | Python | 邮箱/子域名/人名收集 |
| [recon-ng](https://github.com/lanmaster53/recon-ng) | 6K | Python | OSINT信息收集框架 |
| [Photon](https://github.com/s0md3v/Photon) | 13K | Python | 超快OSINT爬虫 |
| [holehe](https://github.com/megadose/holehe) | 11K | Python | 按邮箱查注册了哪些网站 |
| [h8mail](https://github.com/khast3x/h8mail) | 5K | Python | 邮箱密码泄露查询 |
| [uncover](https://github.com/projectdiscovery/uncover) | 3K | Go | 攻击面搜索引擎 |
| [trape](https://github.com/jofpin/trape) | 9K | Python | 互联网人员追踪 |

### 适用场景
- **theHarvester** + **sherlock**：查到攻击者后，反向搜索其社交账号/邮箱，收集证据
- **h8mail**：查攻击者邮箱是否在泄露库中

---

## 五、红队工具（进攻模拟 & 后渗透）

| 工具 | Stars | 语言 | 用途 |
|------|-------|------|------|
| [Caldera](https://github.com/mitre/caldera) | 7K | Python | MITRE ATT&CK自动化攻击模拟平台 |
| [Red-Teaming-Toolkit](https://github.com/infosecn1nja/Red-Teaming-Toolkit) | 10K | - | 红队工具集清单 |
| [Impacket](https://github.com/fortra/impacket) | 16K | Python | 网络协议工具集（SMB/Kerberos/NTLM） |
| [Responder](https://github.com/lgandx/Responder) | 6K | Python | LLMNR/NBT-NS投毒 |
| [bettercap](https://github.com/bettercap/bettercap) | 19K | Go | 网络攻击瑞士军刀（WiFi/蓝牙/IPv4/6） |
| [CrackMapExec](https://github.com/Porchetta-Industries/CrackMapExec) | 10K+ | Python | 内网横向渗透 |
| [Certipy](https://github.com/ly4k/Certipy) | 3.5K | Python | AD证书服务攻击 |
| [Nishang](https://github.com/samratashok/nishang) | 10K | PowerShell | 红队PowerShell脚本集 |
| [SET](https://github.com/trustedsec/social-engineer-toolkit) | 15K | Python | 社会工程学攻击工具包 |
| [Evil-WinRM](https://github.com/Hackplayers/evil-winrm) | 4K+ | Ruby | Windows远程Shell |
| [HexStrike AI](https://github.com/0x4m4/hexstrike-ai) | 9K | Python | AI驱动MCP安全代理 |

### 适用场景
- **Caldera**：用MITRE ATT&CK框架模拟真实攻击，测试antokex防线
- **bettercap**：WiFi/网络层攻击模拟（仅用于自家网络）

---

## 六、蓝队 & 应急响应（DFIR）

| 工具 | Stars | 语言 | 用途 |
|------|-------|------|------|
| [SecLists](https://github.com/danielmiessler/SecLists) | 71K | PHP | 安全测试字典/Payload集 |
| [Hayabusa](https://github.com/Yamato-Security/hayabusa) | 3K | Rust | 威胁狩猎+取证时间线 |
| [GRR](https://github.com/google/grr) | 5K | Python | 远程实时取证响应 |
| [awesome-incident-response](https://github.com/meirwah/awesome-incident-response) | 9K | - | 应急响应工具清单 |
| [Matano](https://github.com/matanolabs/matano) | 2K | Rust | 开源安全数据湖 |
| [sentinel-attack](https://github.com/edoardogerosa/sentinel-attack) | 1K | - | Azure Sentinel威胁狩猎 |

---

## 七、Git/密钥安全

| 工具 | Stars | 语言 | 用途 |
|------|-------|------|------|
| [trufflehog](https://github.com/trufflesecurity/trufflehog) | 18K+ | Go | Git仓库密钥泄露扫描 |
| [gitleaks](https://github.com/gitleaks/gitleaks) | 18K+ | Go | Git密钥泄露检测 |
| [RsaCtfTool](https://github.com/RsaCtfTool/RsaCtfTool) | 7K | Python | RSA密钥攻击 |
| [Snyk CLI](https://github.com/snyk/cli) | 6K | TS | 依赖漏洞扫描 |

---

## 八、知识 & 综合资源

| 工具 | Stars | 语言 | 用途 |
|------|-------|------|------|
| [awesome-pentest](https://github.com/enaqx/awesome-pentest) | 26K | - | 渗透测试资源大全 |
| [the-book-of-secret-knowledge](https://github.com/trimstray/the-book-of-secret-knowledge) | 15K+ | - | 安全/运维知识大全 |
| [AWS安全工具集](https://github.com/toniblyx/my-arsenal-of-aws-security-tools) | 9K | Shell | AWS安全攻防工具集 |
| [HackTools](https://github.com/LasCC/HackTools) | 7K | TS | 浏览器安全扩展（Chrome/Firefox） |

---

## 针对 antokex.com 的推荐部署方案

### Phase 1: 防御（立即执行）
```bash
# 1. nuclei 漏洞扫描
go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
nuclei -u https://antokex.com -t cves/ -severity critical,high

# 2. SafeLine WAF
docker compose up -d  # chaitin/SafeLine

# 3. fail2ban 暴力破解防护
apt install fail2ban
systemctl enable --now fail2ban
```

### Phase 2: 诱捕（1-2天内）
```bash
# SSH蜜罐
docker run -d -p 2222:22 cowrie/cowrie
# 修改真实SSH端口，2222放蜜罐

# 蜜罐记录攻击者IP、输入的密码、执行的命令
```

### Phase 3: 情报（持续）
```bash
# trufflehog扫描代码泄露
trufflehog git https://github.com/your-org/antokex-repo

# 定期nuclei扫描
echo "0 3 * * * nuclei -u https://antokex.com -t cves/" | crontab
```

### Phase 4: 攻击模拟（验证防御）
```bash
# 用Caldera模拟攻击
python3 server.py --insecure --build
# 测试你的防线是否真的有效
```

---

## 注意事项

1. **所有攻击工具只能用于自己的系统或获得授权的目标**
2. **蜜罐记录的攻击证据可用于报警/起诉**
3. **CrowdSec的众包黑名单可以间接"反击"——让攻击者IP被全球屏蔽**
4. **定期nuclei扫描可以提前发现0day漏洞影响**
