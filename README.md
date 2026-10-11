# 张翔 · Xiang Zhang — Academic Homepage

基于 [Academic Pages](https://github.com/academicpages/academicpages.github.io) 官方 Jekyll 模板，定制响应式学术主页。

主页：https://lcbreathe.github.io/  
仓库：https://github.com/lcBreathe/lcBreathe.github.io

支持一键中英文切换、记住语言偏好、`?lang=en` / `?lang=zh` 分享链接、研究细节展开，以及页脚的访问人数和内容更新时间。

## 修改内容

- `content/profile.json`：中英文履历、论文、实验数据与链接的唯一内容来源。
- `assets/css/academic.css`：主页样式与手机布局。
- `assets/js/academic.js`：语言切换、导航、复制与真实访客统计。
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

履历依据用户提供的 `resume(9).pdf`，英文为对应翻译。公开页面和仓库不包含手机号、微信号，不提供 PDF 或简历下载。Dial 的 PVLDB 2026、AutoDialect 的 SIGMOD 2027 在审状态与实验数据按简历保留；没有虚构论文链接、导师或第一作者身份。MemTrace 按用户补充标注为 ICLR 在审；标题、完整作者列表和指标依据 [arXiv:2610.04838](https://arxiv.org/abs/2610.04838)，附论文、PDF 与官方代码链接；pp 表示百分点。

Academic Pages / Minimal Mistakes 的许可证保留于 `LICENSE`，原模板说明保留于 `upstream/AcademicPages-README.md`。
