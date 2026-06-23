#!/usr/bin/env python3
import html
import json
import os

DATA_FILE = 'quizPatenteB_translated.json' if os.path.exists('quizPatenteB_translated.json') else 'quizPatenteB_updated_2026.json'
OUT_FILE = 'patente_quiz_vero_falso.html'

SECTIONS = [
 ("definizioni-generali-doveri-strada","Definizioni stradali e di traffico · Doveri del conducente"),
 ("segnali-pericolo","Segnali di pericolo"),
 ("segnali-divieto","Segnali di divieto"),
 ("segnali-obbligo","Segnali di obbligo"),
 ("segnali-precedenza","Segnali di precedenza"),
 ("segnaletica-orizzontale-ostacoli","Segnaletica orizzontale · Segni sugli ostacoli"),
 ("semafori-vigili","Segnalazioni semaforiche · Segnali degli agenti"),
 ("segnali-indicazione","Segnali di indicazione"),
 ("segnali-complementari-cantiere","Segnali complementari · Temporanei e di cantiere"),
 ("pannelli-integrativi","Pannelli integrativi dei segnali"),
 ("limiti-di-velocita","Limiti di velocità · Passaggi a livello"),
 ("distanza-di-sicurezza","Distanza di sicurezza"),
 ("norme-di-circolazione","Norme sulla circolazione dei veicoli"),
 ("precedenza-incroci","Esempi di precedenza · Ordine agli incroci"),
 ("sorpasso","Norme sul sorpasso"),
 ("fermata-sosta-arresto","Fermata, sosta, arresto e partenza"),
 ("norme-varie-autostrade-pannelli","Ingombro carreggiata · Autostrade e strade extraurbane"),
 ("luci-dispositivi-acustici","Uso delle luci · Dispositivi acustici · Spie e simboli"),
 ("cinture-casco-sicurezza","Cinture di sicurezza · Casco · Dispositivi di equipaggiamento"),
 ("patente-punti-documenti","Patenti · Documenti · Sanzioni · Patente a punti"),
 ("incidenti-stradali-comportamenti","Comportamenti in caso di incidente · Prevenzione"),
 ("alcool-droga-primo-soccorso","Condizioni fisiche e psichiche · Alcool, droga, farmaci · Primo soccorso"),
 ("responsabilita-civile-penale-e-assicurazione","Responsabilità civile, penale, amministrativa · Assicurazione RCA"),
 ("consumi-ambiente-inquinamento","Limitazione dei consumi · Ambiente · Inquinamento"),
 ("elementi-veicolo-manutenzione-comportamenti","Elementi del veicolo · Manutenzione · Stabilità e tenuta di strada"),
]


def cap(s):
    s = s.strip()
    return s[0].upper() + s[1:] if s else s


def esc(s):
    return html.escape(s)


def render_item(row, chip):
    q = row["question"]
    img = q.get('img') or ''
    imghtml = ''
    if img:
        src = img.lstrip('/')
        imghtml = f'<img loading="lazy" src="{esc(src)}" alt="segnale">'
    en = esc(q.get('en', '').strip())
    hint = esc(q.get('hint', '').strip())
    en_attr = '' if en else ' data-empty="1"'
    hint_attr = '' if hint else ' data-empty="1"'
    return (
        f'<li>{chip}<div class="q">'
        f'<p class="meta"><span>{row["section_no"]:02d}</span>{esc(row["section_title"])} · {esc(row["subtopic"])}</p>'
        f'<p class="it">{esc(cap(q.get("q", "")))}</p>'
        f'<p class="en"{en_attr}>{en}</p>'
        f'<p class="hint"{hint_attr}>{hint}</p>'
        f'</div>{imghtml}</li>'
    )


data = json.load(open(DATA_FILE, encoding='utf-8'))

rows = []
for section_no, (slug, title) in enumerate(SECTIONS, 1):
    for subtopic, questions in data.get(slug, {}).items():
        for question in questions:
            rows.append({
                "section_no": section_no,
                "section_title": title,
                "subtopic": subtopic.replace('-', ' '),
                "question": question,
            })

true_rows = [row for row in rows if row["question"].get("a") is True]
false_rows = [row for row in rows if row["question"].get("a") is False]

true_items = ''.join(render_item(row, '<span class="v">V</span>') for row in true_rows)
false_items = ''.join(render_item(row, '<span class="f">F</span>') for row in false_rows)

