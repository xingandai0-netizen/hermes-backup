// 浏览器Console API解密脚本
// 在目标站点的Console中执行

// === 单个API解密 ===
function decryptApi(encoded) {
  try {
    const reversed = encoded.split('').reverse().join('');
    return JSON.parse(atob(reversed));
  } catch (e) {
    return { error: e.message, raw: encoded.substring(0, 100) };
  }
}

// === 批量API枚举+解密 ===
// 使用方法: 修改 apis 数组为目标站点的API端点
async function auditApis(apis) {
  const results = [];
  for (const api of apis) {
    try {
      const resp = await fetch(api);
      const text = await resp.text();
      let data;
      try {
        // 尝试反转+Base64解密
        const reversed = text.split('').reverse().join('');
        data = JSON.parse(atob(reversed));
      } catch {
        try { data = JSON.parse(text); } catch { data = { raw: text.substring(0, 200) }; }
      }
      results.push({ api, status: resp.status, data });
    } catch (e) {
      results.push({ api, error: e.message });
    }
  }
  return results;
}

// === 从前端JS提取所有API端点 ===
async function extractApis() {
  const scripts = [...document.querySelectorAll('script[src]')].map(s => s.src);
  const allJs = (await Promise.all(
    scripts.map(u => fetch(u).then(r => r.text()).catch(() => ''))
  )).join('\n');
  
  const apis = [...new Set([
    ...(allJs.match(/["']api\/[^"']+["']/g) || []).map(s => s.replace(/["']/g, '')),
    ...(allJs.match(/["']\/api\/[^"']+["']/g) || []).map(s => s.replace(/["']/g, ''))
  ])];
  
  console.log(`Found ${apis.length} API endpoints:`);
  apis.forEach(a => console.log('  ' + a));
  return apis;
}
