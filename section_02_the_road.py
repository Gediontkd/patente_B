#!/usr/bin/env python3
import os
from build_pdf import build_section

CM = 28.35  # points per cm helper for column widths

SECTION = {
    "title": "Section 2: The Road",
    "subtitle": "La strada - Types of Roads and Road-related Terms",
    "blocks": [
        # ---------------------------------------------------------------
        {"type": "h2", "text": "1. The Three Core Definitions"},
        {"type": "table",
         "headers": ["Italian", "English", "Meaning / Notes"],
         "widths": [3.4*CM, 3.2*CM, 9.0*CM],
         "rows": [
            ["Strada", "Road", "Public area designed for the movement of <b>pedestrians, vehicles and animals</b>. Includes sidewalks (urban) or shoulders (non-urban), bike lanes and carriageways"],
            ["Carreggiata", "Carriageway", "Part of the road for <b>vehicle circulation</b>. Does NOT include sidewalks, shoulders, bike lanes, lay-bys (piazzole di sosta) or emergency lanes. Can be <b>one-way</b> (senso unico) or <b>two-way</b> (doppio senso)"],
            ["Corsia", "Lane", "<b>Longitudinal division</b> of the carriageway for a <b>single line of vehicles</b>"],
         ]},

        # ---------------------------------------------------------------
        {"type": "h2", "text": "2. Pedestrian & Edge Areas"},
        {"type": "table",
         "headers": ["Italian", "English", "Meaning / Notes"],
         "widths": [4.2*CM, 3.6*CM, 7.8*CM],
         "rows": [
            ["Attraversamento pedonale", "Pedestrian crossing (zebra crossing)", "Area of the carriageway marked by <b>white stripes</b> where pedestrians can cross safely"],
            ["Banchina", "Shoulder / verge", "Strip of ground along the <b>edge</b> of the carriageway. Used for <b>emergency stops</b> or to separate the carriageway from adjacent areas"],
            ["Marciapiede", "Sidewalk / pavement", "Paved space along the <b>sides</b> of a road, for pedestrians"],
            ["Salvagente", "Pedestrian refuge island", "Raised or marked area <b>within</b> the carriageway acting as a refuge for pedestrians, often near intersections"],
            ["Isola di traffico", "Traffic island", "Raised or marked area within the carriageway to <b>manage traffic flow</b>, often found in roundabouts"],
         ]},

        # ---------------------------------------------------------------
        {"type": "h2", "text": "3. Intersections & Crossings"},
        {"type": "table",
         "headers": ["Italian", "English", "Meaning / Notes"],
         "widths": [4.6*CM, 3.8*CM, 7.2*CM],
         "rows": [
            ["Intersezione", "Intersection", "Point where <b>two or more roads cross</b>; can be at the same level or with various traffic configurations"],
            ["Intersezione a raso", "At-grade intersection", "Crossing where two or more roads meet at the <b>same level</b>"],
            ["Intersezione a livelli sfalsati", "Grade-separated intersection", "Intersection of roads at <b>different heights / levels</b> (e.g. overpasses)"],
            ["Passaggio a livello", "Level crossing", "Intersection between a <b>road and a railway</b> on the same level"],
            ["Passo carrabile", "Driveway access", "<b>Private access</b> connecting a property to the road; marked by a specific sign (parking forbidden in front of it)"],
         ]},

        # ---------------------------------------------------------------
        {"type": "h2", "text": "4. Zones & Special Areas"},
        {"type": "table",
         "headers": ["Italian", "English", "Meaning / Notes"],
         "widths": [4.4*CM, 3.6*CM, 7.6*CM],
         "rows": [
            ["Zona a traffico limitato (ZTL)", "Limited Traffic Zone", "Area where vehicle access is <b>restricted at certain times</b> to reduce traffic and improve air quality"],
            ["Area pedonale", "Pedestrian area", "Urban space reserved <b>exclusively for pedestrians</b>; vehicles cannot enter"],
            ["Pista ciclabile", "Bike lane / cycle path", "Path <b>separated from the carriageway</b> for bicycle traffic"],
            ["Centro abitato", "Built-up area", "Built area with <b>at least 25 buildings</b>, like a neighborhood within a city"],
            ["Parcheggio", "Parking", "Area designated for the <b>parking (sosta)</b> of vehicles"],
            ["Zona di preselezione", "Pre-selection zone", "Area of the road <b>before an intersection</b> where vehicles must position in specific lanes based on the direction they intend to take"],
         ]},

        # ---------------------------------------------------------------
        {"type": "h2", "text": "5. Lane Types (Corsie)"},
        {"type": "table",
         "headers": ["Italian", "English", "Meaning / Notes"],
         "widths": [4.6*CM, 3.4*CM, 7.6*CM],
         "rows": [
            ["Corsia di marcia", "Driving lane", "<b>Main lane</b> for vehicles going the same direction. Stay here unless overtaking or exiting"],
            ["Corsia di sorpasso", "Overtaking lane", "Lane used specifically for <b>overtaking</b> slower vehicles; usually on the <b>left</b>. Return to the driving lane after"],
            ["Corsia di accelerazione", "Acceleration lane", "Lane to <b>speed up</b> when entering a motorway, to match traffic flow before merging"],
            ["Corsia di decelerazione", "Deceleration lane", "Lane to <b>slow down safely</b> when exiting a motorway, before an exit or toll booth"],
            ["Corsia riservata", "Reserved lane", "Reserved for <b>specific vehicles</b> (buses, taxis, emergency). Regular vehicles prohibited"],
            ["Corsia di emergenza", "Emergency lane", "On the <b>far right</b> of a motorway; only for emergencies, breakdowns or emergency services. Driving in it is <b>forbidden</b>"],
            ["Corsia centrale", "Central lane", "Shared lane often in urban areas for <b>turning left</b>, usable by vehicles from both directions"],
         ]},

        # ---------------------------------------------------------------
        {"type": "h2", "text": "6. Road Classifications (by type)"},
        {"type": "table",
         "headers": ["Italian", "English", "Key features"],
         "widths": [4.8*CM, 3.4*CM, 7.4*CM],
         "rows": [
            ["Autostrada", "Motorway / Highway", "Carriageways separated by an <b>impassable divider</b>; at least <b>2 lanes per carriageway</b>; service areas, emergency lanes, accel./decel. lanes; <b>no at-grade crossings</b>; specific vehicle categories only"],
            ["Strada extraurbana principale", "Main extra-urban road", "Like a motorway (separated carriageways, &ge;2 lanes per direction) <b>but may allow access to private properties</b>"],
            ["Strada extraurbana secondaria", "Secondary extra-urban road", "Usually a <b>single carriageway</b> with at least one lane per direction and shoulders. E.g. a provincial road through rural areas"],
            ["Strada urbana di scorrimento", "Urban through road", "Urban roads with carriageways <b>separated by a divider</b>, &ge;2 lanes per direction, often sidewalks and public-transport lanes. May have <b>traffic-light intersections</b>"],
            ["Strada urbana di quartiere", "Urban neighborhood road", "<b>Residential</b> roads, single carriageway, at least two lanes; often allow <b>parking along the road</b>"],
         ]},

        # ---------------------------------------------------------------
        {"type": "h2", "text": "Key Points to Memorize"},
        {"type": "bullets", "items": [
            "<b>STRADA</b> = everything; <b>CARREGGIATA</b> = vehicle part only; <b>CORSIA</b> = one lane.",
            "Carriageway does NOT include: sidewalks, shoulders, bike lanes, lay-bys, emergency lanes.",
            "<b>Centro abitato</b> = built-up area with <b>at least 25 buildings</b> (common exam number!).",
            "<b>A raso</b> = same level; <b>a livelli sfalsati</b> = different levels.",
            "<b>Passaggio a livello</b> = road + railway; <b>Passo carrabile</b> = private driveway entrance.",
            "<b>Autostrada</b>: impassable divider, &ge;2 lanes/carriageway, NO at-grade crossings.",
            "Driving in the <b>emergency lane (corsia di emergenza)</b> is forbidden except for real emergencies.",
            "<b>Salvagente</b> = refuge for pedestrians; <b>Isola di traffico</b> = manages traffic flow (roundabouts).",
        ]},
    ],
}

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs("sections", exist_ok=True)
    build_section(SECTION, "sections/Section_02_The_Road.pdf")