CSS = """
:root{--ink:#14181f;--navy:#16315c;--muted:#6b7280;--line:#e4e6ea;--bg:#fbfbf9;
--v:#1f8a4c;--vbg:#e7f4ec;--f:#c2362a;--fbg:#fbe9e7;}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);
font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
.wrap{max-width:920px;margin:0 auto;padding:32px 20px 80px}
header h1{font-size:30px;margin:0 0 4px}
header .sub{color:var(--muted);margin:0 0 6px}
header .tot{font-weight:700;color:var(--navy)}
.toc{margin:22px 0 8px;border-top:2px solid var(--navy);border-bottom:1px solid var(--line);
padding:14px 0;display:grid;grid-template-columns:1fr 1fr;gap:12px 26px}
@media(max-width:640px){.toc{grid-template-columns:1fr}}
.toc a{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--ink);font-weight:700}
.toc a:hover{color:var(--navy)}
.toc .count{margin-left:auto;color:var(--muted);font-size:13px;font-weight:400}
section{margin-top:38px}
h2{font-size:22px;color:var(--navy);border-bottom:2px solid var(--navy);
padding-bottom:8px;margin:0 0 4px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
h2 .hc{color:var(--muted);font-size:13px;font-weight:400}
h2 .top{margin-left:auto;font-size:12px;color:var(--muted);text-decoration:none;font-weight:400}
ol{list-style:none;margin:0;padding:0;counter-reset:q}
li{counter-increment:q;display:flex;gap:12px;align-items:flex-start;
padding:11px 4px;border-bottom:1px solid var(--line)}
li::before{content:counter(q);min-width:44px;text-align:right;color:var(--muted);
font:12px ui-monospace,Menlo,monospace;padding-top:3px}
.v,.f{flex:none;width:24px;height:24px;border-radius:50%;font:700 12px ui-monospace,Menlo,monospace;
display:flex;align-items:center;justify-content:center;margin-top:1px}
.v{color:var(--v);background:var(--vbg)}
.f{color:var(--f);background:var(--fbg)}
.q{flex:1;min-width:0}
.q .meta{margin:0 0 2px;color:var(--muted);font-size:12px}
.q .meta span{font:700 11px ui-monospace,Menlo,monospace;color:var(--navy);margin-right:6px}
.q .it{margin:0}
.q .en{margin:2px 0 0;color:var(--muted);font-size:14px}
.q .en[data-empty]{display:none}
.q .hint{margin:3px 0 0;color:#334155;font-size:13px;font-style:italic}
.q .hint::before{content:"Hint: ";font-style:normal;font-weight:700;color:var(--navy)}
.q .hint[data-empty]{display:none}
li img{flex:none;width:74px;height:auto;border:1px solid var(--line);border-radius:6px;background:#fff}
footer{margin-top:50px;color:var(--muted);font-size:13px;border-top:1px solid var(--line);padding-top:16px}
"""

HTML = f"""<!doctype html><html lang="it"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Quiz Patente B — Vero e Falso</title><style>{CSS}</style></head>
<body><a id="top"></a><div class="wrap">
<header><h1>Quiz Patente B — Vero e Falso</h1>
<p class="sub">Tutte le domande divise in due sezioni: prima tutte le risposte Vero, poi tutte le risposte Falso.</p>
<p class="tot">{len(rows)} domande · {len(true_rows)} Vero · {len(false_rows)} Falso</p></header>
<nav class="toc">
<a href="#vero"><span class="v">V</span> Tutte le domande Vero <span class="count">{len(true_rows)}</span></a>
<a href="#falso"><span class="f">F</span> Tutte le domande Falso <span class="count">{len(false_rows)}</span></a>
</nav>
<section id="vero"><h2><span class="v">V</span>Vero <span class="hc">{len(true_rows)} domande</span><a class="top" href="#top">↑ indice</a></h2><ol>{true_items}</ol></section>
<section id="falso"><h2><span class="f">F</span>Falso <span class="hc">{len(false_rows)} domande</span><a class="top" href="#top">↑ indice</a></h2><ol>{false_items}</ol></section>
<footer>Fonte: listato ministeriale MIT (domande AB, 23-04-2025) + integrazioni 2024–2026.
Dataset: {esc(DATA_FILE)}.</footer>
</div></body></html>"""

open(OUT_FILE, 'w', encoding='utf-8').write(HTML)
print(f"Wrote {OUT_FILE}")
print(f"Total questions: {len(rows)}")
print(f"Vero: {len(true_rows)}")
print(f"Falso: {len(false_rows)}")
print("Size: %.1f KB" % (os.path.getsize(OUT_FILE) / 1024))
