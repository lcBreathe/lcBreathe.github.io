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


def emphasized(value):
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', e(value))


def tr(value, en=None):
    if isinstance(value, str):
        value = {"zh": value, "en": en}
    return ''.join(f'<span class="i18n" data-lang="{lang}" lang="{("zh-CN" if lang == "zh" else "en")}">{emphasized(value[lang])}</span>' for lang in ("zh", "en"))


def paragraphs(value):
    return ''.join(f'<div class="description i18n" data-lang="{lang}" lang="{("zh-CN" if lang == "zh" else "en")}">' + ''.join(f'<p>{emphasized(text)}</p>' for text in value[lang]) + '</div>' for lang in ("zh", "en"))


def icon(name):
    if name == 'xiaohongshu':
        return '<span class="icon icon-xiaohongshu" aria-hidden="true">红</span>'
    if name == 'linkedin':
        return '<svg class="icon icon-linkedin" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect width="24" height="24" rx="3" fill="#0a66c2"/><circle cx="5.5" cy="6" r="1.5" fill="white"/><path fill="white" d="M4 9h3v11H4zM10 9h3v1.5c1-2 7-3 7 3V20h-3v-6c0-3-4-3-4 0v6h-3z"/></svg>'
    if name == 'huggingface':
        return '<span class="icon icon-huggingface" aria-hidden="true">🤗</span>'
    if name == 'orcid':
        return '<svg class="icon icon-orcid" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="12" fill="#a6ce39"/><text x="4" y="17" fill="white" font-family="Arial,sans-serif" font-size="15">iD</text></svg>'
    paths = {
        'user': '<circle cx="12" cy="8" r="3"/><path d="M5 21v-3a7 7 0 0 1 14 0v3"/>',
        'paper': '<path d="M14 2H5v20h14V7zM14 2v5h5M8 12h8M8 16h8"/>',
        'review': '<path d="M12 5C8 2 4 3 2 4v16c3-2 7-1 10 1 3-2 7-3 10-1V4c-2-1-6-2-10 1zM12 5v16"/>',
        'copy': '<rect x="8" y="8" width="13" height="14" rx="2"/><path d="M16 8V2H2v14h6"/>',
        'project': '<rect x="3" y="7" width="18" height="14" rx="2"/><path d="M8 7V3h8v4M3 12h18M10 12v3h4v-3"/>',
        'education': '<path d="m2 9 10-5 10 5-10 5zM6 11v6c4 3 8 3 12 0v-6M22 9v8"/>',
        'location': '<path d="M19 10c0 5-7 12-7 12S5 15 5 10a7 7 0 0 1 14 0z"/><circle cx="12" cy="10" r="2"/>',
        'mail': '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 6 10 7 10-7"/>',
        'code': '<path d="m8 5-7 7 7 7M16 5l7 7-7 7M14 3l-4 18"/>',
        'github': '<path fill="currentColor" stroke="none" d="M12 .8a11.3 11.3 0 0 0-3.6 22c.6.1.8-.2.8-.5v-2.1c-3.2.7-3.9-1.4-3.9-1.4-.5-1.3-1.3-1.6-1.3-1.6-1-.7.1-.7.1-.7 1.1.1 1.7 1.2 1.7 1.2 1 1.7 2.6 1.2 3.3.9.1-.7.4-1.2.7-1.5-2.6-.3-5.3-1.3-5.3-5.6 0-1.2.4-2.2 1.2-3-.1-.3-.5-1.5.1-3 0 0 1-.3 3.1 1.2a10.8 10.8 0 0 1 5.7 0c2.2-1.5 3.1-1.2 3.1-1.2.6 1.5.2 2.7.1 3 .8.8 1.2 1.8 1.2 3 0 4.3-2.7 5.3-5.3 5.6.4.4.8 1.1.8 2.2v3c0 .3.2.6.8.5A11.3 11.3 0 0 0 12 .8z"/>',
        'link': '<path d="m10 13 4-4M8 15l-2 2a4 4 0 0 1-6-6l4-4a4 4 0 0 1 6 0M16 9l2-2a4 4 0 0 1 6 6l-4 4a4 4 0 0 1-6 0"/>',
        'lab': '<path d="M9 2h6M10 2v7L4 20q-1 2 2 2h12q3 0 2-2L14 9V2M7 15h10"/>',
        'language': '<path d="M2 4h12M8 2v2M5 4c1 6 4 9 8 11M11 4c-1 5-4 9-9 12M14 22l4-11 4 11M15 19h6"/>',
    }
    return f'<svg class="icon icon-{name}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{paths[name]}</svg>'


