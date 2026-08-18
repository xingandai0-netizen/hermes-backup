#!/usr/bin/env python3
"""
解密中文博彩/诈骗站点的API响应。
常见加密模式: 反转字符串 + Base64解码

用法:
  python3 api-response-decrypt.py <encoded_string>
  python3 api-response-decrypt.py --file responses.txt
  echo "encoded_string" | python3 api-response-decrypt.py --stdin
"""

import base64
import json
import sys


def decrypt_reverse_base64(encoded: str) -> dict:
    """解密 反转+Base64 格式的API响应"""
    reversed_str = encoded[::-1]
    decoded = base64.b64decode(reversed_str).decode('utf-8')
    return json.loads(decoded)


def decrypt_standard_base64(encoded: str) -> dict:
    """解密 标准Base64 格式的API响应"""
    decoded = base64.b64decode(encoded).decode('utf-8')
    return json.loads(decoded)


def try_all_patterns(encoded: str) -> dict:
    """尝试所有已知的加密模式"""
    results = {}
    
    # Pattern 1: Reverse + Base64
    try:
        results['reverse_base64'] = decrypt_reverse_base64(encoded)
    except Exception as e:
        results['reverse_base64'] = f'FAIL: {e}'
    
    # Pattern 2: Standard Base64
    try:
        results['standard_base64'] = decrypt_standard_base64(encoded)
    except Exception as e:
        results['standard_base64'] = f'FAIL: {e}'
    
    # Pattern 3: Double Base64
    try:
        decoded1 = base64.b64decode(encoded).decode('utf-8')
        decoded2 = base64.b64decode(decoded1).decode('utf-8')
        results['double_base64'] = json.loads(decoded2)
    except Exception as e:
        results['double_base64'] = f'FAIL: {e}'
    
    return results


def main():
    if len(sys.argv) < 2:
        print("用法: python3 api-response-decrypt.py <encoded_string>")
        print("      python3 api-response-decrypt.py --file responses.txt")
        print("      echo 'encoded' | python3 api-response-decrypt.py --stdin")
        sys.exit(1)
    
    if sys.argv[1] == '--file':
        with open(sys.argv[2]) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                print(f"\n--- {line[:50]}... ---")
                result = try_all_patterns(line)
                for pattern, data in result.items():
                    if not isinstance(data, str) or not data.startswith('FAIL'):
                        print(f"  [{pattern}]: {json.dumps(data, ensure_ascii=False, indent=2)}")
    
    elif sys.argv[1] == '--stdin':
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            result = try_all_patterns(line)
            for pattern, data in result.items():
                if not isinstance(data, str) or not data.startswith('FAIL'):
                    print(json.dumps(data, ensure_ascii=False, indent=2))
    
    else:
        encoded = sys.argv[1]
        result = try_all_patterns(encoded)
        for pattern, data in result.items():
            status = "✓" if not isinstance(data, str) or not data.startswith('FAIL') else "✗"
            print(f"\n[{status}] {pattern}:")
            if isinstance(data, str) and data.startswith('FAIL'):
                print(f"  {data}")
            else:
                print(f"  {json.dumps(data, ensure_ascii=False, indent=2)}")


if __name__ == '__main__':
    main()
