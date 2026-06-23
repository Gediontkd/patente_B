#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "quizPatenteB_updated_2026.json"
OUT = ROOT / "quizPatenteB_translated.json"
REPORT = ROOT / "translations_sections" / "batch_report.json"

SECTION_HINTS = {
    "definizioni-generali-doveri-strada": "Definitions are literal: match the exact road term; absolutes like always/only are common traps.",
    "segnali-pericolo": "Warning signs announce danger ahead; do not confuse advance warning with an immediate obligation.",
    "segnali-divieto": "Prohibition signs forbid access, transit, stopping or a manoeuvre; watch vehicle category traps.",
    "segnali-obbligo": "Mandatory signs impose a direction, lane or equipment; blue circles usually mean obligation.",
    "segnali-precedenza": "Priority signs decide who goes first; STOP means full halt, Give Way means yield.",
    "segnaletica-orizzontale-ostacoli": "Road markings guide lanes and limits; continuous lines and pedestrian areas are classic traps.",
    "semafori-vigili": "Lights and police signals override ordinary signs; arm positions and colours decide the rule.",
    "segnali-indicazione": "Indication signs inform or guide; do not turn information into a ban unless the sign says so.",
    "segnali-complementari-cantiere": "Temporary and work-zone signs change normal rules; yellow/background work signs matter.",
    "pannelli-integrativi": "Supplementary panels limit the main sign by distance, length, time, category or direction.",
    "limiti-di-velocita": "Speed limits depend on road type, vehicle type, weather and novice-driver rules.",
    "distanza-di-sicurezza": "Safety distance depends on speed, reaction, weather, road, brakes and load; never on engine power.",
    "norme-di-circolazione": "General circulation rules favour prudence, right-side driving, signalling and keeping traffic fluid.",
    "precedenza-incroci": "At intersections, read the vehicles' paths first; right-hand priority applies only when no sign/light/police rule overrides it.",
    "sorpasso": "Overtaking requires visibility, space and no danger; bends, crossings and continuous lines are typical false traps.",
    "fermata-sosta-arresto": "Stop, parking and temporary halt are different; bans often depend on distance, visibility and obstruction.",
    "norme-varie-autostrade-pannelli": "Motorways and extra-urban roads have special lane, emergency, access and panel rules.",
    "luci-dispositivi-acustici": "Lights and horn rules depend on visibility, place and vehicle status; misuse is often false.",
    "cinture-casco-sicurezza": "Seat belts, helmets and child restraints are safety obligations with narrow exemptions.",
    "patente-punti-documenti": "Documents, licences, points and sanctions are administrative rules; exact categories and deadlines matter.",
    "incidenti-stradali-comportamenti": "After a crash: secure the scene, help injured people, exchange details and avoid creating danger.",
    "alcool-droga-primo-soccorso": "Fitness to drive is non-negotiable: alcohol, drugs, fatigue and unsafe first aid create danger.",
    "responsabilita-civile-penale-e-assicurazione": "Liability and RCA insurance cover damage rules; intentional or uninsured cases are traps.",
    "consumi-ambiente-inquinamento": "Eco-driving means smooth driving, correct maintenance and no unnecessary idling or noise.",
    "elementi-veicolo-manutenzione-comportamenti": "Vehicle condition affects stability, braking and control; tyres, load and maintenance matter.",
}

