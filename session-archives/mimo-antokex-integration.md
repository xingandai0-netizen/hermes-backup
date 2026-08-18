# MiMo集成归档

日期: 2026-05-07
状态: ✅ 完成

## 任务概述
将小米MiMo v2.5 Pro通过antokex.com中转站接入Hermes Agent。

## 关键发现
- Sub2API v0.1.124已部署在ECS 47.99.55.244上，Docker容器健康运行
- MiMo API通过Sub2API中转成功，HTTP 200返回
- 用户前台生成的API key可用，不存在403问题
- 之前403错误是因为用了admin内部key或旧key

## 可用模型
- mimo-v2.5-pro (当前默认)
- mimo-v2.5
- mimo-v2-pro
- mimo-v2-flash
- mimo-v2-omni

## 配置详情
- **base_url**: https://antokex.com/v1
- **API Key**: 用户541098012@qq.com前台生成的key
- **Group ID**: 3 ("Xiaomi MiMo")
- **Account ID**: 3 ("Xiaomi MiMo v2.5 Pro")
- **platform**: openai

## 踩坑记录
1. Sub2API内部admin key和用户前台生成key权限不同
2. 用户key必须在Sub2API前台注册后生成，不能直接用admin key
3. Sub2API v0.1.124修复了ChatCompletions路由问题，旧版会将请求路由到/v1/responses导致404

## 测试结果
- mimo-v2.5-pro: HTTP 200 ✅
- mimo-v2.5: HTTP 200 ✅
- 无效key: HTTP 401 ✅

## 相关文件
- 配置: /Users/macpro/.hermes/config.yaml
- 环境变量: /Users/macpro/.hermes/.env
- 测试结果: /Users/macpro/antokex_test_result.txt
