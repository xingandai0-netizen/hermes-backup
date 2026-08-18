import base64
import json
import sys
import requests


def decrypt_reverse_b64(encoded: str) -> dict:
    """解密"反转+Base64"编码的API响应
    
    很多中文Web站点使用这种简单编码:
    1. 将JSON响应反转
    2. Base64编码
    """
    try:
        reversed_str = encoded[::-1]
        decoded = base64.b64decode(reversed_str).decode('utf-8')
        return json.loads(decoded)
    except Exception as e:
        return {"error": str(e)}


def detect_encoding(response_text: str) -> str:
    """自动检测API响应编码模式"""
    import re
    
    # 模式A: 反转+Base64
    try:
        reversed_str = response_text[::-1]
        base64.b64decode(reversed_str)
        return "reverse_base64"
    except:
        pass
    
    # 模式B: 直接Base64
    try:
        if re.match(r'^[A-Za-z0-9+/=]+$', response_text.strip()):
            base64.b64decode(response_text)
            return "base64"
    except:
        pass
    
    # 模式C: 已经是JSON
    try:
        json.loads(response_text)
        return "plain_json"
    except:
        pass
    
    return "unknown"


def batch_decrypt(urls: list, base_url: str = "") -> dict:
    """批量解密多个API端点"""
    results = {}
    for url in urls:
        full_url = base_url + url if not url.startswith('http') else url
        try:
            resp = requests.get(full_url, timeout=10)
            encoding = detect_encoding(resp.text)
            
            if encoding == "reverse_base64":
                results[url] = decrypt_reverse_b64(resp.text)
            elif encoding == "base64":
                results[url] = json.loads(base64.b64decode(resp.text))
            elif encoding == "plain_json":
                results[url] = json.loads(resp.text)
            else:
                results[url] = {"raw": resp.text[:200], "encoding": encoding}
        except Exception as e:
            results[url] = {"error": str(e)}
    
    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 api-decrypt.py <encoded_string>")
        print("  python3 api-decrypt.py --url <api_url>")
        print("  python3 api-decrypt.py --batch <base_url> <api1> <api2> ...")
        sys.exit(1)
    
    if sys.argv[1] == "--url":
        resp = requests.get(sys.argv[2])
        encoding = detect_encoding(resp.text)
        print(f"Detected encoding: {encoding}")
        if encoding == "reverse_base64":
            print(json.dumps(decrypt_reverse_b64(resp.text), indent=2, ensure_ascii=False))
        else:
            print(resp.text[:500])
    
    elif sys.argv[1] == "--batch":
        base_url = sys.argv[2]
        apis = sys.argv[3:]
        results = batch_decrypt(apis, base_url)
        print(json.dumps(results, indent=2, ensure_ascii=False))
    
    else:
        encoded = sys.argv[1]
        encoding = detect_encoding(encoded)
        print(f"Detected encoding: {encoding}")
        if encoding == "reverse_base64":
            print(json.dumps(decrypt_reverse_b64(encoded), indent=2, ensure_ascii=False))
        else:
            print(f"Not reverse_base64. Raw: {encoded[:200]}")