PHRASES = [
    ("In una carreggiata del tipo rappresentato", "On a carriageway of the type shown"),
    ("In una carreggiata extraurbana del tipo rappresentato", "On an extra-urban carriageway of the type shown"),
    ("La carreggiata del tipo rappresentato", "The carriageway of the type shown"),
    ("si può sorpassare", "overtaking is possible"),
    ("non si può effettuare", "it is not possible to carry out"),
    ("inversione di marcia", "U-turn"),
    ("anche in curva", "even on a bend"),
    ("Il segnale raffigurato", "The sign shown"),
    ("La figura rappresenta", "The figure shows"),
    ("Il pannello integrativo raffigurato", "The supplementary panel shown"),
    ("strada deformata", "uneven road"),
    ("raffreddati ad aria", "air-cooled"),
    ("liquido di raffreddamento", "coolant"),
    ("dall'apposita finestrella", "through the specific inspection window"),
    ("dall’apposita finestrella", "through the specific inspection window"),
    ("tra le alettature del motore", "between the engine cooling fins"),
    ("preannuncia", "warns of"),
    ("indica", "indicates"),
    ("vieta", "forbids"),
    ("consente", "allows"),
    ("obbliga", "requires"),
    ("può essere", "can be"),
    ("possono essere", "can be"),
    ("si può", "it is possible to"),
    ("non si può", "it is not possible to"),
    ("si deve", "one must"),
    ("non si deve", "one must not"),
    ("deve dare la precedenza", "must give way"),
    ("dare la precedenza", "give way"),
    ("diritto di precedenza", "right of priority"),
    ("è vietato", "it is forbidden"),
    ("è consentito", "it is allowed"),
    ("è obbligatorio", "it is mandatory"),
    ("di norma", "as a rule"),
    ("in ogni caso", "in every case"),
    ("sempre", "always"),
    ("mai", "never"),
    ("solo", "only"),
    ("strada", "road"),
    ("carreggiata", "carriageway"),
    ("corsia", "lane"),
    ("corsie", "lanes"),
    ("sorpasso", "overtaking"),
    ("sorpassare", "overtake"),
    ("sosta", "parking"),
    ("fermata", "stopping"),
    ("arresto", "halt"),
    ("incrocio", "intersection"),
    ("intersezione", "intersection"),
    ("precedenza", "priority"),
    ("pedoni", "pedestrians"),
    ("veicoli", "vehicles"),
    ("motocicli", "motorcycles"),
    ("ciclomotori", "mopeds"),
    ("autocarri", "trucks"),
    ("autobus", "buses"),
    ("velocità", "speed"),
    ("distanza di sicurezza", "safety distance"),
    ("passaggio a livello", "level crossing"),
    ("autostrada", "motorway"),
    ("centro abitato", "built-up area"),
    ("fuori dei centri abitati", "outside built-up areas"),
    ("limite massimo di velocità", "maximum speed limit"),
    ("doppio senso di circolazione", "two-way traffic"),
    ("due sensi", "two directions"),
    ("senso unico", "one-way traffic"),
    ("curva", "bend"),
    ("banchina", "shoulder"),
    ("marciapiede", "sidewalk"),
    ("semaforo", "traffic light"),
    ("agente", "traffic officer"),
    ("polizia", "police"),
    ("incidente", "crash"),
    ("feriti", "injured people"),
    ("alcool", "alcohol"),
    ("droga", "drugs"),
    ("farmaci", "medicines"),
    ("assicurazione", "insurance"),
    ("patente", "driving licence"),
    ("carta di circolazione", "registration certificate"),
    ("pneumatici", "tyres"),
    ("freni", "brakes"),
    ("luci", "lights"),
    ("clacson", "horn"),
    ("cinture di sicurezza", "seat belts"),
    ("casco", "helmet"),
]

WORD_MAP = {
    "il": "the",
    "lo": "the",
    "la": "the",
    "i": "the",
    "gli": "the",
    "le": "the",
    "un": "a",
    "una": "a",
    "uno": "a",
    "di": "of",
    "del": "of the",
    "dello": "of the",
    "della": "of the",
    "dei": "of the",
    "degli": "of the",
    "delle": "of the",
    "a": "at",
    "al": "at the",
    "allo": "at the",
    "alla": "at the",
    "alle": "at the",
    "ai": "to the",
    "ad": "to",
    "in": "in",
    "nel": "in the",
    "nello": "in the",
    "nella": "in the",
    "nei": "in the",
    "nelle": "in the",
    "su": "on",
    "sul": "on the",
    "sulla": "on the",
    "sulle": "on the",
    "sui": "on the",
    "con": "with",
    "per": "for",
    "da": "from/by",
    "dall": "from the",
    "dal": "from the",
    "dalla": "from the",
    "dopo": "after",
    "prima": "before",
    "durante": "during",
    "quando": "when",
    "se": "if",
    "che": "that",
    "e": "and",
    "o": "or",
    "non": "not",
    "è": "is",
    "sono": "are",
    "ha": "has",
    "può": "can",
    "possono": "can",
    "deve": "must",
    "devono": "must",
    "bisogna": "it is necessary",
    "possibile": "possible",
    "consentito": "allowed",
    "consentita": "allowed",
    "consentiti": "allowed",
    "anche": "also",
    "più": "more",
    "secondo": "according to",
    "senza": "without",
    "tra": "between",
    "raffigurato": "shown",
    "rappresentato": "shown",
    "tratto": "stretch",
    "deformata": "uneven",
    "pavimentazione": "surface",
    "irregolare": "irregular",
    "accessi": "accesses",
    "circolazione": "traffic",
    "transito": "transit",
    "posto": "placed",
    "presenza": "presence",
    "destra": "right",
    "sinistra": "left",
    "marcia": "movement",
    "conducente": "driver",
    "conducenti": "drivers",
    "veicolo": "vehicle",
    "stradale": "road",
    "strade": "roads",
    "motore": "engine",
    "pericolo": "danger",
    "obbligo": "obligation",
    "divieto": "prohibition",
    "segnale": "sign",
    "segnali": "signs",
    "pannello": "panel",
    "integrativo": "supplementary",
    "metri": "metres",
    "chilometri": "kilometres",
    "urbana": "urban",
    "extraurbana": "extra-urban",
    "extraurbane": "extra-urban",
    "principale": "main",
    "secondaria": "secondary",
    "emergenza": "emergency",
    "accelerazione": "acceleration",
    "decelerazione": "deceleration",
    "riservata": "reserved",
    "vietata": "forbidden",
    "vietato": "forbidden",
    "permesso": "allowed",
    "permessa": "allowed",
    "obbligatorio": "mandatory",
    "obbligatoria": "mandatory",
    "massimo": "maximum",
    "minimo": "minimum",
    "carico": "load",
    "massa": "mass",
    "ruote": "wheels",
    "raffreddati": "cooled",
    "raffreddamento": "cooling",
    "aria": "air",
    "livello": "level",
    "liquido": "fluid",
    "controllato": "checked",
    "apposita": "specific",
    "finestrella": "inspection window",
    "posta": "located",
    "alettature": "cooling fins",
    "rimorchio": "trailer",
    "pioggia": "rain",
    "neve": "snow",
    "ghiaccio": "ice",
    "nebbia": "fog",
    "visibilità": "visibility",
    "sicurezza": "safety",
    "distanza": "distance",
    "documenti": "documents",
    "sanzioni": "penalties",
    "punti": "points",
    "guida": "driving",
    "svoltare": "turn",
    "luce": "light",
    "norme": "rules",
    "ambiente": "environment",
    "inquinamento": "pollution",
}

