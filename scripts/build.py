#!/usr/bin/env python3
"""Generate the bilingual Jekyll include and a dependency-free local preview."""
import argparse
import html
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
e = html.escape


def tr(value, en=None):
    if isinstance(value, str):
        value = {"zh": value, "en": en}
    return ''.join(f'<span class="i18n" data-lang="{lang}" lang="{("zh-CN" if lang == "zh" else "en")}">{e(value[lang])}</span>' for lang in ("zh", "en"))


def bullet_lists(value):
    return ''.join(f'<ul class="detail-list i18n" data-lang="{lang}" lang="{("zh-CN" if lang == "zh" else "en")}">' + ''.join(f'<li>{e(text)}</li>' for text in value[lang]) + '</ul>' for lang in ("zh", "en"))


def heading(id_, number, zh, en):
    return f'<section id="{id_}" class="content-section"><h2>{tr(zh, en)}</h2>'


def render(d):
    nav = [('about', '关于我', 'About'), ('research', '研究与论文', 'Research'), ('projects', '项目经历', 'Projects'), ('education', '教育背景', 'Education'), ('awards', '荣誉奖项', 'Awards')]
    parts = [f'''<a class="skip-link" href="#main">{tr('跳至正文', 'Skip to content')}</a>
<div class="page">
<header class="masthead"><a class="site-name" href="#about">Xiang Zhang</a>
<nav class="nav" aria-label="Main navigation">{''.join(f'<a href="#{id_}">{tr(zh, en)}</a>' for id_, zh, en in nav)}</nav>
<button id="language-toggle" class="language-button" type="button" aria-label="Switch to English"><span class="language-text">English</span></button>
</header>
<div class="site-grid">
<aside class="profile-sidebar" aria-label="Profile">
<img class="avatar" src="assets/images/avatar.jpg" width="600" height="600" alt="Xiang Zhang">
<div class="profile-info"><h1>{tr(d['name'])}</h1><p class="other-name">{tr('Xiang Zhang', '张翔')}</p>
<p class="profile-role">{tr('计算机专业硕士研究生', "Master’s student in Computer Science")}</p>
<p class="profile-school">{tr('上海交通大学', 'Shanghai Jiao Tong University')}</p>
<ul class="profile-links"><li>{tr('中国 · 上海', 'Shanghai, China')}</li>
<li><a href="mailto:{e(d['email'])}">{e(d['email'])}</a></li>
<li><a href="https://github.com/{e(d['github'])}" target="_blank" rel="noopener noreferrer">GitHub · {e(d['github'])}</a></li></ul></div>
</aside>
<main id="main"><section id="about" class="about-section"><h2>{tr('关于我', 'About me')}</h2>
<p class="intro">{tr(d['intro'])}</p>
</section>''', heading('research', '01', '研究与论文', 'Research & Publications')]
    for paper in d['research']:
        authors = ''
        if paper.get('authors'):
            author_names = ', '.join('<strong>Xiang Zhang</strong>' if x == 'Xiang Zhang' else e(x) for x in paper['authors'])
            authors = f'<p class="paper-authors">{author_names}</p>'
        links = ''.join(f'<a href="{e(link["url"])}" target="_blank" rel="noopener noreferrer">[{e(link["label"])}]</a>' for link in paper.get('links', []))
        title = e(paper['title'])
        if paper.get('links'):
            title = f'<a href="{e(paper["links"][0]["url"])}" target="_blank" rel="noopener noreferrer">{title}</a>'
        results = ''
        if paper['id'] == 'memtrace':
            values = ' · '.join(f'{tr(metric["label"])} {e(metric["value"])}' for metric in paper['metrics'])
            results = f'<p class="paper-results">{values}</p>'
        parts.append(f'''<article class="research-item" id="{e(paper['id'])}">
<a class="paper-figure" href="{e(paper['overview'])}" target="_blank" rel="noopener noreferrer"><img src="{e(paper['overview'])}" alt="{e(paper['title'])} — overview" loading="lazy"></a>
<div class="paper-content">
<h3 class="paper-title">{title}</h3>{authors}
<p class="paper-meta"><span class="venue">{e(paper['venue'])}</span><span class="status">{tr(paper['status'])}</span><span class="date">{e(paper['dates'])}</span></p>
<p class="paper-summary">{tr(paper['summary'])}</p>
{f'<div class="paper-links">{links}</div>' if links else ''}
<details class="research-details"><summary>{tr('研究详情', 'Details')}</summary>{bullet_lists(paper['details'])}{results}</details>
</div></article>''')
    parts += ['</section>', heading('projects', '02', '项目经历', 'Projects')]
    for project in d['projects']:
        parts.append(f'''<article class="project-item"><div class="item-top"><h3 class="project-title">{tr(project['title'])}</h3><span class="date">{e(project['dates'])}</span></div>
<p class="project-subtitle">{tr(project['subtitle'])}</p>
<details class="project-details"><summary>{tr('项目详情', 'Details')}</summary>{bullet_lists(project['details'])}</details></article>''')
    parts += ['</section>', heading('education', '03', '教育背景', 'Education')]
    for edu in d['education']:
        parts.append(f'''<article class="education-item"><img class="school-logo" src="{e(edu['logo'])}" alt="{e(edu['school']['en'])}" width="72" height="72" loading="lazy"><div class="education-content"><div class="item-top"><h3 class="education-title">{tr(edu['school'])}</h3><span class="date">{e(edu['dates'])}</span></div><p class="education-degree">{tr(edu['degree'])}</p><p class="education-note">{tr(edu['note'])}</p></div></article>''')
    parts += ['</section>', heading('awards', '04', '荣誉奖项', 'Honors & Awards'), '<ul class="award-list">' + ''.join(f'<li>{tr(award)}</li>' for award in d['awards']) + '</ul></section>']
    parts.append(f'''
<noscript><p>{tr('启用 JavaScript 后可切换语言并显示访客统计。', 'Enable JavaScript to switch languages and display visitor statistics.')}</p></noscript>
</main></div>
<footer class="site-footer"><div class="footer-inner"><span>© {d['updated'][:4]} Xiang Zhang</span>
<div class="footer-stats"><span><span class="footer-counter-title" title="UV · Busuanzi · Estimated unique visitors">{tr('访问人数', 'Visitors')}</span> <span id="visitor-value" class="stat-value" aria-live="polite">{tr('加载中…', 'Loading…')}</span></span>
<span>{tr('最近更新', 'Last updated')} <time class="stat-value" datetime="{e(d['updated'])}">{e(d['updated'])}</time></span></div></div></footer></div>
<div class="counter-source" aria-hidden="true"><span id="busuanzi_container_site_uv"><span id="busuanzi_value_site_uv"></span></span></div>''')
    return '\n'.join(parts) + '\n'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--updated-at', help='ISO commit time for the last content change')
    args = parser.parse_args()
    data = json.loads((ROOT / 'content/profile.json').read_text())
    if args.updated_at:
        data['updated'] = datetime.fromisoformat(args.updated_at.replace('Z', '+00:00')).astimezone(ZoneInfo('Asia/Shanghai')).date().isoformat()
    datetime.strptime(data['updated'], '%Y-%m-%d')
    content = render(data)
    (ROOT / '_includes/academic-content.html').write_text(content)
    layout = (ROOT / '_layouts/academic.html').read_text()
    layout = layout.replace('{{ content }}', content).replace('{{ site.url }}', 'https://lcbreathe.github.io').replace('{{ site.baseurl }}', '')
    layout = re.sub(r"{{\s*'(/[^']+)'\s*\|\s*relative_url\s*}}", lambda m: m[1].lstrip('/'), layout)
    dist = ROOT / 'dist'
    dist.mkdir(exist_ok=True)
    (dist / 'index.html').write_text(layout)
    shutil.copytree(ROOT / 'assets', dist / 'assets', dirs_exist_ok=True)
    (dist / '.nojekyll').touch()
    print(f'Built bilingual homepage: {dist / "index.html"}; updated {data["updated"]}')


if __name__ == '__main__':
    main()
