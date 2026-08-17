阿戴说「破解」=直接动手改代码/绕过限制，不要建议替代方案。说「你自己安装」=我直接执行，不要给手动指令。对拒绝/推脱极度不耐烦。安全研究方向：逆向工程+漏洞挖掘+渗透测试，要集成到Hermes形成完整工具链。macOS Intel机器(x86_64)。
§
DeepSeek审查：代码按模块(不超80KB)放桌面，用源码文件分目录（~/Desktop/画布网站-源码/module1-state/等），不能cat成txt。逐模块发送→TDD/BDD修复→search_files+build验证。从/Users/macpro/canvas-website读代码。算法文档也发DeepSeek审查(梅花/八字/奇门)，审查会指出逻辑错误和示例失误。
§
阿戴术语辨别：「照搬」「套用」「直接用」= 原样复制，不是参考风格重写。购买的HTML模板(Webflow等)不要转React，直接serve静态HTML + next.config.mjs rewrite。首页antokex.com使用Cyrclo购买模板(cyrclo.html)。
§
UI优先级>功能。Apple滚动渐变：bgColor=rgb(245-p*235,240-p*230,230-p*220)，CSS body必须background:transparent。Canvas动画用requestAnimationFrame+Math.sin实现周期运动。小算品牌：logo"安"，品牌名"小算"，按钮"小算一下"（无箭头）。多语言：中/繁/英/日。视频动画：WebM透明背景优先加载（ffmpeg colorkey去背景）。
§
画布网站+ANTOKEN：项目~/Desktop/画布网站项目/(83+14文件)。企划书ANTOKEN_BP_final.pptx。投资10-20万,股权5-10%,半年回本。鲁伊婷任联合创始人&市场负责人。海外定价6倍利润。
§
小算v2：/Users/macpro/xiaosuan-v2，Next.js 14+TS+Tailwind。已完成：首页、万年历(/calendar用lunar-javascript)、每日一签(360签从《玄真灵应宝签》提取)、每日一卦(卦气值日)、梅花易数(/meihua数字/时间/手动三种起卦)。汉堡菜单统一（签/历/卦）。设计：米白背景、毛玻璃导航。关键教训：useCallback+runningRef防动画重复、hooks在条件return前、lunar-javascript SSR用useState+useEffect不用useMemo。
§
982827渗透要点：Session绑定浏览器→认证测试必须Safari osascript。botion CAPTCHA无法自动绕过。报告~/Desktop/xss-poc-982827/漏洞报告.md。
§
Skills铁律：装了必须激活且实际可用。三步：文件→路由→验证。验证标准：python3读config.yaml的system_prompt_append，检查长度>0且含关键标记；MCP工具必须能import/启动；CLI工具必须which能找到。不能只grep或信旧报告。工程任务强制NEXUS管线+delegate_task。安装后必须跑全量验证脚本确认生效。
§
阿戴学业情况：Stanfort Academy MSc-IAF学号25028666，London Met合作办学。上学期考试作弊→挂科需重修。休学申请被拒(因作弊)。焦虑症诊断(金华市第二医院)。人在中国无法去新加坡。Dr Kumar是系主任(Head of Dept)。邮件草稿桌面dr_kumar_email_v2.md。Singapore电话+65 83758578。
§
阿戴关注越南电商市场：调研过越南电商平台排名（Shopee最大、TikTok Shop增速快、Tiki本土）、越南私域SCRM工具（Zalo OA是核心载体，类似企微）、越南二手平台（Chợ Tốt类似58同城）。越南没有对标闲鱼的平台，二手交易主要在Facebook Marketplace和Shopee二手板块。越南SCRM生态碎片化：Zalo OA + Facebook Groups + HARAVAN/Sapo。
§
MiMo Token Plan：Lite¥39/4.1B, Standard¥99/11B, Pro¥329/38B, Max¥659/82B Credits。Credits≠token。首购88折,包年88折,夜间0.8x。V2已下线只剩V2.5。Token Plan仅限编程工具(tp-xxxxx key)。阿戴下载/安装类任务先给方案再研究，不要边搜边做让他等。