TRAP_WORDS = ("sempre", "mai", "solo", "soltanto", "in ogni caso", "comunque", "necessariamente")


def cap(s):
    s = s.strip()
    return s[0].upper() + s[1:] if s else s


def rough_translate(text):
    out = cap(text)
    out = re.sub(r"\bl['’]", "the ", out, flags=re.IGNORECASE)
    out = re.sub(r"\ball['’]", "at the ", out, flags=re.IGNORECASE)
    out = re.sub(r"\bdell['’]", "of the ", out, flags=re.IGNORECASE)
    out = re.sub(r"\bnell['’]", "in the ", out, flags=re.IGNORECASE)
    out = re.sub(r"\bdall['’]", "from the ", out, flags=re.IGNORECASE)
    protected = {}
    for it, en in sorted(PHRASES, key=lambda x: len(x[0]), reverse=True):
        token = f"__PHRASE_{len(protected)}__"
        pattern = re.compile(re.escape(it), flags=re.IGNORECASE)
        if pattern.search(out):
            protected[token] = en
            out = pattern.sub(token, out)

    def repl(match):
        word = match.group(0)
        lower = word.lower()
        mapped = WORD_MAP.get(lower)
        if not mapped:
            return word
        return mapped.capitalize() if word[:1].isupper() else mapped

    out = re.sub(r"[A-Za-zÀ-ÿ]+", repl, out)
    for token, en in protected.items():
        out = out.replace(token, en)
    out = out.replace("  ", " ")
    return out


def hint_for(slug, q, answer):
    lower = q.lower()
    verdict = "VERO" if answer else "FALSO"
    if any(w in lower for w in TRAP_WORDS):
        return f"Trap words such as always/never/only need the exact rule: here the statement is {verdict}."
    if "distanza di sicurezza" in lower:
        return f"Safety distance depends on speed, reaction, road/weather, brakes and load; this wording is {verdict}."
    if "segnale raffigurato" in lower or "pannello integrativo" in lower:
        return f"Identify the pictured sign/panel first, then test the wording: this statement is {verdict}."
    if "precedenza" in lower or "incrocio" in lower or "intersezione" in lower:
        return f"Priority questions are solved by signs/lights/police first, then right-hand priority: {verdict}."
    if "sorpass" in lower:
        return f"Overtaking is allowed only with visibility, space and no danger or ban: {verdict}."
    if "sosta" in lower or "fermata" in lower:
        return f"Separate stopping from parking and check obstruction/distance bans: {verdict}."
    if "alcool" in lower or "droga" in lower or "farmac" in lower:
        return f"Impaired driving rules are strict; alcohol/drugs/unsafe medicines mean danger: {verdict}."
    if "pneumatic" in lower or "fren" in lower or "carico" in lower:
        return f"Vehicle condition and load change grip, braking and stability: {verdict}."
    return f"{SECTION_HINTS.get(slug, 'Memorize the exact rule and the wording trap.')} Answer: {verdict}."


def main():
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    report = {"source": SOURCE.name, "output": OUT.name, "sections": {}, "total": 0}
    for slug, subs in data.items():
        count = 0
        for questions in subs.values():
            for item in questions:
                item["en"] = rough_translate(item.get("q", ""))
                item["hint"] = hint_for(slug, item.get("q", ""), bool(item.get("a")))
                count += 1
        report["sections"][slug] = count
        report["total"] += count

    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.name}")
    print(f"Questions processed: {report['total']}")
    print(f"Wrote {REPORT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