def heading(id_, number, zh, en):
    return f'<section id="{id_}" class="content-section"><h2>{tr(zh, en)}</h2>'


def render(d):
    nav = [('about', '关于我', 'About'), ('research', '研究与论文', 'Publications'), ('projects', '项目经历', 'Projects'), ('demo', '项目演示', 'Demo'), ('education', '个人经历', 'Experience')]
    parts = [f'''<a class="skip-link" href="#main">{tr('跳至正文', 'Skip to content')}</a>
<div class="page">
<header class="masthead"><a class="site-name" href="#about">Xiang Zhang</a>
<nav class="nav" aria-label="Main navigation">{''.join(f'<a href="#{id_}">{tr(zh, en)}</a>' for id_, zh, en in nav)}</nav>
<button id="language-toggle" class="language-button" type="button" aria-label="切换到中文">{icon('language')}<span class="language-text">中文</span></button>
</header>
<div class="site-grid">
<aside class="profile-sidebar" aria-label="Profile">
<img class="avatar" src="assets/images/avatar.jpg" width="600" height="600" alt="Xiang Zhang">
<div class="profile-info"><h1>{tr(d['name'])}</h1><p class="other-name">{tr('Xiang Zhang', '张翔')}</p>
<p class="profile-role">{tr('计算机专业硕士研究生', "Master’s student in Computer Science")}</p>
<p class="profile-school">{tr('上海交通大学', 'Shanghai Jiao Tong University')}</p>
<ul class="profile-links"><li>{icon('location')}{tr('中国 · 上海', 'Shanghai, China')}</li>
<li><a href="mailto:{e(d['email'])}">{icon('mail')}{e(d['email'])}</a></li>
<li><a href="https://github.com/{e(d['github'])}" target="_blank" rel="noopener noreferrer">{icon('github')}GitHub</a></li>
{''.join(f'<li><a href="{e(profile["url"])}" target="_blank" rel="noopener noreferrer">{icon(profile["icon"])}{e(profile["label"])}</a></li>' for profile in d.get('profiles', []))}
<li class="xiaohongshu-row"><a href="{e(d['xiaohongshu']['search_url'])}" target="_blank" rel="noopener noreferrer" title="Xiaohongshu ID: {e(d['xiaohongshu']['id'])}">{icon('xiaohongshu')}{tr('小红书', 'Xiaohongshu')}</a><button class="copy-account" type="button" data-copy="{e(d['xiaohongshu']['id'])}" aria-label="复制小红书号" title="{e(d['xiaohongshu']['id'])}" hidden>{icon('copy')}</button><span class="copy-status" aria-live="polite"></span></li>
</ul></div>
</aside>
<main id="main"><section id="about" class="about-section"><h2>{tr('关于我', 'About me')}</h2>
<p class="intro">{tr(d['intro'])}</p>
</section>''', heading('research', '01', '研究与论文', 'Research & Publications')]
    for paper in d['research']:
        authors = ''
        if paper.get('authors'):
            author_names = ', '.join('<strong>Xiang Zhang</strong>' if x == 'Xiang Zhang' else e(x) for x in paper['authors'])
            full_authors = e(', '.join(paper['authors']))
            authors = f'<p class="paper-authors" title="{full_authors}" aria-label="{full_authors}" data-authors="{e(json.dumps(paper["authors"]))}">{author_names}</p>'
        links = ''.join(f'<a href="{e(link["url"])}" target="_blank" rel="noopener noreferrer">{icon("github" if link["label"] == "Code" else "paper")}{e(link["label"])}</a>' for link in paper.get('links', []))
        title = e(paper['title'])
        if paper.get('links'):
            title = f'<a href="{e(paper["links"][0]["url"])}" target="_blank" rel="noopener noreferrer">{title}</a>'
        parts.append(f'''<article class="research-item" id="{e(paper['id'])}">
<div class="paper-top">
<a class="paper-figure" href="{e(paper['overview'])}" target="_blank" rel="noopener noreferrer"><span class="paper-badge">{tr(paper['badge'])}</span><img src="{e(paper['overview'])}" alt="{e(paper['title'])} — overview" loading="lazy"></a>
<div class="paper-content">
<h3 class="paper-title">{title}</h3>{authors}
<p class="paper-meta"><span class="venue">{e(paper['venue'])}</span><span class="status">{tr(paper['status'])}</span><span class="date">{e(paper['dates'])}</span></p>
{paragraphs(paper['description'])}
{f'<div class="paper-links">{links}</div>' if links else ''}
</div></div></article>''')
    parts += ['</section>', heading('projects', '02', '项目经历', 'Projects')]
    for project in d['projects']:
        parts.append(f'''<article class="project-item"><div class="item-top"><h3 class="project-title">{tr(project['title'])}</h3><span class="date">{e(project['dates'])}</span></div>
<p class="project-subtitle">{tr(project['subtitle'])}</p>
{paragraphs(project['details'])}</article>''')
    parts += ['</section>', heading('demo', '03', '项目演示', 'Demo')]
    parts.append(f'''<article class="project-item"><h3 class="project-title"><a href="https://lcbreathe.github.io/ai-digest/" target="_blank" rel="noopener noreferrer">{tr('AI 技术日报', 'AI Daily Digest')}</a></h3>
<p class="project-subtitle">{tr('社媒观点 · 技术讨论 · 实践经验', 'Community perspectives · Technical discussions · Hands-on experience')}</p>
<p class="description">{tr('把更多篇幅留给 X、Reddit 和技术博客里的评价、争论与使用经验。同一事件保留不同人的说法，回到原始材料核对，再补充分析；产品发布和热度消息只作简讯。', 'An AI digest with more space for opinions, debates, and hands-on experience from X, Reddit, and technical blogs. It preserves different takes on the same event and checks claims against original sources before adding analysis. Launches and trending news stay brief.')}</p>
<p class="links"><a href="https://lcbreathe.github.io/ai-digest/" target="_blank" rel="noopener noreferrer">{tr('阅读日报 ↗', 'Read the digest ↗')}</a> · <a href="https://lcbreathe.github.io/ai-digest/archive.html" target="_blank" rel="noopener noreferrer">{tr('历史日历', 'Past issues')}</a></p></article>''')
    parts += ['</section>', heading('education', '04', '个人经历', 'Experience')]
    for edu in d['education']:
        affiliation = ''
        if edu.get('advisor'):
            affiliation = f'<p class="education-affiliation">{tr("导师", "Advisor")}: <a href="{e(edu["advisor"]["url"])}" target="_blank" rel="noopener noreferrer">{tr(edu["advisor"]["name"])}</a><span class="separator" aria-hidden="true"> · </span><a href="{e(edu["lab"]["url"])}" target="_blank" rel="noopener noreferrer">{icon("lab")}{e(edu["lab"]["name"])}</a></p>'
        parts.append(f'''<article class="education-item"><img class="school-logo" src="{e(edu['logo'])}" alt="{e(edu['school']['en'])}" width="72" height="72" loading="lazy"><div class="education-content"><div class="item-top"><h3 class="education-title">{tr(edu['school'])}</h3><span class="date">{e(edu['dates'])}</span></div><p class="education-degree">{tr(edu['degree'])}</p>{affiliation}<p class="education-note">{tr(edu['note'])}</p></div></article>''')
    parts += ['</section>']
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
