# nuclei 安装与配置参考

## 安装
```bash
# macOS
brew install nuclei

# 或直接下载二进制
curl -sL https://github.com/projectdiscovery/nuclei/releases/latest/download/nuclei_$(uname -s)_$(uname -m).zip -o nuclei.zip && unzip nuclei.zip && mv nuclei ~/.local/bin/
```

## 模板管理

### 下载模板
```bash
# 方法1: nuclei内置更新（需要git）
nuclei -update-templates

# 方法2: git clone（更快，用 --depth 1）
git clone --depth 1 https://github.com/projectdiscovery/nuclei-templates.git ~/nuclei-templates
```

### 模板路径 (v10.4+)
nuclei v10.4+ 模板目录结构变更，注意单复数：

```
~/nuclei-templates/
├── http/
│   ├── cves/                    # CVE漏洞
│   ├── vulnerabilities/         # 通用漏洞
│   ├── misconfiguration/        # ⚠️ 单数！不是 misconfigurations
│   ├── exposures/               # 信息泄露
│   ├── fuzzing/                 # Fuzzing
│   ├── default-logins/          # 默认凭据
│   ├── technologies/            # 技术栈识别
│   ├── cnvd/                    # CNVD漏洞
│   ├── miscellaneous/
│   ├── token-spray/
│   └── credential-stuffing/
├── network/
├── dns/
├── file/
├── headless/
├── javascript/
├── dast/
├── code/
└── cloud/
```

### 常用扫描命令
```bash
# CVE + 漏洞 + 错误配置
nuclei -u https://TARGET -t ~/nuclei-templates/http/cves/ -t ~/nuclei-templates/http/vulnerabilities/ -t ~/nuclei-templates/http/misconfiguration/ -severity critical,high,medium -o results.txt -timeout 10

# 信息泄露专项
nuclei -u https://TARGET -t ~/nuclei-templates/http/exposures/ -o exposures.txt

# 默认凭据
nuclei -u https://TARGET -t ~/nuclei-templates/http/default-logins/ -o default-logins.txt

# 全面扫描（慢）
nuclei -u https://TARGET -t ~/nuclei-templates/http/ -severity critical,high,medium -o full.txt -timeout 10
```

## Pitfalls

1. **模板路径错误**: `http/misconfigurations/` 不存在，正确是 `http/misconfiguration/`（单数）
2. **git clone太慢**: 用 `--depth 1` 只下载最新版本
3. **nuclei -update-templates失败**: 可能是git未安装或网络问题，回退到手动clone
4. **自研框架无匹配**: nuclei主要检测已知CVE和标准配置错误，自研框架通常0匹配
5. **SSL证书问题**: 自签名证书可能导致连接失败，加 `-nc`（no-color）或检查超时设置
6. **扫描太慢**: 用 `-severity critical,high,medium` 过滤低危，用 `-timeout 10` 限制单请求超时
