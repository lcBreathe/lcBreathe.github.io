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


def icon(name):
    paths = {
        'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 6 9 7 9-7"/>',
        'phone': '<path d="M7 3H4a1 1 0 0 0-1 1c0 10 7 17 17 17a1 1 0 0 0 1-1v-3l-5-2-2 2a14 14 0 0 1-7-7l2-2z"/>',
        'chat': '<path d="M21 11a8 8 0 0 1-8 8H7l-5 3 2-6a8 8 0 0 1 7-13h2a8 8 0 0 1 8 8Z"/><path d="M8 11h.01M12 11h.01M16 11h.01"/>',
        'github': '<path d="M9 19c-4 1-4-2-6-2M15 22v-4c0-1-.3-1.6-.7-2 3-.4 6-1.5 6-6a5 5 0 0 0-1.3-3.5c.1-1 .1-2.2-.5-3.5 0 0-1-.3-3.5 1.3a12 12 0 0 0-6 0C6.5 2.7 5.5 3 5.5 3 5 4.3 5 5.5 5.1 6.5A5 5 0 0 0 3.8 10c0 4.5 3 5.6 6 6-.4.4-.8 1.2-.8 2v4"/>',
        'download': '<path d="M12 3v12m-5-5 5 5 5-5M4 16v5h16v-5"/>',
        'arrow': '<path d="M5 12h14m-5-5 5 5-5 5"/>'
    }
    return f'<svg class="icon" viewBox="0 0 24 24" aria-hidden="true">{paths[name]}</svg>'


def bullet_lists(value):
    return ''.join(f'<ul class="detail-list i18n" data-lang="{lang}" lang="{("zh-CN" if lang == "zh" else "en")}">' + ''.join(f'<li>{e(text)}</li>' for text in value[lang]) + '</ul>' for lang in ("zh", "en"))


def heading(id_, number, zh, en):
    return f'<section id="{id_}" class="content-section"><div class="section-head"><span class="number">{number}</span><h2>{tr(zh, en)}</h2></div>'


