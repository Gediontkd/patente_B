#!/usr/bin/env python3
import os
from build_pdf import build_section

CM = 28.35  # points per cm

# Column layout used for every table: Term (IT) | Definition (IT) | English gloss
W = [3.3*CM, 7.7*CM, 5.0*CM]
HEADERS = ["Termine (IT)", "Definizione (Italiano)", "English"]

SECTION = {
    "title": "Section 2: The Road",
    "subtitle": "La strada - Tipi di strade e termini stradali",
    "blocks": [
        # ---------------------------------------------------------------
        {"type": "h2", "text": "1. Le tre definizioni fondamentali"},
        {"type": "table", "headers": HEADERS, "widths": W, "rows": [
            ["<b>Strada</b>",
             "Area pubblica progettata per il movimento di pedoni, veicoli e animali. Include marciapiedi (nelle aree urbane) o banchine (fuori dalle aree urbane), piste ciclabili e carreggiate.",
             "<b>Road:</b> a public area designed for the movement of pedestrians, vehicles and animals. It includes sidewalks (in urban areas) or shoulders (outside urban areas), bike lanes and carriageways."],
            ["<b>Carreggiata</b>",
             "Parte della strada destinata alla circolazione dei veicoli. Non comprende marciapiedi, banchine o piste ciclabili, le piazzole di sosta e le corsie d'emergenza. Pu&ograve; essere a senso unico di circolazione oppure a doppio senso.",
             "<b>Carriageway:</b> the part of the road meant for vehicle traffic. It does not include sidewalks, shoulders, bike lanes, lay-bys or emergency lanes. It can be one-way or two-way."],
            ["<b>Corsia</b>",
             "Divisione longitudinale della carreggiata destinata al movimento di una singola fila di veicoli.",
             "<b>Lane:</b> a longitudinal division of the carriageway meant for the movement of a single line of vehicles."],
        ]},

        # ---------------------------------------------------------------
        {"type": "h2", "text": "2. Aree pedonali e di bordo"},
        {"type": "table", "headers": HEADERS, "widths": W, "rows": [
            ["<b>Attraversamento pedonale</b>",
             "Area della carreggiata segnalata da strisce bianche dove i pedoni possono attraversare in sicurezza.",
             "<b>Pedestrian (zebra) crossing:</b> an area of the carriageway marked by white stripes where pedestrians can cross safely."],
            ["<b>Banchina</b>",
             "Fascia di terreno lungo il bordo della carreggiata. Viene utilizzata per fermate d'emergenza o per separare la carreggiata dalle aree adiacenti.",
             "<b>Shoulder / verge:</b> a strip of ground along the edge of the carriageway. It is used for emergency stops or to separate the carriageway from adjacent areas."],
            ["<b>Marciapiede</b>",
             "Spazio pavimentato lungo i lati di una strada, destinato ai pedoni.",
             "<b>Sidewalk / pavement:</b> a paved space along the sides of a road, meant for pedestrians."],
            ["<b>Salvagente</b>",
             "Area rialzata o segnalata all'interno della carreggiata che funge da rifugio per i pedoni, spesso presente nei pressi degli incroci.",
             "<b>Pedestrian refuge island:</b> a raised or marked area within the carriageway that acts as a refuge for pedestrians, often found near intersections."],
            ["<b>Isola di traffico</b>",
             "Area rialzata o segnalata all'interno della carreggiata per gestire il flusso del traffico, spesso presente nelle rotatorie.",
             "<b>Traffic island:</b> a raised or marked area within the carriageway to manage the flow of traffic, often found in roundabouts."],
        ]},

        # ---------------------------------------------------------------
        {"type": "h2", "text": "3. Intersezioni e attraversamenti"},
        {"type": "table", "headers": HEADERS, "widths": W, "rows": [
            ["<b>Intersezione</b>",
             "Punto in cui due o pi&ugrave; strade si incrociano, che pu&ograve; essere a livello o con diverse configurazioni per il traffico.",
             "<b>Intersection:</b> a point where two or more roads cross, which may be at the same level or have different traffic configurations."],
            ["<b>Intersezione a raso</b>",
             "Incrocio in cui due o pi&ugrave; strade si incontrano allo stesso livello.",
             "<b>At-grade intersection:</b> a crossing where two or more roads meet at the same level."],
            ["<b>Intersezione a livelli sfalsati</b>",
             "&Egrave; un'intersezione di due o pi&ugrave; strade situate ad altezze/livelli diverse.",
             "<b>Grade-separated intersection:</b> an intersection of two or more roads located at different heights/levels (e.g. overpasses)."],
            ["<b>Passaggio a livello</b>",
             "Incrocio tra una strada e una linea ferroviaria sullo stesso piano.",
             "<b>Level crossing:</b> a crossing between a road and a railway line on the same level."],
            ["<b>Passo carrabile</b>",
             "Accesso privato che collega una propriet&agrave; a una strada, segnalato da un cartello specifico.",
             "<b>Driveway access:</b> a private access connecting a property to the road, marked by a specific sign (parking in front of it is forbidden)."],
        ]},

        # ---------------------------------------------------------------
        {"type": "h2", "text": "4. Zone e aree speciali"},
        {"type": "table", "headers": HEADERS, "widths": W, "rows": [
            ["<b>Zona a traffico limitato (ZTL)</b>",
             "Area in cui l'accesso ai veicoli &egrave; limitato in determinati orari per ridurre il traffico e migliorare la qualit&agrave; dell'aria.",
             "<b>Limited Traffic Zone (ZTL):</b> an area where vehicle access is restricted at certain times to reduce traffic and improve air quality."],
            ["<b>Area pedonale</b>",
             "Spazio urbano riservato esclusivamente ai pedoni, dove i veicoli non possono entrare.",
             "<b>Pedestrian area:</b> an urban space reserved exclusively for pedestrians, where vehicles cannot enter."],
            ["<b>Pista ciclabile</b>",
             "Percorso separato dalla carreggiata destinato al traffico di biciclette.",
             "<b>Bike lane / cycle path:</b> a path separated from the carriageway meant for bicycle traffic."],
            ["<b>Centro abitato</b>",
             "Area edificata con almeno 25 edifici, come un quartiere all'interno di una citt&agrave;.",
             "<b>Built-up area:</b> a built area with at least 25 buildings, like a neighborhood within a city."],
            ["<b>Parcheggio</b>",
             "Area destinata alla sosta dei veicoli.",
             "<b>Parking:</b> an area designated for the parking (stopping) of vehicles."],
            ["<b>Zona di preselezione</b>",
             "Area della strada che precede un incrocio dove i veicoli devono disporsi in corsie specifiche in base alla direzione che intendono prendere.",
             "<b>Pre-selection zone:</b> an area of the road before an intersection where vehicles must position themselves in specific lanes based on the direction they intend to take."],
        ]},

        # ---------------------------------------------------------------
        {"type": "h2", "text": "5. Tipi di corsie"},
        {"type": "table", "headers": HEADERS, "widths": W, "rows": [
            ["<b>Corsia di marcia</b>",
             "La corsia principale per i veicoli che si muovono nella stessa direzione. I veicoli devono restare in questa corsia salvo sorpasso o uscita.",
             "<b>Driving lane:</b> the main lane for vehicles moving in the same direction. Vehicles must stay in this lane unless overtaking or exiting."],
            ["<b>Corsia di sorpasso</b>",
             "Corsia usata specificamente per sorpassare i veicoli pi&ugrave; lenti; di solito si trova a sinistra. Dopo il sorpasso si deve rientrare nella corsia di marcia.",
             "<b>Overtaking lane:</b> a lane used specifically to overtake slower vehicles; usually located on the left. After overtaking, drivers must return to the driving lane."],
            ["<b>Corsia di accelerazione</b>",
             "Corsia per i veicoli che entrano in autostrada o in una strada veloce, per accelerare e adeguarsi al flusso del traffico prima di immettersi.",
             "<b>Acceleration lane:</b> a lane for vehicles entering a motorway or fast road, allowing them to speed up to match the flow of traffic before merging."],
            ["<b>Corsia di decelerazione</b>",
             "Corsia usata dai veicoli che escono dall'autostrada o da una strada veloce, per rallentare in sicurezza prima dell'uscita o del casello.",
             "<b>Deceleration lane:</b> a lane used by vehicles exiting a motorway or fast road, allowing them to slow down safely before reaching an exit or toll booth."],
            ["<b>Corsia riservata</b>",
             "Corsia riservata a veicoli specifici, come autobus, taxi o mezzi di emergenza. I veicoli normali non possono usarla.",
             "<b>Reserved lane:</b> a lane reserved for specific vehicles, such as buses, taxis or emergency vehicles. Regular vehicles are prohibited from using it."],
            ["<b>Corsia di emergenza</b>",
             "Corsia situata all'estrema destra dell'autostrada, usata solo per emergenze, guasti o mezzi di soccorso. &Egrave; vietato circolarvi.",
             "<b>Emergency lane:</b> a lane located on the far right of a motorway, used only for emergencies, breakdowns or emergency services. Driving in this lane is forbidden."],
            ["<b>Corsia centrale</b>",
             "Corsia condivisa spesso presente in aree urbane per la svolta a sinistra, utilizzabile dai veicoli di entrambe le direzioni.",
             "<b>Central lane:</b> a shared lane often found in urban areas for turning left, allowing vehicles from both directions to use it."],
        ]},

        # ---------------------------------------------------------------
        {"type": "h2", "text": "6. Classificazione delle strade"},
        {"type": "table", "headers": HEADERS, "widths": W, "rows": [
            ["<b>Autostrada</b>",
             "Strada caratterizzata da carreggiate separate da uno spartitraffico invalicabile, con almeno due corsie per carreggiata. &Egrave; progettata per categorie specifiche di veicoli e di solito ha aree di servizio, corsie di emergenza, corsie di accelerazione e decelerazione. Non ci sono incroci a raso.",
             "<b>Motorway:</b> a road with carriageways separated by an impassable divider, with at least two lanes per carriageway. It is designed for specific vehicle categories and usually has service areas, emergency lanes and acceleration/deceleration lanes. There are no at-grade crossings."],
            ["<b>Strada extraurbana principale</b>",
             "Condivide le caratteristiche con l'autostrada (carreggiate separate e almeno due corsie per senso di marcia). Tuttavia, potrebbe consentire l'accesso a propriet&agrave; private.",
             "<b>Main extra-urban road:</b> shares the features of a motorway (separated carriageways and at least two lanes per direction). However, it may allow access to private properties."],
            ["<b>Strada extraurbana secondaria</b>",
             "Solitamente ha una sola carreggiata con almeno una corsia per direzione e banchine. Un esempio tipico &egrave; una strada provinciale che attraversa zone rurali.",
             "<b>Secondary extra-urban road:</b> usually has a single carriageway with at least one lane per direction and shoulders. A typical example is a provincial road crossing rural areas."],
            ["<b>Strada urbana di scorrimento</b>",
             "Strade urbane con carreggiate separate da spartitraffico, almeno due corsie per senso di marcia e spesso marciapiedi e corsie dedicate ai mezzi pubblici. Possono avere incroci regolati da semafori.",
             "<b>Urban through road:</b> urban roads with carriageways separated by a divider, at least two lanes per direction, and often sidewalks and lanes dedicated to public transport. They may have intersections regulated by traffic lights."],
            ["<b>Strada urbana di quartiere</b>",
             "Strade residenziali con una carreggiata e almeno due corsie; spesso consentono il parcheggio lungo la strada.",
             "<b>Urban neighborhood road:</b> residential roads with a single carriageway and at least two lanes; they often allow parking along the road."],
        ]},

        # ---------------------------------------------------------------
        {"type": "h2", "text": "Punti chiave da memorizzare"},
        {"type": "bullets", "items": [
            "<b>STRADA</b> = tutto; <b>CARREGGIATA</b> = solo la parte dei veicoli; <b>CORSIA</b> = una sola fila.",
            "La carreggiata NON comprende: marciapiedi, banchine, piste ciclabili, piazzole di sosta, corsie d'emergenza.",
            "<b>Centro abitato</b> = area con <b>almeno 25 edifici</b> (numero d'esame!).",
            "<b>A raso</b> = stesso livello; <b>a livelli sfalsati</b> = livelli diversi.",
            "<b>Passaggio a livello</b> = strada + ferrovia; <b>Passo carrabile</b> = accesso privato.",
            "<b>Autostrada</b>: spartitraffico invalicabile, &ge;2 corsie per carreggiata, nessun incrocio a raso.",
            "&Egrave; <b>vietato</b> circolare nella corsia di emergenza salvo reale emergenza.",
            "<b>Salvagente</b> = rifugio per i pedoni; <b>Isola di traffico</b> = gestisce il flusso (rotatorie).",
        ]},
    ],
}

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs("sections", exist_ok=True)
    build_section(SECTION, "sections/Section_02_The_Road.pdf")
