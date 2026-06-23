import json, html

data = json.load(open('quizPatenteB_updated_2026.json'))

# 25 sections: slug -> (Italian display title) in official order
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
    return s[0].upper()+s[1:] if s else s

def esc(s): return html.escape(s)

rows_total = 0
parts = []
toc = []
for idx,(slug,title) in enumerate(SECTIONS, 1):
    subs = data.get(slug, {})
    qs = [q for sub in subs.values() for q in sub]
    n = len(qs)
    rows_total += n
    anchor = f"sez{idx:02d}"
    toc.append(f'<a href="#{anchor}"><span class="tn">{idx:02d}</span> {esc(title)} <span class="tc">{n}</span></a>')
    items = []
    for i,q in enumerate(qs,1):
        ans = q.get('a')
        chip = '<span class="v">V</span>' if ans else '<span class="f">F</span>'
        img = q.get('img') or ''
        imghtml = ''
        if img:
            src = img.lstrip('/')   # /img_sign/40.png -> img_sign/40.png
            imghtml = f'<img loading="lazy" src="{esc(src)}" alt="segnale">'
        text = esc(cap(q.get('q','')))
        items.append(
            f'<li>{chip}<div class="q"><p class="it">{text}</p>'
            f'<p class="en" data-empty="1"></p></div>{imghtml}</li>')
    parts.append(
        f'<section id="{anchor}"><h2><span class="hn">{idx:02d}</span>{esc(title)}'
        f'<span class="hc">{n} domande</span><a class="top" href="#top">↑ indice</a></h2>'
        f'<ol>{"".join(items)}</ol></section>')

CSS = """
:root{--ink:#14181f;--navy:#16315c;--muted:#6b7280;--line:#e4e6ea;--bg:#fbfbf9;
--v:#1f8a4c;--vbg:#e7f4ec;--f:#c2362a;--fbg:#fbe9e7;}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);
font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
.wrap{max-width:880px;margin:0 auto;padding:32px 20px 80px}
header h1{font-size:30px;letter-spacing:-.4px;margin:0 0 4px}
header .sub{color:var(--muted);margin:0 0 6px}
header .tot{font-weight:700;color:var(--navy)}
.toc{margin:22px 0 8px;border-top:2px solid var(--navy);border-bottom:1px solid var(--line);
padding:14px 0;display:grid;grid-template-columns:1fr 1fr;gap:2px 26px}
@media(max-width:640px){.toc{grid-template-columns:1fr}}
.toc a{display:flex;align-items:baseline;gap:8px;text-decoration:none;color:var(--ink);
padding:3px 0;font-size:14px;border-bottom:1px dotted transparent}
.toc a:hover{color:var(--navy);border-bottom-color:var(--line)}
.toc .tn{font:600 12px ui-monospace,Menlo,monospace;color:var(--f)}
.toc .tc{margin-left:auto;color:var(--muted);font-size:12px}
section{margin-top:38px}
h2{font-size:20px;color:var(--navy);border-bottom:2px solid var(--navy);
padding-bottom:8px;margin:0 0 4px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
h2 .hn{font:700 13px ui-monospace,Menlo,monospace;color:#fff;background:var(--navy);
border-radius:4px;padding:3px 7px}
h2 .hc{color:var(--muted);font-size:13px;font-weight:400}
h2 .top{margin-left:auto;font-size:12px;color:var(--muted);text-decoration:none;font-weight:400}
h2 .top:hover{color:var(--navy)}
ol{list-style:none;margin:0;padding:0;counter-reset:q}
li{counter-increment:q;display:flex;gap:12px;align-items:flex-start;
padding:11px 4px;border-bottom:1px solid var(--line)}
li::before{content:counter(q);min-width:34px;text-align:right;color:var(--muted);
font:12px ui-monospace,Menlo,monospace;padding-top:3px}
.v,.f{flex:none;width:22px;height:22px;border-radius:50%;font:700 12px ui-monospace,Menlo,monospace;
display:flex;align-items:center;justify-content:center;margin-top:1px}
.v{color:var(--v);background:var(--vbg)}
.f{color:var(--f);background:var(--fbg)}
.q{flex:1;min-width:0}
.q .it{margin:0}
.q .en{margin:2px 0 0;color:var(--muted);font-size:14px}
.q .en[data-empty]{display:none}
li img{flex:none;width:74px;height:auto;border:1px solid var(--line);border-radius:6px;background:#fff}
footer{margin-top:50px;color:var(--muted);font-size:13px;border-top:1px solid var(--line);padding-top:16px}
"""

HTML = f"""<!doctype html><html lang="it"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Quiz Patente B — Elenco completo</title><style>{CSS}</style></head>
<body><a id="top"></a><div class="wrap">
<header><h1>Quiz Patente B — Elenco completo</h1>
<p class="sub">Tutte le domande ufficiali, divise per i 25 argomenti d'esame · <span class="v" style="display:inline-flex;vertical-align:middle">V</span> = Vero &nbsp; <span class="f" style="display:inline-flex;vertical-align:middle">F</span> = Falso</p>
<p class="tot">{rows_total} domande · 25 sezioni</p></header>
<nav class="toc">{"".join(toc)}</nav>
{"".join(parts)}
<footer>Fonte: listato ministeriale MIT (domande AB, 23-04-2025) + integrazioni 2024–2026.
Traduzione in inglese e suggerimenti mnemonici: in arrivo.</footer>
</div></body></html>"""

open('patente_quiz_lista.html','w',encoding='utf-8').write(HTML)
print("Wrote patente_quiz_lista.html")
print("Total questions:", rows_total)
import os; print("Size: %.1f KB" % (os.path.getsize('patente_quiz_lista.html')/1024))
