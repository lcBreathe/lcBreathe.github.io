# 张翔 · Xiang Zhang — Academic Homepage

基于 [Academic Pages](https://github.com/academicpages/academicpages.github.io) 官方 Jekyll 模板，定制响应式学术主页。

主页：https://lcbreathe.github.io/  
仓库：https://github.com/lcBreathe/lcBreathe.github.io

每次打开或刷新均以英文展示，点击“中文”切换，仅影响当前页面；不读取历史语言偏好，旧链接中的 `lang` 参数也会清除。保留页脚的访问人数和内容更新时间。CSS 与 JavaScript 使用版本参数，避免沿用旧缓存。

作者过长时根据可用宽度省略中间姓名，保留本人姓名和原始作者顺序；完整名单保留在悬停提示和无障碍标签中。侧栏学术账号链接由用户提供，含 Google Scholar、OpenReview、Hugging Face、ORCID 与 LinkedIn。小红书号为 `2625439295`：平台限制当前网络访问，暂未取得可核实的个人主页 URL，因此提供账号搜索入口和复制按钮，未将账号号段猜作主页 ID。浏览器图标使用与链接配色一致的原创 SVG 书页图标。

## 修改内容

- `content/profile.json`：中英文履历、论文、实验数据与链接的唯一内容来源。
- `assets/css/academic.css`：主页样式与手机布局。
- `assets/js/academic.js`：语言切换、导航与真实访客统计。
- `_layouts/academic.html`：定制主页布局。保留官方模板的 `_layouts`、`_includes`、`_sass` 和资源，便于后续扩展。
- `_config.yml`：域名、仓库、作者与 Jekyll 配置。

修改后运行 `python3 scripts/build.py`，会生成 Jekyll 使用的 `_includes/academic-content.html`，以及 `dist/` 中无需 Ruby 的本地预览。推送到 `main` 后，GitHub Actions 自动生成内容、构建 Jekyll 并部署。

## 本地预览

```bash
python3 scripts/build.py
python3 -m http.server 8765 --directory dist
```

打开 http://localhost:8765/。如需完整 Jekyll 预览，安装 Ruby 后执行 `bundle install` 与 `bundle exec jekyll serve`。

## 统计与更新时间

访问人数使用 [不蒜子](https://busuanzi.ibruce.info/) 的站点 UV，是服务估计的独立访客数，不是页面浏览次数。仅在上线域名加载统计脚本；本地显示“上线后统计”，服务不可用时显示“暂不可用”，不使用本地计数代替全站统计。更换域名可能改变统计口径；浏览器拦截第三方脚本时也可能无法统计。

GitHub Actions 从履历、样式、布局或构建脚本 最近一次 Git 提交读取更新日期，并按北京时间展示。仅修改 README 或重新部署不会刷新内容更新时间。尚未提交时，本地预览使用 `content/profile.json` 中的 `updated`。

## 内容来源

中文研究介绍按 `humanizer-zh` 技能的事实保留与自然表达要求润色；仅调整行文与重点，不补写研究贡献。

履历依据用户提供的 `resume(9).pdf`，英文为对应翻译。公开页面和仓库不包含手机号、微信号，不提供简历 PDF 或简历下载。AutoDialect 按用户要求暂不展示；独立荣誉栏已移除，同济优秀学生和优秀毕业生保留在个人经历中，本科专业按用户最新更正写为土木工程（Civil Engineering）。Dial 的 PVLDB 2026 与实验数据按简历保留，作者、论文及代码链接依据 [arXiv:2603.07449](https://arxiv.org/abs/2603.07449)；没有虚构导师信息。MemTrace 按用户要求标注为 arXiv，不展示会议在审状态；标题、完整作者列表和指标依据 [arXiv:2610.04838](https://arxiv.org/abs/2610.04838)，附 arXiv 与官方代码链接；pp 表示百分点。

头像为用户提供的证件照，保留原图并显示为方形。两篇论文的 overview 使用论文原图，点击可查看完整大小：

- [MemTrace 图 2](https://arxiv.org/html/2610.04838v2/overview.png)。
- [Dial 图 2](https://arxiv.org/html/2603.07449v2/Framework.png)。
- 校徽来自[上海交通大学视觉形象识别系统](https://vi.sjtu.edu.cn/index.php/articles/bulletin/13)与[同济大学信息公开网](https://xxgk.tongji.edu.cn/index.php?classid=3080&newsid=6829&t=show)。

Academic Pages / Minimal Mistakes 的许可证保留于 `LICENSE`，原模板说明保留于 `upstream/AcademicPages-README.md`。
