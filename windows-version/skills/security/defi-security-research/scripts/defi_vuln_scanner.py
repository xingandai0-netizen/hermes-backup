#!/usr/bin/env python3
"""
DeFi废弃项目漏洞扫描器
从Etherscan获取合约源码，分析常见漏洞模式

用法：python3 defi_vuln_scanner.py
输出：~/Desktop/DeFi漏洞扫描报告.md + ~/Desktop/defi_vuln_results.json
"""
import requests
import json
import re
import os
import time

ETHERSCAN_API = "https://api.etherscan.io/api"
BSCSCAN_API = "https://api.bscscan.com/api"
POLYGONSCAN_API = "https://api.polygonscan.com/api"

# DeadDeFi验证的合约（有残余资金）
DEAD_CONTRACTS = [
    {"name": "Index Coop", "chain": "eth", "address": "0x248e8bD1985388D2D62e79C6A50051DAeDa30BC9", "tvl": "$5.8M"},
    {"name": "Aave V1 LendingPool", "chain": "eth", "address": "0xf5cceab563cdbc5e2ce1dba77861250389581d2b", "tvl": "$4.83M"},
    {"name": "Set Protocol V1", "chain": "eth", "address": "0xdF903FF062DD851d57f4E18E5444e7ef23D4DA7F", "tvl": "$2.16M"},
    {"name": "Rari Fuse", "chain": "eth", "address": "0xb28153be87a0b8fb948f83ea58800977e7c8bc13", "tvl": "$1.66M"},
    {"name": "dForce Lending", "chain": "eth", "address": "0xec49c17fe2d7dd0724ac9299d1a61be30d1f3e6f", "tvl": "$1.58M"},
    {"name": "Pickle Finance", "chain": "eth", "address": "0x7989Fc1ccFDff1E2899299CC26c7Fc7ad07D55dB", "tvl": "$407K"},
    {"name": "Yam Finance", "chain": "eth", "address": "0x3d1165510c078adf7bdd723f2cfdf503caa85937", "tvl": "$47K"},
    {"name": "Indexed Finance", "chain": "eth", "address": "0x1250ac3781b80339c5cdf2646074a689c99a173d", "tvl": "$40K"},
]

VULNERABILITY_PATTERNS = {
    "reentrancy": {
        "patterns": [r"\.call\{value:.*\}\(.*\)[\s\S]*?(?=balance|Balance|state)", r"\.call\.value\(.*\)\(.*\)"],
        "severity": "CRITICAL"
    },
    "unchecked_call": {
        "patterns": [r"\.call\{.*\}\(.*\)(?![\s\S]*require)", r"\.delegatecall\(.*\)(?![\s\S]*require)"],
        "severity": "HIGH"
    },
    "flash_loan": {
        "patterns": [r"flashLoan", r"flash_loan", r"IFlashLoan"],
        "severity": "HIGH"
    },
    "oracle_manipulation": {
        "patterns": [r"getReserves", r"getAmountOut", r"balanceOf.*pair", r"totalSupply.*balanceOf"],
        "severity": "HIGH"
    },
    "access_control": {
        "patterns": [r"function.*mint.*public(?!.*only)", r"function.*initialize.*public(?!.*only)"],
        "severity": "CRITICAL"
    },
    "selfdestruct": {
        "patterns": [r"selfdestruct\(", r"suicide\("],
        "severity": "CRITICAL"
    },
    "delegatecall": {
        "patterns": [r"\.delegatecall\("],
        "severity": "HIGH"
    },
    "tx_origin": {
        "patterns": [r"tx\.origin"],
        "severity": "MEDIUM"
    },
}

def get_api(chain):
    return {"eth": ETHERSCAN_API, "bsc": BSCSCAN_API, "polygon": POLYGONSCAN_API}.get(chain, ETHERSCAN_API)

def fetch_source(address, chain="eth"):
    try:
        resp = requests.get(get_api(chain), params={
            "module": "contract", "action": "getsourcecode",
            "address": address, "apikey": ""
        }, timeout=15)
        data = resp.json()
        if data.get("status") == "1" and data.get("result"):
            r = data["result"][0]
            if r.get("SourceCode"):
                return {"source": r["SourceCode"], "name": r.get("ContractName", ""), "compiler": r.get("CompilerVersion", "")}
    except:
        pass
    return None

def analyze(source):
    findings = []
    if not source:
        return [{"severity": "INFO", "type": "no_source", "desc": "源码未验证"}]
    for name, info in VULNERABILITY_PATTERNS.items():
        for p in info["patterns"]:
            if re.search(p, source, re.I | re.M):
                findings.append({"severity": info["severity"], "type": name, "desc": f"匹配模式: {p}"})
                break
    return findings or [{"severity": "INFO", "type": "clean", "desc": "未发现明显漏洞"}]

def main():
    results = []
    for c in DEAD_CONTRACTS:
        info = fetch_source(c["address"], c["chain"])
        if info:
            findings = analyze(info["source"])
            results.append({**c, "contract": info["name"], "findings": findings})
        else:
            results.append({**c, "findings": [{"severity": "INFO", "type": "no_source"}]})
        time.sleep(0.5)
    
    with open(os.path.expanduser("~/Desktop/defi_vuln_results.json"), "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"扫描完成: {len(results)} 个合约")

if __name__ == "__main__":
    main()