def render(d):
    nav = [('about', '关于我', 'About'), ('research', '研究与论文', 'Research'), ('projects', '项目经历', 'Projects'), ('education', '教育背景', 'Education'), ('awards', '荣誉奖项', 'Awards')]
    parts = [f'''<a class="skip-link" href="#main">{tr('跳至正文', 'Skip to content')}</a>
<header class="site-header"><div class="header-inner">
<a class="brand" href="#about">Xiang Zhang <small>{tr('学术主页', 'Academic Homepage')}</small></a>
<nav class="nav" aria-label="Main navigation">{''.join(f'<a href="#{id_}">{tr(zh, en)}</a>' for id_, zh, en in nav)}</nav>
<button id="language-toggle" class="language-button" type="button" aria-label="Switch to English"><span class="language-icon" aria-hidden="true">文/A</span><span class="language-text">English</span></button>
</div></header>
<div class="page-grid"><aside class="sidebar" aria-label="Profile">
<div class="avatar" aria-hidden="true">张</div>
<h2 class="profile-name">{tr(d['name'])}</h2><p class="roman-name">{tr('Xiang Zhang', '张翔')}</p>
<p class="profile-role">{tr('上海交通大学', 'Shanghai Jiao Tong University')}<br>{tr('计算机专业 · 硕士研究生', "Computer Science · Master's student")}<br>{tr('2028 届毕业生', 'Class of 2028')}</p>
<hr class="sidebar-rule">
<div class="profile-contact">
<a href="mailto:{e(d['email'])}">{icon('mail')}{e(d['email'])}</a>
<a href="https://github.com/{e(d['github'])}" target="_blank" rel="noopener noreferrer">{icon('github')}{e(d['github'])}</a>
</div>
</aside>
<main id="main" class="main">
<section id="about" class="hero"><p class="eyebrow">{tr('个人学术主页', 'Academic Profile')}</p>
<h1>{tr('张翔', 'Xiang Zhang')}<small>{tr('Xiang Zhang', '张翔')}</small></h1>
<p class="intro">{tr(d['intro'])}</p>
<div class="interest-row"><span class="interest-label">{tr('研究兴趣', 'Research interests')}</span>{''.join(f'<span class="interest">{e(x)}</span>' for x in d['interests'])}</div>
</section>''', heading('research', '01', '研究与论文', 'Research & Publications')]
    for paper in d['research']:
        authors = ''
        if paper.get('authors'):
            author_names = ', '.join('<strong>Xiang Zhang</strong>' if x == 'Xiang Zhang' else e(x) for x in paper['authors'])
            authors = f'<p class="paper-authors">{author_names}</p>'
        links = ''.join(f'<a href="{e(link["url"])}" target="_blank" rel="noopener noreferrer">{e(link["label"])} ↗</a>' for link in paper.get('links', []))
        parts.append(f'''<article class="research-item" id="{e(paper['id'])}">
<div class="item-top"><div class="badges"><span class="venue">{e(paper['venue'])}</span><span class="status">{tr(paper['status'])}</span></div><span class="date">{e(paper['dates'])}</span></div>
<h3 class="paper-title">{e(paper['title'])}</h3>{authors}
<p class="paper-summary">{tr(paper['summary'])}</p>
<div class="metrics">{''.join(f'<div class="metric"><strong>{e(metric["value"])}</strong><small>{tr(metric["label"])}</small></div>' for metric in paper['metrics'])}</div>
<details class="research-details"><summary>{tr('研究细节与实验', 'Methods & evaluation')}</summary>{bullet_lists(paper['details'])}</details>
{f'<div class="paper-links">{links}</div>' if links else ''}
</article>''')
    parts += ['</section>', heading('projects', '02', '项目经历', 'Projects')]
    for project in d['projects']:
        parts.append(f'''<article class="project-item"><div class="item-top"><h3 class="project-title">{tr(project['title'])}</h3><span class="date">{e(project['dates'])}</span></div>
<p class="project-subtitle">{tr(project['subtitle'])}</p><div class="tag-row">{''.join(f'<span class="tag">{e(x)}</span>' for x in project['tags'])}</div>
{bullet_lists(project['details'])}</article>''')
    parts += ['</section>', heading('education', '03', '教育背景', 'Education')]
    for edu in d['education']:
        parts.append(f'''<article class="education-item"><div class="item-top"><h3 class="education-title">{tr(edu['school'])}</h3><span class="date">{e(edu['dates'])}</span></div><p class="education-degree">{tr(edu['degree'])}</p><p class="education-note">{tr(edu['note'])}</p></article>''')
    parts += ['</section>', heading('awards', '04', '荣誉奖项', 'Honors & Awards'), '<ul class="award-list">' + ''.join(f'<li>{tr(award)}</li>' for award in d['awards']) + '</ul></section>']
    parts.append(f'''<section class="contact-panel" id="contact"><div><h2>{tr('联系我', 'Get in touch')}</h2><p>{tr('欢迎通过邮件联系。', 'Feel free to reach out by email.')}</p></div><a href="mailto:{e(d['email'])}">{e(d['email'])} {icon('arrow')}</a></section>
<noscript><p>{tr('启用 JavaScript 后可切换语言并显示访客统计。', 'Enable JavaScript to switch languages and display visitor statistics.')}</p></noscript>
</main></div>
<footer class="site-footer"><div class="footer-inner"><div>© {d['updated'][:4]} Xiang Zhang<div class="footer-credit">{tr('基于', 'Built with')} <a href="https://academicpages.github.io/" target="_blank" rel="noopener noreferrer">Academic Pages</a> · GitHub Pages</div></div>
<div class="footer-stats"><span><span class="footer-counter-title" title="UV · Busuanzi · Estimated unique visitors">{tr('访问人数', 'Visitors')}</span> <span id="visitor-value" class="stat-value" aria-live="polite">{tr('加载中…', 'Loading…')}</span></span>
<span>{tr('最近更新', 'Last updated')} <time class="stat-value" datetime="{e(d['updated'])}">{e(d['updated'])}</time></span></div></div></footer>
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
