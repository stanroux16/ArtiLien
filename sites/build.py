#!/usr/bin/env python3
"""Générateur de maquettes de sites pour artisans/commerçants.
Usage : python3 build.py clients/<fichier>.json   (ou sans argument : tous les clients)
Sortie : dist/<slug>/  (site statique prêt à déployer)
"""
import json, sys, html, pathlib, shutil, re, subprocess, tempfile

ROOT = pathlib.Path(__file__).parent
E = html.escape

# ---------- icônes (SVG trait) ----------
ICONS = {
    "wrench": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5L3 17.6V21h3.4l6.3-6.3a4 4 0 0 0 5-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/>',
    "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    "brick": '<path d="M3 5h18v14H3zM3 12h18M9 5v7M15 12v7"/>',
    "brush": '<path d="M4 20c3 0 5-1 5-3a3 3 0 0 0-3-3c-2 0-2 3-3 6zM9 14 20 3l1 1-11 11z"/>',
    "drop": '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>',
    "home": '<path d="M3 11 12 3l9 8M5 10v10h14V10M10 20v-6h4v6"/>',
    "scissors": '<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M8.5 8 20 19M8.5 16 20 5"/>',
    "sparkle": '<path d="M12 3v6M12 15v6M3 12h6M15 12h6M6 6l3 3M15 15l3 3M18 6l-3 3M9 15l-3 3"/>',
    "leaf": '<path d="M5 19c0-9 5-14 15-14 0 10-5 15-14 15M5 19c3-5 6-8 10-10"/>',
    "hand": '<path d="M8 13V5a1.5 1.5 0 0 1 3 0v6M11 11V3.5a1.5 1.5 0 0 1 3 0V11M14 11V5.5a1.5 1.5 0 0 1 3 0V13c0 5-3 8-6 8-4 0-5-3-7-6l-1-2a1.5 1.5 0 0 1 2.5-1.5L8 14"/>',
    "bread": '<path d="M4 11c0-4 4-7 8-7s8 3 8 7v1H4zM5 12v7h14v-7M9 8l1 3M13 7l1 4"/>',
    "cake": '<path d="M4 12h16v8H4zM4 16c3 2 5-2 8 0s5-2 8 0M12 12V8M12 5v1"/>',
    "cup": '<path d="M5 8h12v6a5 5 0 0 1-5 5h-2a5 5 0 0 1-5-5zM17 9h2a2 2 0 0 1 0 5h-2M8 3v2M12 3v2"/>',
    "basket": '<path d="M3 10h18l-2 10H5zM8 10l3-6M16 10l-3-6"/>',
    "car": '<path d="M3 15v-3l2-5h14l2 5v3zM3 15v3h3v-3M18 15v3h3v-3M5 12h14"/>',
    "gear": '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/>',
    "shield": '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>',
    "spray": '<path d="M7 9h6v12H7zM9 9V5h3l2 2M16 5h2M16 8h3M16 11h2"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "phone": '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/>',
    "pin": '<path d="M12 21s7-6.2 7-11a7 7 0 0 0-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "mail": '<path d="M3 6h18v12H3zM3 7l9 7 9-7"/>',
}

def icon(name, size=28):
    return (f'<svg class="ico" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true">{ICONS.get(name, ICONS["gear"])}</svg>')

# ---------- thèmes par secteur ----------
THEMES = {
    "batiment": {
        "fonts": "Barlow+Condensed:wght@500;600;700&family=Barlow:wght@400;500;600",
        "h": "'Barlow Condensed', 'Arial Narrow', sans-serif", "b": "'Barlow', system-ui, sans-serif",
        "palettes": {
            "orange": dict(bg="#f1eee8", ink="#1d2430", acc="#e8590c", acc2="#1d2430", soft="#e4dfd5", dark="#1d2430"),
            "bleu":   dict(bg="#eef0f2", ink="#14202e", acc="#1f5f99", acc2="#f2b705", soft="#dfe4e9", dark="#14202e"),
            "vert":   dict(bg="#eff0ea", ink="#1c261f", acc="#2f6b45", acc2="#d9822b", soft="#e0e3d9", dark="#1c261f"),
        },
        "defaut_palette": "orange",
        "tag": "Artisan du bâtiment",
        "hero_kicker": "Devis gratuit sous 48 h",
        "default_services": [
            ("wrench", "Dépannage urgent", "Fuite, panne, blocage : nous intervenons rapidement et expliquons le prix avant de commencer."),
            ("home", "Rénovation complète", "Du diagnostic à la finition, un seul interlocuteur pour coordonner votre chantier."),
            ("brick", "Travaux neufs", "Installation soignée, matériaux sélectionnés, respect des normes en vigueur."),
            ("shield", "Entretien et contrats", "Vérifications régulières pour éviter les mauvaises surprises et prolonger vos équipements."),
        ],
        "valeurs": [("Devis clair", "Un prix écrit, détaillé, sans surprise à la facture."), ("Chantier propre", "Nous protégeons vos sols et nettoyons chaque jour."), ("Garantie", "Travaux garantis, assurance décennale à jour."), ("Délais tenus", "Un planning annoncé, respecté, communiqué.")],
        "etapes": ["Vous nous contactez", "Visite et devis gratuit", "Travaux soignés", "Réception et garantie"],
        "horaires": "Lun – Ven : 8h – 18h · Urgences : 7j/7",
    },
    "beaute": {
        "fonts": "Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Jost:wght@400;500",
        "h": "'Cormorant Garamond', Georgia, serif", "b": "'Jost', system-ui, sans-serif",
        "palettes": {
            "sauge":  dict(bg="#f6f1ea", ink="#2b2a26", acc="#5f7a62", acc2="#c9785b", soft="#ebe3d7", dark="#2f3a32"),
            "rose":   dict(bg="#f8efec", ink="#34262a", acc="#b4586b", acc2="#7d8f7a", soft="#f0e0dc", dark="#3a2a2f"),
            "sable":  dict(bg="#f4eee4", ink="#2d2923", acc="#a9774a", acc2="#3f4f4a", soft="#e9dfce", dark="#2d2923"),
        },
        "defaut_palette": "sauge",
        "tag": "Institut & coiffure",
        "hero_kicker": "Sur rendez-vous",
        "default_services": [
            ("scissors", "Coupes & coiffures", "Coupe sur mesure, conseil personnalisé, finitions soignées."),
            ("brush", "Colorations", "Colorations, balayages et soins adaptés à la nature de vos cheveux."),
            ("sparkle", "Soins du visage", "Soins personnalisés pour révéler l’éclat naturel de votre peau."),
            ("hand", "Beauté des mains", "Manucure, pose de vernis et soins pour des mains impeccables."),
        ],
        "valeurs": [("Écoute", "Chaque rendez-vous commence par comprendre vos envies."), ("Produits choisis", "Des gammes sélectionnées pour leur qualité et leur douceur."), ("Hygiène", "Matériel désinfecté, espace entretenu entre chaque cliente."), ("Sur-mesure", "Aucune prestation standardisée : tout s’adapte à vous.")],
        "etapes": ["Vous réservez", "Échange sur vos envies", "Votre moment soin", "Conseils pour la maison"],
        "horaires": "Mar – Sam : 9h – 18h30 · Fermé dimanche et lundi",
    },
    "bouche": {
        "fonts": "Fraunces:opsz,wght@9..144,500;9..144,700&family=DM+Sans:wght@400;500",
        "h": "'Fraunces', Georgia, serif", "b": "'DM Sans', system-ui, sans-serif",
        "palettes": {
            "ble":    dict(bg="#faf3e6", ink="#3a2a1d", acc="#b8581f", acc2="#7a8b4f", soft="#f0e3c9", dark="#3a2a1d"),
            "cerise": dict(bg="#fbf1ea", ink="#3b2320", acc="#a82e3a", acc2="#c79a3a", soft="#f2dfd2", dark="#3b2320"),
            "olive":  dict(bg="#f6f2e4", ink="#2e2b1a", acc="#6c7a2b", acc2="#b8581f", soft="#ebe4c8", dark="#2e2b1a"),
        },
        "defaut_palette": "ble",
        "tag": "Artisan de bouche",
        "hero_kicker": "Fait maison, chaque jour",
        "default_services": [
            ("bread", "Pains & viennoiseries", "Pétris et cuits chaque matin, avec des farines choisies."),
            ("cake", "Pâtisseries & gâteaux", "Gâteaux du quotidien et créations sur commande pour vos fêtes."),
            ("basket", "Traiteur & plateaux", "Buffets, plateaux et menus pour vos réceptions, de 6 à 100 personnes."),
            ("cup", "Salon & snacking", "Sandwichs, formules du midi et boissons chaudes sur place."),
        ],
        "valeurs": [("Fait maison", "Tout est préparé dans notre laboratoire, sur place."), ("Produits de saison", "Nous travaillons avec des producteurs proches de chez nous."), ("Sur commande", "Gâteaux, buffets et menus personnalisés pour vos événements."), ("Chaque jour frais", "Fournées renouvelées dans la journée.")],
        "etapes": ["Vous nous contactez", "On valide la commande", "Préparation maison", "Retrait ou livraison"],
        "horaires": "Mar – Sam : 6h30 – 19h · Dim : 7h – 13h",
    },
    "auto": {
        "fonts": "Archivo:wght@500;700;800&family=Archivo+Narrow:wght@500;600",
        "h": "'Archivo', 'Arial Black', sans-serif", "b": "'Archivo Narrow', 'Arial Narrow', sans-serif",
        "palettes": {
            "rouge":  dict(bg="#eceae6", ink="#16181c", acc="#d9261c", acc2="#16181c", soft="#dedcd6", dark="#16181c"),
            "bleu":   dict(bg="#eceeef", ink="#12161c", acc="#1d5fd6", acc2="#12161c", soft="#dde1e4", dark="#12161c"),
            "jaune":  dict(bg="#efede6", ink="#17171a", acc="#e0a400", acc2="#17171a", soft="#e1ddd0", dark="#17171a"),
        },
        "defaut_palette": "rouge",
        "tag": "Garage & carrosserie",
        "hero_kicker": "Devis en ligne gratuit",
        "default_services": [
            ("gear", "Entretien & révision", "Vidange, freins, distribution : toutes marques, respect des préconisations constructeur."),
            ("car", "Carrosserie & peinture", "Réparation de chocs, rayures et peinture au plus près de la teinte d’origine."),
            ("wrench", "Mécanique générale", "Diagnostic électronique, embrayage, suspension, climatisation."),
            ("shield", "Contrôle technique", "Préparation au contrôle technique et contre-visite."),
        ],
        "valeurs": [("Toutes marques", "Véhicules particuliers et utilitaires."), ("Devis détaillé", "Pièces et main-d’œuvre expliquées avant intervention."), ("Délais annoncés", "Vous savez quand récupérer votre véhicule."), ("Pièces garanties", "Pièces de qualité équivalente ou d’origine, garanties.")],
        "etapes": ["Prise de rendez-vous", "Diagnostic et devis", "Réparation", "Restitution et conseils"],
        "horaires": "Lun – Ven : 8h – 12h / 14h – 18h30 · Sam : 8h – 12h",
    },
}

# ---------- illustrations de hero ----------
def hero_art(secteur):
    if secteur == "batiment":
        return ('<svg viewBox="0 0 520 420" class="art" role="img" aria-label="Plan de maison"><defs><pattern id="g" width="26" height="26" patternUnits="userSpaceOnUse"><path d="M26 0H0V26" fill="none" stroke="currentColor" stroke-opacity=".12"/></pattern></defs>'
                '<rect width="520" height="420" fill="url(#g)"/><g fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round">'
                '<path d="M80 230 260 90l180 140"/><path d="M110 210v150h300V210"/><path d="M230 360V270h60v90"/><path d="M140 250h56v50h-56zM324 250h56v50h-56z"/></g>'
                '<g stroke="var(--acc)" stroke-width="2" fill="none"><path d="M80 392h360M80 384v16M440 384v16"/><path d="M470 90v270M462 90h16M462 360h16"/></g>'
                '<text x="260" y="412" text-anchor="middle" font-size="14" fill="var(--acc)" font-family="monospace">12,00 m</text></svg>')
    if secteur == "beaute":
        return ('<svg viewBox="0 0 520 460" class="art" role="img" aria-label="Illustration"><path d="M60 460V210a200 200 0 0 1 400 0v250z" fill="var(--soft)"/>'
                '<path d="M110 460V220a150 150 0 0 1 300 0v240z" fill="none" stroke="var(--acc)" stroke-width="2"/>'
                '<g fill="none" stroke="var(--ink)" stroke-width="2.4" stroke-linecap="round"><circle cx="260" cy="170" r="52"/><path d="M215 155c8-30 70-48 90-4-30-4-55 0-90 4z" fill="var(--acc)" stroke="none" opacity=".85"/><path d="M170 460c0-70 40-110 90-110s90 40 90 110"/></g>'
                '<g fill="var(--acc2)"><circle cx="420" cy="90" r="9"/><circle cx="90" cy="120" r="5"/><circle cx="440" cy="300" r="6"/></g></svg>')
    if secteur == "bouche":
        return ('<svg viewBox="0 0 520 440" class="art" role="img" aria-label="Illustration"><circle cx="270" cy="220" r="190" fill="var(--soft)"/>'
                '<g fill="none" stroke="var(--ink)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M120 260c0-70 60-120 150-120s150 50 150 120z" fill="var(--acc)" fill-opacity=".9"/><path d="M120 260v34c0 20 14 34 34 34h232c20 0 34-14 34-34v-34"/><path d="M200 175l14 38M268 160l8 50M338 175l-14 38"/></g>'
                '<g stroke="var(--acc2)" stroke-width="3" fill="none" stroke-linecap="round"><path d="M70 120c10 30 10 70 0 100M70 150l-18-12M70 175l-20-8M70 150l18-12M70 175l20-8"/><path d="M455 80c10 30 10 70 0 100M455 110l-18-12M455 135l-20-8M455 110l18-12M455 135l20-8"/></g></svg>')
    return ('<svg viewBox="0 0 560 360" class="art" role="img" aria-label="Voiture"><g fill="none" stroke="currentColor" stroke-width="4" stroke-linejoin="round" stroke-linecap="round">'
            '<path d="M40 250c0-30 10-42 40-48l70-18 48-64c8-10 18-14 32-14h130c18 0 30 6 42 18l62 62 52 12c20 5 28 14 28 34v18c0 8-6 14-14 14h-40M40 250v18c0 8 6 14 14 14h38"/>'
            '<path d="M170 118l-34 70h300l-66-66"/><path d="M300 108v78"/><circle cx="132" cy="282" r="40"/><circle cx="132" cy="282" r="14"/><circle cx="428" cy="282" r="40"/><circle cx="428" cy="282" r="14"/><path d="M172 282h216"/></g>'
            '<g stroke="var(--acc)" stroke-width="6" stroke-linecap="round"><path d="M10 330h120M30 346h90M0 314h80"/></g></svg>')

# ---------- CSS ----------
BASE_CSS = """
*{box-sizing:border-box;margin:0}html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--ink);font-family:var(--b);font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased}
img,svg{max-width:100%;display:block}a{color:inherit}
h1,h2,h3{font-family:var(--h);line-height:1.08;letter-spacing:-.01em}
.wrap{width:min(1120px,92vw);margin-inline:auto}
.ribbon{background:var(--dark);color:#f4f1ea;font-size:13px;padding:7px 0;text-align:center;font-family:system-ui,sans-serif}
.ribbon b{color:#fff;background:var(--acc);padding:1px 8px;margin-right:4px}
header.top{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid color-mix(in srgb,var(--ink) 12%,transparent)}
.bar{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:14px 0}
.logo{display:flex;align-items:center;gap:10px;font-family:var(--h);font-weight:700;font-size:1.45rem;text-decoration:none}
.logo .mark{width:34px;height:34px;display:grid;place-items:center;background:var(--acc);color:#fff}
nav ul{display:flex;gap:26px;list-style:none;padding:0;align-items:center}
nav a{text-decoration:none;font-weight:500;font-size:.98rem}nav a:hover{color:var(--acc)}
.btn{display:inline-flex;align-items:center;gap:8px;background:var(--acc);color:#fff;text-decoration:none;font-weight:600;padding:13px 24px;border:2px solid var(--acc);cursor:pointer;font-family:var(--b);font-size:1rem;transition:transform .15s,background .15s}
.btn:hover{transform:translateY(-2px)}.btn.ghost{background:transparent;color:var(--ink);border-color:var(--ink)}
.btn.ghost:hover{background:var(--ink);color:var(--bg)}
.burger{display:none;background:none;border:2px solid var(--ink);padding:6px 10px;font-weight:600;cursor:pointer;color:inherit}
.hero{padding:70px 0 80px;position:relative;overflow:hidden}
.hero .grid{display:grid;grid-template-columns:1.1fr .9fr;gap:50px;align-items:center}
.kicker{display:inline-block;font-size:.82rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--acc);margin-bottom:18px}
.hero h1{font-size:clamp(2.6rem,6vw,4.9rem);margin-bottom:22px}
.hero p.lead{font-size:1.2rem;max-width:34em;margin-bottom:30px;opacity:.88}
.hero .cta{display:flex;flex-wrap:wrap;gap:14px}
.art{width:100%;height:auto;color:var(--ink)}
.facts{display:flex;flex-wrap:wrap;gap:10px 30px;margin-top:34px;font-size:.95rem}
.facts span{display:flex;gap:8px;align-items:center}.facts .ico{color:var(--acc)}
section{padding:78px 0}section.alt{background:var(--soft)}
.sec-head{max-width:640px;margin-bottom:44px}.sec-head h2{font-size:clamp(2rem,4vw,3rem);margin-bottom:12px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(235px,1fr));gap:22px}
.card{background:var(--bg);padding:30px 26px;border:1px solid color-mix(in srgb,var(--ink) 14%,transparent);transition:transform .2s,box-shadow .2s}
.alt .card{background:var(--bg)}.card:hover{transform:translateY(-4px);box-shadow:0 14px 30px -18px rgba(0,0,0,.35)}
.card .ico{color:var(--acc);margin-bottom:16px}.card h3{font-size:1.45rem;margin-bottom:8px}.card p{opacity:.85;font-size:.98rem}
.split{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center}
.ph{aspect-ratio:4/3;background:repeating-linear-gradient(135deg,var(--soft) 0 14px,color-mix(in srgb,var(--soft) 82%,var(--ink)) 14px 15px);display:grid;place-items:center;color:color-mix(in srgb,var(--ink) 55%,transparent);font-size:.9rem;text-align:center;padding:20px;border:1px solid color-mix(in srgb,var(--ink) 15%,transparent)}
.steps{counter-reset:s;display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:26px;list-style:none;padding:0}
.steps li{counter-increment:s;border-top:3px solid var(--acc);padding-top:16px}
.steps li::before{content:"0" counter(s);font-family:var(--h);font-size:2.4rem;font-weight:700;color:var(--acc);display:block;line-height:1}
.steps li{font-weight:500;font-size:1.1rem}
.quote{background:var(--dark);color:#f4f1ea;padding:38px;max-width:760px}.quote p{font-family:var(--h);font-size:1.7rem;line-height:1.3}.quote small{display:block;margin-top:14px;opacity:.7;font-family:var(--b);font-size:.9rem}
.band{background:var(--acc);color:#fff;padding:54px 0}.band .in{display:flex;flex-wrap:wrap;gap:20px;justify-content:space-between;align-items:center}.band h2{font-size:clamp(1.8rem,3.4vw,2.6rem);max-width:20em}
.band .btn{background:#fff;color:var(--ink);border-color:#fff}
form.contact{display:grid;gap:16px}label{font-weight:600;font-size:.92rem;display:block;margin-bottom:6px}
input,select,textarea{width:100%;padding:13px 14px;border:1.5px solid color-mix(in srgb,var(--ink) 35%,transparent);background:#fff;font:inherit;color:#222;border-radius:0}
input:focus,select:focus,textarea:focus{outline:3px solid color-mix(in srgb,var(--acc) 40%,transparent);border-color:var(--acc)}
.row2{display:grid;grid-template-columns:1fr 1fr;gap:16px}.check{display:flex;gap:10px;align-items:flex-start;font-size:.88rem}.check input{width:auto;margin-top:5px}
.info{display:grid;gap:18px}.info div{display:flex;gap:14px;align-items:flex-start}.info .ico{color:var(--acc);flex:none;margin-top:3px}
.ok{display:none;background:var(--acc);color:#fff;padding:16px 18px;font-weight:500}
.legal{max-width:760px}.legal h2{font-size:1.7rem;margin:34px 0 10px}.legal p,.legal li{margin-bottom:10px}.legal ul{padding-left:20px}
.todo{background:#fff3c4;color:#5a4500;padding:1px 6px;font-size:.92em}
.notice{border-left:4px solid var(--acc2);background:var(--soft);padding:14px 18px;font-size:.92rem;margin-bottom:28px}
footer{background:var(--dark);color:#d9d5cb;padding:54px 0 28px;font-size:.95rem}
footer .cols{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:36px;margin-bottom:34px}footer h4{font-family:var(--h);font-size:1.2rem;color:#fff;margin-bottom:10px}
footer a{display:block;text-decoration:none;margin-bottom:6px}footer a:hover{color:#fff}footer .base{border-top:1px solid #ffffff22;padding-top:18px;font-size:.84rem;opacity:.75}
@media(max-width:860px){.hero .grid,.split,footer .cols,.row2{grid-template-columns:1fr}.hero{padding:44px 0 56px}.art{max-width:420px;margin-inline:auto}
nav ul{display:none;position:absolute;left:0;right:0;top:100%;background:var(--bg);flex-direction:column;padding:20px 4vw;gap:16px;border-bottom:1px solid #0002}nav ul.open{display:flex}.burger{display:block}section{padding:56px 0}}
"""

# CSS spécifique par secteur (le "caractère" du métier)
EXTRA_CSS = {
    "batiment": """
.hero{background:linear-gradient(90deg,transparent 0 0)}.hero h1{text-transform:uppercase;font-weight:700;letter-spacing:.005em}
.hero h1 em{font-style:normal;color:var(--acc);display:block}
.btn,.card,.quote,.ph,input,textarea,select{border-radius:0}
.card{border-top:4px solid var(--acc)}.logo .mark{clip-path:polygon(0 0,100% 0,100% 70%,70% 100%,0 100%)}
section.alt{background:var(--soft)}.kicker{background:var(--ink);color:#fff;padding:5px 12px}
""",
    "beaute": """
body{font-size:17.5px}.hero h1{font-weight:500}.hero h1 em{font-style:italic;color:var(--acc)}
.btn{border-radius:999px;padding:13px 30px}.card{border-radius:140px 140px 18px 18px;padding-top:44px;text-align:center}
.card .ico{margin-inline:auto}.ph{border-radius:200px 200px 0 0}.quote{border-radius:0 80px 0 0}
.logo{font-weight:600;letter-spacing:.02em}.logo .mark{border-radius:50%}.kicker{letter-spacing:.24em}
input,textarea,select{border-radius:10px}.steps li{border-top:1px solid var(--acc)}
.band{border-radius:0}.sec-head h2{font-weight:500}
""",
    "bouche": """
.hero{background:radial-gradient(circle at 85% 20%,color-mix(in srgb,var(--acc2) 18%,transparent),transparent 45%)}
.hero h1{font-weight:700}.hero h1 em{font-style:italic;color:var(--acc);font-weight:500}
.btn{border-radius:14px}.card{border-radius:22px}.ph{border-radius:22px}.quote{border-radius:26px 26px 26px 4px}
.logo .mark{border-radius:50% 50% 50% 8px}input,textarea,select{border-radius:12px}
section.alt{background:var(--soft)}.steps li{border-radius:0;border-top:3px dotted var(--acc)}
""",
    "auto": """
.hero{background:var(--dark);color:#f2f0ea}.hero .art{color:#f2f0ea}.hero p.lead{opacity:.8}.hero .btn.ghost{color:#f2f0ea;border-color:#f2f0ea}.hero .btn.ghost:hover{background:#f2f0ea;color:var(--dark)}
.hero::after{content:"";position:absolute;right:-60px;bottom:0;width:46%;height:14px;background:var(--acc);transform:skewX(-35deg)}
.hero h1{text-transform:uppercase;font-weight:800;letter-spacing:-.02em}.hero h1 em{font-style:normal;color:var(--acc);display:block}
.hero .facts .ico{color:var(--acc)}.kicker{border-left:5px solid var(--acc);padding-left:10px}
.btn,.card,.ph,.quote,input,textarea,select{border-radius:2px}.btn{text-transform:uppercase;letter-spacing:.06em;font-size:.9rem;font-weight:700}
.card{border-left:5px solid var(--acc)}h2,h3{text-transform:uppercase;letter-spacing:-.005em}.logo{text-transform:uppercase}
.logo .mark{transform:skewX(-12deg)}.steps li::before{font-style:italic}
""",
}


# ---------- polices locales (aucune requête vers Google : RGPD, rendu identique partout, PDF fidèle) ----------
FONT_WEIGHTS = {
    "Barlow Condensed": [(500, "normal"), (600, "normal"), (700, "normal")],
    "Barlow": [(400, "normal"), (500, "normal"), (600, "normal")],
    "Cormorant Garamond": [(500, "normal"), (600, "normal"), (500, "italic")],
    "Jost": [(400, "normal"), (500, "normal")],
    "Fraunces": [(500, "normal"), (700, "normal")],
    "DM Sans": [(400, "normal"), (500, "normal")],
    "Archivo": [(500, "normal"), (700, "normal"), (800, "normal")],
    "Archivo Narrow": [(500, "normal"), (600, "normal")],
    "Playfair Display": [(600, "normal"), (700, "normal"), (600, "italic")],
    "Source Sans 3": [(400, "normal"), (500, "normal"), (600, "normal")],
    "Space Grotesk": [(500, "normal"), (700, "normal")],
    "Inter": [(400, "normal"), (500, "normal"), (600, "normal")],
}
FONT_SETS = {  # choix « Police » de la brochure : A = police du secteur (défaut), B, C
    "classique": {"label": "Classique et élégante", "h": "'Playfair Display', Georgia, serif", "b": "'Source Sans 3', system-ui, sans-serif"},
    "moderne": {"label": "Moderne et nette", "h": "'Space Grotesk', system-ui, sans-serif", "b": "'Inter', system-ui, sans-serif"},
}
FONTS_DIR = ROOT / "fonts"
PAL_LABELS = {"ble": "blé", "sauge": "sauge"}

def families_of(*stacks):
    out = []
    for st in stacks:
        m = re.match(r"\s*'([^']+)'", st or "")
        if m and m.group(1) in FONT_WEIGHTS and m.group(1) not in out:
            out.append(m.group(1))
    return out

def font_faces(families, used):
    css = []
    for fam in families:
        slug = fam.lower().replace(" ", "-")
        for w, st in FONT_WEIGHTS[fam]:
            fn = f"{slug}-latin-{w}-{st}.woff2"
            used.add(fn)
            css.append(f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:{st};font-display:swap;src:url(fonts/{fn}) format('woff2')}}")
    return "".join(css)

def theme_for(p, t):
    fs = FONT_SETS.get(p.get("police"))
    return {**t, "h": fs["h"], "b": fs["b"]} if fs else t

# ---------- logos (texte seul, pas de dessin inventé) ----------
LOGOS = {
    "icone": "Pictogramme du métier + nom (version actuelle)",
    "capitales": "Nom en capitales espacées",
    "souligne": "Nom souligné d’un trait de couleur",
    "deux-lignes": "Nom + métier et ville en petit",
    "point": "Nom suivi d’un point de couleur",
    "encadre": "Nom dans un cadre (style tampon)",
    "serif": "Nom en italique élégant",
}

def logo_inner(p, style, size=20):
    nom = E(p["nom"])
    if style == "icone":
        return f'<span class="mark">{icon(p.get("icone_logo") or THEMES[p["secteur"]]["default_services"][0][0], size)}</span>{nom}'
    if style == "deux-lignes":
        return f'<span class="lgt">{nom}</span><span class="lgs">{E(p["metier"])} · {E(p["ville"])}</span>'
    if style == "point":
        return f'<span class="lgt">{nom}<i class="dot"></i></span>'
    return f'<span class="lgt">{nom}</span>'

def logo_link(p, style, href="index.html"):
    return f'<a class="logo lg-{style}" href="{href}">{logo_inner(p, style)}</a>'

LOGO_CSS = """
.logo.lg-capitales .lgt{text-transform:uppercase;letter-spacing:.2em;font-size:1.1rem;font-weight:600}
.logo.lg-souligne .lgt{border-bottom:4px solid var(--acc);padding-bottom:2px}
.logo.lg-deux-lignes{flex-direction:column;align-items:flex-start;gap:2px;line-height:1.05}
.logo.lg-deux-lignes .lgs{font-family:var(--b);font-size:.6rem;letter-spacing:.2em;text-transform:uppercase;font-weight:500;opacity:.7}
.logo .dot{display:inline-block;width:.3em;height:.3em;border-radius:50%;background:var(--acc);margin-left:.1em}
.logo.lg-encadre .lgt{border:2.5px solid var(--acc);padding:3px 12px;letter-spacing:.03em}
.logo.lg-serif .lgt{font-family:'Playfair Display',Georgia,serif;font-style:italic;font-weight:600}
"""

# ---------- gabarits de page ----------
USED_FONTS = set()

def page_shell(p, t, pal, titre, body, active, extra_families=(), extra_css=""):
    nom = E(p["nom"])
    desc = E(p.get("description_seo") or f'{p["nom"]} – {p["metier"]} à {p["ville"]}. Devis, horaires et contact.')
    lstyle = p.get("logo", "icone")
    fams = families_of(t["h"], t["b"]) + [f for f in (list(extra_families) + (["Playfair Display"] if lstyle == "serif" else [])) if f not in families_of(t["h"], t["b"])]
    fonts = f"<style>{font_faces(fams, USED_FONTS)}</style>"
    css_vars = ":root{" + "".join(f"--{k}:{v};" for k, v in pal.items()) + f"--h:{t['h']};--b:{t['b']}" + "}"
    def nav_item(href, label, key):
        cur = ' aria-current="page"' if key == active else ""
        return f'<li><a href="{href}"{cur}>{label}</a></li>'
    nav = "".join([nav_item("index.html", "Accueil", "home"), nav_item("presentation.html", "Qui sommes-nous", "pres"),
                   nav_item("index.html#services", "Services", "serv"), nav_item("contact.html", "Contact", "contact")])
    ribbon = ""
    if p.get("maquette", True):
        ribbon = f'<div class="ribbon"><b>Maquette</b> proposée à {nom} par {E(p.get("agence", "votre agence web"))} — textes et visuels provisoires, tout est modifiable.</div>'
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(titre)} – {nom}</title><meta name="description" content="{desc}">{'<meta name="robots" content="noindex,nofollow">' if p.get("maquette", True) else ''}
{fonts}<style>{css_vars}{BASE_CSS}{LOGO_CSS}{EXTRA_CSS[p["secteur"]]}{extra_css}</style></head><body>
{ribbon}
<header class="top"><div class="wrap bar">{logo_link(p, lstyle)}
<nav><button class="burger" onclick="document.getElementById('m').classList.toggle('open')" aria-label="Menu">Menu</button><ul id="m">{nav}<li><a class="btn" href="contact.html">{E(p.get("cta", "Demander un devis"))}</a></li></ul></nav></div></header>
{body}
<footer><div class="wrap"><div class="cols"><div><h4>{nom}</h4><p>{E(p["slogan"])}</p><p style="margin-top:10px">{E(p["ville"])}{(' · ' + E(p['zone'])) if p.get('zone') else ''}</p></div>
<div><h4>Contact</h4><a href="tel:{E(p['tel'].replace(' ',''))}">{E(p['tel'])}</a><a href="mailto:{E(p['email'])}">{E(p['email'])}</a><a href="contact.html">{E(p['adresse'])}</a></div>
<div><h4>Informations</h4><a href="presentation.html">Qui sommes-nous</a><a href="mentions-legales.html">Mentions légales</a><a href="politique-confidentialite.html">Politique de confidentialité</a></div></div>
<div class="base">© {E(p.get("annee", "2026"))} {nom}. Tous droits réservés.</div></div></footer></body></html>"""

def services_of(p, t):
    if p.get("services"):
        return [(s.get("icone", "gear"), s["titre"], s["texte"]) for s in p["services"]]
    return t["default_services"]

def build_home(p, t, pal):
    sv = services_of(p, t)
    h1a, h1b = p.get("titre", ["", ""]) if p.get("titre") else (f'{p["metier"].capitalize()}', f'à {p["ville"]}')
    cards = "".join(f'<article class="card">{icon(i)}<h3>{E(ti)}</h3><p>{E(tx)}</p></article>' for i, ti, tx in sv)
    vals = "".join(f'<article class="card"><h3>{E(a)}</h3><p>{E(b)}</p></article>' for a, b in t["valeurs"])
    steps = "".join(f"<li>{E(s)}</li>" for s in t["etapes"])
    avis = p.get("avis") or {"texte": "Avis client à insérer ici : un témoignage réel renforce la confiance de vos futurs clients.", "auteur": "Prénom N., ville"}
    body = f"""
<section class="hero"><div class="wrap grid"><div><span class="kicker">{E(p.get("kicker", t["hero_kicker"]))}</span>
<h1>{E(h1a)} <em>{E(h1b)}</em></h1><p class="lead">{E(p["accroche"])}</p>
<div class="cta"><a class="btn" href="contact.html">{E(p.get("cta", "Demander un devis"))}</a><a class="btn ghost" href="tel:{E(p['tel'].replace(' ',''))}">{E(p['tel'])}</a></div>
<div class="facts"><span>{icon("clock", 20)}{E(p.get("horaires", t["horaires"]))}</span><span>{icon("pin", 20)}{E(p["ville"])}{(' et ' + E(p['zone'])) if p.get('zone') else ''}</span></div></div>
<div>{hero_art(p["secteur"])}</div></div></section>
<section id="services" class="alt"><div class="wrap"><div class="sec-head"><h2>Ce que nous faisons</h2><p>{E(p.get("intro_services", "Des prestations simples à comprendre, réalisées avec soin."))}</p></div><div class="cards">{cards}</div></div></section>
<section><div class="wrap split"><div class="ph">Photo de l’équipe ou de l’atelier<br>(à fournir par vous)</div><div><div class="sec-head" style="margin-bottom:20px"><h2>{E(p.get("titre_apropos", "Un métier, une façon de faire"))}</h2></div>
<p>{E(p["presentation"][0])}</p><p style="margin:14px 0 24px">{E(p["presentation"][1] if len(p["presentation"])>1 else "")}</p><a class="btn ghost" href="presentation.html">Découvrir notre histoire</a></div></div></section>
<section class="alt"><div class="wrap"><div class="sec-head"><h2>Pourquoi nous choisir</h2></div><div class="cards">{vals}</div></div></section>
<section><div class="wrap"><div class="sec-head"><h2>Comment ça se passe</h2></div><ol class="steps">{steps}</ol></div></section>
<section class="alt"><div class="wrap"><div class="quote"><p>« {E(avis["texte"])} »</p><small>{E(avis["auteur"])} <span style="opacity:.6">(exemple de mise en page)</span></small></div></div></section>
<div class="band"><div class="wrap in"><h2>{E(p.get("phrase_cta", "Parlez-nous de votre projet, nous revenons vers vous rapidement."))}</h2><a class="btn" href="contact.html">{E(p.get("cta", "Demander un devis"))}</a></div></div>"""
    return page_shell(p, t, pal, "Accueil", body, "home")

def build_pres(p, t, pal):
    paras = "".join(f"<p style='margin-bottom:14px'>{E(x)}</p>" for x in p["presentation"])
    vals = "".join(f'<article class="card"><h3>{E(a)}</h3><p>{E(b)}</p></article>' for a, b in t["valeurs"])
    body = f"""<section><div class="wrap split"><div><span class="kicker">Qui sommes-nous</span><div class="sec-head" style="margin-bottom:20px"><h2>{E(p["nom"])}</h2></div>{paras}
<p style="margin-top:20px"><b>{E(p.get("dirigeant", "Prénom Nom"))}</b>, {E(p.get("fonction", "gérant"))}</p></div><div class="ph">Portrait ou photo de l’atelier<br>(à fournir par vous)</div></div></section>
<section class="alt"><div class="wrap"><div class="sec-head"><h2>Nos engagements</h2></div><div class="cards">{vals}</div></div></section>
<div class="band"><div class="wrap in"><h2>Un projet ? Discutons-en.</h2><a class="btn" href="contact.html">Nous contacter</a></div></div>"""
    return page_shell(p, t, pal, "Qui sommes-nous", body, "pres")

def build_contact(p, t, pal):
    opts = "".join(f"<option>{E(s[1])}</option>" for s in services_of(p, t)) + "<option>Autre demande</option>"
    body = f"""<section><div class="wrap split" style="align-items:start"><div><span class="kicker">Contact</span><div class="sec-head" style="margin-bottom:24px"><h2>Parlons de votre besoin</h2><p>Réponse sous 24 h ouvrées.</p></div>
<div class="info"><div>{icon("phone", 22)}<span><b>Téléphone</b><br><a href="tel:{E(p['tel'].replace(' ',''))}">{E(p['tel'])}</a></span></div>
<div>{icon("mail", 22)}<span><b>Email</b><br><a href="mailto:{E(p['email'])}">{E(p['email'])}</a></span></div>
<div>{icon("pin", 22)}<span><b>Adresse</b><br>{E(p['adresse'])}</span></div>
<div>{icon("clock", 22)}<span><b>Horaires</b><br>{E(p.get("horaires", t["horaires"]))}</span></div></div></div>
<div><form class="contact" id="f" onsubmit="event.preventDefault();this.style.display='none';document.getElementById('ok').style.display='block'">
<div class="row2"><div><label for="n">Nom et prénom *</label><input id="n" name="nom" required autocomplete="name"></div><div><label for="t">Téléphone *</label><input id="t" name="tel" type="tel" required autocomplete="tel"></div></div>
<div><label for="e">Email *</label><input id="e" name="email" type="email" required autocomplete="email"></div>
<div><label for="s">Objet de la demande</label><select id="s" name="objet">{opts}</select></div>
<div><label for="m">Votre message *</label><textarea id="m" name="message" rows="5" required placeholder="Décrivez votre besoin en quelques lignes"></textarea></div>
<label class="check"><input type="checkbox" required><span>J’accepte que mes données soient utilisées pour répondre à ma demande, conformément à la <a href="politique-confidentialite.html">politique de confidentialité</a>.</span></label>
<button class="btn" type="submit">Envoyer ma demande</button></form>
<div class="ok" id="ok">Merci ! Votre message a bien été pris en compte (envoi simulé dans cette maquette).</div></div></div></section>"""
    return page_shell(p, t, pal, "Contact", body, "contact")

def todo(x):
    return f'<span class="todo">{E(x)}</span>'

def build_mentions(p, t, pal):
    l = p.get("legal", {})
    g = lambda k, d: E(l[k]) if l.get(k) else todo(d)
    body = f"""<section><div class="wrap legal"><div class="notice">Modèle fourni à titre indicatif : les champs surlignés sont à compléter, et le contenu est à faire valider avant publication.</div>
<h1 style="font-size:2.6rem">Mentions légales</h1>
<h2>Éditeur du site</h2><p>{E(p["nom"])}<br>Forme juridique : {g("forme", "ex. entrepreneur individuel / SARL")}<br>SIRET : {g("siret", "numéro SIRET")}<br>Adresse : {E(p["adresse"])}<br>Téléphone : {E(p["tel"])}<br>Email : {E(p["email"])}<br>TVA intracommunautaire : {g("tva", "numéro ou « non applicable »")}</p>
<h2>Directeur de la publication</h2><p>{g("directeur", "Prénom Nom")}</p>
<h2>Hébergeur</h2><p>Hostinger International Ltd., 61 Lordou Vironos Street, 6023 Larnaca, Chypre. Site : hostinger.fr</p>
<h2>Activité réglementée</h2><p>{g("reglemente", "assurance, qualification ou ordre professionnel si applicable (ex. garantie décennale : nom de l’assureur et couverture géographique)")}</p>
<h2>Propriété intellectuelle</h2><p>Les textes, images et éléments graphiques de ce site sont la propriété de {E(p["nom"])} ou utilisés avec autorisation. Toute reproduction sans accord préalable est interdite.</p>
<h2>Responsabilité</h2><p>Nous mettons tout en œuvre pour fournir des informations exactes, sans pouvoir garantir l’absence d’erreur. Les liens vers des sites tiers n’engagent pas notre responsabilité.</p>
<h2>Médiation de la consommation</h2><p>{g("mediateur", "nom et coordonnées du médiateur de la consommation, obligatoire pour les professionnels vendant à des consommateurs")}</p></div></section>"""
    return page_shell(p, t, pal, "Mentions légales", body, "")

def build_privacy(p, t, pal):
    body = f"""<section><div class="wrap legal"><div class="notice">Modèle fourni à titre indicatif, à faire valider avant publication.</div>
<h1 style="font-size:2.6rem">Politique de confidentialité</h1>
<h2>Responsable du traitement</h2><p>{E(p["nom"])}, {E(p["adresse"])}. Contact : {E(p["email"])}.</p>
<h2>Données collectées</h2><p>Via le formulaire de contact : nom, téléphone, adresse email et contenu de votre message. Aucune autre donnée n’est collectée volontairement par ce site.</p>
<h2>Finalité et base légale</h2><p>Ces données servent uniquement à répondre à votre demande (base légale : mesures précontractuelles et intérêt légitime). Elles ne sont ni vendues ni utilisées pour de la prospection sans votre accord.</p>
<h2>Durée de conservation</h2><p>Vos données sont conservées au maximum 3 ans après le dernier échange, puis supprimées.</p>
<h2>Destinataires</h2><p>Les données sont accessibles uniquement à {E(p["nom"])} et à son hébergeur technique, Hostinger, qui agit comme sous-traitant.</p>
<h2>Vos droits</h2><p>Vous pouvez demander l’accès, la rectification, l’effacement ou la limitation de vos données en écrivant à {E(p["email"])}. Vous pouvez aussi saisir la CNIL (cnil.fr).</p>
<h2>Cookies</h2><p>{todo("À adapter : ce site n’utilise aucun cookie de suivi par défaut. Si un outil de mesure d’audience ou une carte est ajouté, un bandeau de consentement sera nécessaire.")}</p></div></section>"""
    return page_shell(p, t, pal, "Politique de confidentialité", body, "")


# ---------- brochure de personnalisation (page + PDF) ----------
CHOIX_CSS = """
.ch-intro{padding:56px 0 20px}.ch-intro h1{font-size:clamp(2.2rem,5vw,3.6rem);margin-bottom:14px}.ch-intro p{max-width:46em;font-size:1.1rem;opacity:.88}
.ch-how{background:var(--dark);color:#f4f1ea;padding:18px 22px;margin-top:24px;max-width:46em;font-size:1rem}.ch-how b{color:#fff}
.ch-sec{padding:44px 0 8px}.ch-sec h2{font-size:clamp(1.7rem,3.4vw,2.4rem);margin-bottom:6px}.ch-sec>.wrap>p.sub{opacity:.8;margin-bottom:22px;max-width:48em}
.ch-num{display:inline-grid;place-items:center;width:38px;height:38px;background:var(--acc);color:#fff;font-family:var(--h);font-weight:700;margin-right:10px;font-size:1.2rem;vertical-align:middle}
.opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.opt{border:1px solid color-mix(in srgb,var(--ink) 16%,transparent);background:#fff;padding:0;overflow:hidden;break-inside:avoid;color:#1d2430}
.opt .tag{display:flex;align-items:center;gap:10px;padding:10px 14px;font-weight:600;font-size:.95rem;border-bottom:1px solid #0001;background:#faf9f6;font-family:system-ui,sans-serif}
.opt .tag i{font-style:normal;display:inline-grid;place-items:center;width:26px;height:26px;background:#1d2430;color:#fff;font-weight:700;font-size:.85rem}
.opt .body{padding:16px 14px;font-size:.95rem;line-height:1.5}
.pal{padding:16px}.pal .sw{display:flex;gap:6px;margin-top:12px}.pal .sw span{width:28px;height:28px;border-radius:50%;border:1px solid #0002}
.pal .mini{padding:14px;border-radius:2px}.pal .mini b{display:block;font-size:1.05rem;margin-bottom:6px}.pal .mini u{display:inline-block;text-decoration:none;padding:6px 12px;color:#fff;font-size:.8rem;font-weight:600}
.fnt .big{font-size:1.9rem;line-height:1.1;margin-bottom:8px}.fnt .txt{font-size:.98rem}
.lgbox{padding:22px 14px;display:flex;align-items:center;justify-content:center;background:var(--bg);color:var(--ink)}
.lgbox.dark{background:var(--dark);color:#fff}.lgbox .logo{pointer-events:none}
.tone q{display:block;font-family:var(--h);font-size:1.25rem;line-height:1.25;quotes:none}
.lst{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px 24px;list-style:none;padding:0}
.lst li{display:flex;gap:10px;align-items:flex-start;padding:8px 0;border-bottom:1px solid #0001}.lst .ico{color:var(--acc);flex:none;margin-top:2px}
.lst small{display:block;opacity:.7;font-size:.86rem}
.incl{background:var(--soft);padding:22px 26px;break-inside:avoid}.incl ul{padding-left:20px}.incl li{margin:4px 0}
.dl{display:inline-block;margin-top:20px}
@media print{@page{size:A4;margin:11mm}body{font-size:14px}header.top{position:static;backdrop-filter:none}nav,.dl,.burger{display:none!important}
.ch-sec{padding:14px 0 2px;break-inside:avoid}.ch-sec.long{break-inside:auto}.ch-sec h2{break-after:avoid}.ch-intro{padding:14px 0 4px}footer{display:none}.ribbon{font-size:11px}.opts{gap:10px;grid-template-columns:repeat(3,1fr)}.lst{grid-template-columns:repeat(2,1fr)}.opt .body{padding:10px 12px;font-size:.88rem}.fnt .big{font-size:1.5rem}.ch-sec>.wrap>p.sub{margin-bottom:10px}
.opt,.lgbox{-webkit-print-color-adjust:exact;print-color-adjust:exact}*{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
"""

TONES = [
    ("Convivial et proche", "Bienvenue chez {nom} ! {Metier} à {ville} : on prend le temps de vous écouter et de bien faire les choses."),
    ("Sérieux et rassurant", "{nom}, {metier} à {ville} : un travail soigné, des prix clairs et un interlocuteur qui répond."),
    ("Haut de gamme et sobre", "{nom} — {metier} à {ville}. Savoir-faire, qualité et attention aux détails."),
]
EXTRA_SECTIONS = {
    "batiment": [("shield", "Assurances et qualifications", "à afficher si vous en avez (décennale, RGE…)"), ("pin", "Zones d’intervention", "liste des villes ou carte")],
    "beaute": [("sparkle", "Tarifs des prestations", "liste claire, par catégorie"), ("clock", "Réservation en ligne", "bouton vers votre outil de rendez-vous existant")],
    "bouche": [("basket", "Carte et produits du jour", "mise à jour sur simple mail"), ("cake", "Commandes spéciales", "formulaire pour gâteaux, plateaux, événements")],
    "auto": [("car", "Marques et services", "ce que vous réparez ou entretenez"), ("clock", "Prise de rendez-vous atelier", "formulaire dédié")],
}
COMMON_SECTIONS = [
    ("brush", "Galerie de réalisations", "vos photos, présentées en grille"),
    ("hand", "Avis clients", "témoignages réels, avec leur accord"),
    ("clock", "Tarifs / devis type", "fourchettes de prix ou formules"),
    ("mail", "FAQ", "les questions que vos clients posent le plus"),
    ("pin", "Plan d’accès", "adresse, parking, accès"),
    ("phone", "Boutons d’appel et WhatsApp", "un clic pour vous joindre depuis un mobile"),
    ("leaf", "Réseaux sociaux", "liens vers vos pages Facebook, Instagram"),
    ("home", "Actualités et promotions", "une courte rubrique que vous alimentez par mail"),
]

def _choix_parts(p, t, pal, form=False):
    """Blocs de choix (couleurs, polices, logos, tons, photos, sections). form=True : cases à cocher/boutons radio."""
    nom = E(p["nom"]); sect = p["secteur"]; L = "ABC"
    def opt(name, code, label, inner, cls="", tagfn=None):
        if not form:
            return f'<div class="opt {cls}"><div class="tag"><i>{code}</i>{label}</div>{inner}</div>'
        return (f'<label class="opt pick {cls}"><input type="radio" name="{name}" value="{code}" required>'
                f'<div class="tag"><i>{code}</i>{label}<span class="chk">✓ Choisi</span></div>{inner}</label>')
    pals = ""
    for i, (key, c) in enumerate(list(t["palettes"].items())[:3]):
        inner = (f'<div class="pal"><div class="mini" style="background:{c["bg"]};color:{c["ink"]}"><b style="font-family:var(--h)">{nom}</b>'
                 f'<span style="font-size:.85rem">{E(p["metier"].capitalize())} à {E(p["ville"])}</span><br><br><u style="background:{c["acc"]}">{E(p.get("cta", "Demander un devis"))}</u></div>'
                 f'<div class="sw">' + "".join(f'<span style="background:{c[k]}"></span>' for k in ("bg", "soft", "acc", "acc2", "ink")) + '</div></div>')
        pals += opt("palette", L[i], f'Ambiance {E(PAL_LABELS.get(key, key))}', inner)
    sets = [("A", "Police du secteur (actuelle)", t["h"], t["b"])]
    for i, (k, fs) in enumerate(FONT_SETS.items()):
        sets.append((L[i + 1], fs["label"], fs["h"], fs["b"]))
    fonts = "".join(opt("police", c, E(lab), f'<div class="body"><div class="big" style="font-family:{h}">{nom}</div><div class="txt" style="font-family:{b}">{E(p["accroche"])}</div></div>', "fnt") for c, lab, h, b in sets)
    logos = ""
    for i, (k, lab) in enumerate(LOGOS.items(), 1):
        logos += opt("logo", str(i), E(lab), f'<div class="lgbox">{logo_link(p, k, "#")}</div><div class="lgbox dark">{logo_link(p, k, "#")}</div>')
    tones = "".join(opt("ton", L[i], E(lab), f'<div class="body"><q>{E(tx.format(nom=p["nom"], metier=p["metier"], Metier=p["metier"].capitalize(), ville=p["ville"]))}</q></div>', "tone") for i, (lab, tx) in enumerate(TONES))
    photos = "".join(opt("photos", c, E(a), f'<div class="body">{E(b)}</div>') for c, a, b in [
        ("A", "Vos photos", "Équipe, devanture, réalisations : vous nous envoyez 5 à 15 photos, nous les mettons en page."),
        ("B", "Visuels génériques", "Illustrations du métier, sans photo. Vous pourrez ajouter les vôtres plus tard."),
        ("C", "Un mélange", "Vos meilleures photos aux endroits clés, illustrations ailleurs.")])
    secs = COMMON_SECTIONS + EXTRA_SECTIONS.get(sect, [])
    if form:
        lst = "".join(f'<li><label class="cb"><input type="checkbox" name="sections[]" value="{E(a)}">{icon(i, 22)}<div><b>{E(a)}</b><small>{E(b)}</small></div></label></li>' for i, a, b in secs)
    else:
        lst = "".join(f'<li>{icon(i, 22)}<div><b>{E(a)}</b><small>{E(b)}</small></div></li>' for i, a, b in secs)
    return dict(pals=pals, fonts=fonts, logos=logos, tones=tones, photos=photos, lst=lst, nom=nom)

def build_choix(p, t, pal, has_pdf=False):
    P = _choix_parts(p, t, pal, False); nom = P["nom"]
    infos = ["Vos services à mettre en avant (4 à 6, une phrase chacun)", "Votre adresse, zone d’intervention, horaires", "Téléphone et e-mail à afficher",
             "Vos informations légales (forme juridique, SIRET, assurance, médiateur si vous vendez à des particuliers)", "Un site que vous aimez (facultatif)"]
    infl = "".join(f"<li>{E(x)}</li>" for x in infos)
    prix = ""
    if p.get("prix_install") and p.get("prix_abo"):
        prix = f'<p><b>{E(str(p["prix_install"]))} € une seule fois</b>, puis <b>{E(str(p["prix_abo"]))} €/mois</b>, sans engagement de durée.</p>'
    dl = '<a class="btn ghost dl" href="personnalisation.pdf">Télécharger cette brochure en PDF</a>' if has_pdf else ""
    contact = E(p.get("contact_agence", "artilien.contact@gmail.com"))
    body = f"""
<section class="ch-intro"><div class="wrap"><span class="kicker">Personnalisation</span><h1>Votre site, à l’image de {nom}</h1>
<p>Voici tout ce que nous pouvons ajuster. Rien n’est définitif : vous choisissez, nous modifions, et vous pouvez encore changer après la mise en ligne.</p>
<div class="ch-how"><b>Comment répondre ?</b> Par mail à {contact}, en donnant simplement vos codes. Exemple : « Couleurs B – Police A – Logo 3 – Ton C – Photos A ». Vous pouvez aussi écrire « je ne sais pas, conseillez-moi ».</div>{dl}</div></section>
<section class="ch-sec"><div class="wrap"><h2><span class="ch-num">1</span>Couleurs</h2><p class="sub">Trois ambiances pensées pour votre métier. La maquette utilise actuellement l’ambiance {E(PAL_LABELS.get(p.get("palette", t["defaut_palette"]), p.get("palette", t["defaut_palette"])))}.</p><div class="opts">{P["pals"]}</div></div></section>
<section class="ch-sec"><div class="wrap"><h2><span class="ch-num">2</span>Polices de caractères</h2><p class="sub">Le style des titres et des textes.</p><div class="opts">{P["fonts"]}</div></div></section>
<section class="ch-sec long"><div class="wrap"><h2><span class="ch-num">3</span>Logo</h2><p class="sub">Sept présentations de votre nom, sur fond clair et sur fond foncé. Si vous avez déjà un logo, envoyez-le : nous l’utiliserons à la place.</p><div class="opts">{P["logos"]}</div></div></section>
<section class="ch-sec"><div class="wrap"><h2><span class="ch-num">4</span>Ton des textes</h2><p class="sub">La façon dont le site parle de vous. Nous réécrivons tous les textes dans le ton choisi.</p><div class="opts">{P["tones"]}</div></div></section>
<section class="ch-sec"><div class="wrap"><h2><span class="ch-num">5</span>Photos</h2><div class="opts">{P["photos"]}</div></div></section>
<section class="ch-sec"><div class="wrap"><h2><span class="ch-num">6</span>Sections et fonctions en plus</h2><p class="sub">Dites-nous celles qui vous intéressent.</p><ul class="lst">{P["lst"]}</ul></div></section>
<section class="ch-sec"><div class="wrap"><h2><span class="ch-num">7</span>Ce que nous vous demanderons</h2><ul style="padding-left:20px;line-height:1.9">{infl}</ul></div></section>
<section class="ch-sec" style="padding-bottom:50px"><div class="wrap"><div class="incl"><b>Inclus dans l’offre</b>{prix}<ul><li>Création et mise en ligne de votre site (accueil, présentation, contact avec formulaire, mentions légales, politique de confidentialité)</li><li>Hébergement, nom de domaine et certificat de sécurité (HTTPS)</li><li>Une modification par mois sur simple mail</li><li>Vous restez propriétaire de vos contenus, résiliation par mail à tout moment</li></ul></div></div></section>"""
    return page_shell(p, t, pal, "Personnalisation", body, "", extra_families=["Playfair Display", "Source Sans 3", "Space Grotesk", "Inter"] + families_of(t["h"], t["b"]), extra_css=CHOIX_CSS)

COMMANDE_CSS = """
.pick{cursor:pointer;position:relative;transition:box-shadow .15s,border-color .15s}.pick input{position:absolute;opacity:0;pointer-events:none}
.pick .chk{display:none;margin-left:auto;font-size:.8rem;color:#fff;background:var(--acc);padding:2px 8px}
.pick:hover{box-shadow:0 8px 22px -14px rgba(0,0,0,.5)}
.pick:has(input:checked){border:2px solid var(--acc);box-shadow:0 0 0 3px color-mix(in srgb,var(--acc) 25%,transparent)}.pick:has(input:checked) .chk{display:inline-block}
.pick:has(input:focus-visible){outline:3px solid var(--acc);outline-offset:2px}
.cb{display:flex;gap:10px;align-items:flex-start;cursor:pointer;padding:8px 0;width:100%}.cb input{width:auto;margin-top:5px;accent-color:var(--acc);flex:none}
.fm{display:grid;gap:16px;max-width:760px}.fm label.l{font-weight:600;font-size:.95rem;display:block;margin-bottom:6px}.fm small.h{display:block;opacity:.7;font-weight:400}
.fm input[type=text],.fm input[type=email],.fm input[type=tel],.fm textarea{background:#fff;color:#1d2430;border:1.5px solid #8b93a1}
.doms{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:10px}.dom{overflow-wrap:anywhere}
.dom{display:flex;align-items:center;gap:10px;background:#fff;color:#1d2430;border:1.5px solid #c9ced6;padding:12px 14px;cursor:pointer;font-weight:700;border-radius:4px}
.dom input{width:auto;accent-color:var(--acc)}.dom:has(input:checked){border-color:var(--acc);box-shadow:0 0 0 3px color-mix(in srgb,var(--acc) 25%,transparent)}
.panel{background:var(--soft);padding:26px;border:1px solid color-mix(in srgb,var(--ink) 14%,transparent);max-width:760px}
.msg{padding:14px 16px;font-weight:600;margin-top:14px;display:none}.msg.ok{display:block;background:#e3f4e7;color:#14532d;border:1px solid #86c99a}.msg.err{display:block;background:#fde8e8;color:#7f1d1d;border:1px solid #e49a9a}
#paiement{display:none}#checkout{min-height:300px;margin-top:14px;background:#fff;border-radius:6px;padding:6px}
.price{display:flex;flex-wrap:wrap;gap:14px;margin:12px 0 4px}.price div{background:var(--bg);border:1px solid color-mix(in srgb,var(--ink) 18%,transparent);padding:14px 18px;flex:1;min-width:200px;color:var(--ink)}.price b{display:block;font-family:var(--h);font-size:1.9rem;line-height:1.1}
.steps2{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0 0;padding:0;list-style:none}.steps2 li{background:var(--dark);color:#f4f1ea;padding:8px 14px;font-size:.92rem}
"""

def build_commande(p, t, pal):
    P = _choix_parts(p, t, pal, True); nom = P["nom"]
    pi, pa = p.get("prix_install", 190), p.get("prix_abo", 29)
    ref = ""
    js = """
<script>
(function(){
 var q=new URLSearchParams(location.search), ref=(q.get('r')||'').replace(/[^A-Za-z0-9_-]/g,'').slice(0,40);
 var slug=location.pathname.split('/').filter(Boolean).slice(-2,-1)[0]||'';
 var t0=Math.floor(Date.now()/1000);
 var doms=(q.get('d')||'').split(',').map(function(x){return x.trim().toLowerCase()}).filter(function(x){return /^[a-z0-9.-]+\\.[a-z]{2,}$/.test(x)}).slice(0,15);
 var box=document.getElementById('doms');
 doms.forEach(function(d){var l=document.createElement('label');l.className='dom';var i=document.createElement('input');i.type='radio';i.name='domaine';i.value=d;l.appendChild(i);l.appendChild(document.createTextNode(d));box.insertBefore(l,box.lastElementChild)});
 if(!doms.length){document.getElementById('domnote').textContent='Indiquez le nom de domaine souhaité ci-dessous : nous vérifions sa disponibilité avant de continuer.'}
 var f=document.getElementById('fm'), msg=document.getElementById('msg'), btn=document.getElementById('send');
 f.addEventListener('submit',function(e){e.preventDefault();
  var fd=new FormData(f);fd.append('slug',slug);fd.append('ref',ref);fd.append('t0',t0);fd.append('commerce',document.body.getAttribute('data-nom')||'');
  btn.disabled=true;btn.textContent='Envoi en cours…';msg.className='msg';
  fetch('/api/choix.php',{method:'POST',body:fd}).then(function(r){return r.json()}).then(function(j){
   if(j.ok){msg.className='msg ok';msg.textContent='Merci, vos choix sont enregistrés. Vous pouvez maintenant régler pour lancer la mise en ligne.';
     document.getElementById('paiement').style.display='block';document.getElementById('paiement').scrollIntoView({behavior:'smooth'});btn.textContent='Choix enregistrés ✓';
     try{sessionStorage.setItem('email',fd.get('email'))}catch(x){}}
   else{btn.disabled=false;btn.textContent='Enregistrer mes choix';msg.className='msg err';msg.textContent=({email_invalide:'Merci de vérifier votre adresse e-mail.',consentement:'Merci de cocher la case de consentement.',trop_rapide:'Un instant, puis réessayez.',trop_de_demandes:'Trop de tentatives, réessayez plus tard.'})[j.error]||'Un problème est survenu : écrivez-nous à artilien.contact@gmail.com.'}
  }).catch(function(){btn.disabled=false;btn.textContent='Enregistrer mes choix';msg.className='msg err';msg.textContent='Connexion impossible : écrivez-nous à artilien.contact@gmail.com.'})});
 var pay=document.getElementById('paybtn'), started=false;
 pay.addEventListener('click',function(){ if(started)return; started=true; pay.disabled=true; pay.textContent='Chargement du paiement sécurisé…';
  var s=document.createElement('script');s.src='https://js.stripe.com/v3/';s.onload=function(){
   var em='';try{em=sessionStorage.getItem('email')||''}catch(x){}
   fetch('/api/checkout.php',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({slug:slug,ref:ref,email:em})}).then(function(r){return r.json()}).then(function(j){
    if(!j.ok){throw new Error(j.error||'x')}
    var stripe=Stripe(j.publishableKey,{locale:'fr'});
    return stripe.initEmbeddedCheckout({fetchClientSecret:function(){return Promise.resolve(j.clientSecret)}}).then(function(c){c.mount('#checkout');pay.style.display='none'})
   }).catch(function(){started=false;pay.disabled=false;pay.textContent='Payer en ligne';var m=document.getElementById('paymsg');m.className='msg err';m.textContent='Le paiement en ligne est momentanément indisponible. Écrivez-nous à artilien.contact@gmail.com et nous vous envoyons un lien de paiement.'})};
  s.onerror=function(){started=false;pay.disabled=false;pay.textContent='Payer en ligne'};document.head.appendChild(s)});
})();
</script>"""
    body = f"""<div data-nom-holder></div>
<section class="ch-intro"><div class="wrap"><span class="kicker">Votre site, en 3 étapes</span><h1>Choisissez, validez, payez : c’est en ligne</h1>
<p>Tout se fait ici, en quelques minutes. Rien n’est définitif : nous pouvons encore modifier après la mise en ligne.</p>
<ul class="steps2"><li>1 · Vos choix</li><li>2 · Votre adresse web</li><li>3 · Paiement sécurisé</li></ul></div></section>
<form id="fm" class="fm-all" novalidate onsubmit="return false">
<section class="ch-sec"><div class="wrap"><h2><span class="ch-num">1</span>Couleurs</h2><div class="opts">{P["pals"]}</div></div></section>
<section class="ch-sec"><div class="wrap"><h2><span class="ch-num">2</span>Polices de caractères</h2><div class="opts">{P["fonts"]}</div></div></section>
<section class="ch-sec long"><div class="wrap"><h2><span class="ch-num">3</span>Logo</h2><p class="sub">Vous avez déjà un logo ? Choisissez une présentation, puis répondez à notre mail avec votre fichier : nous l’utiliserons à la place.</p><div class="opts">{P["logos"]}</div></div></section>
<section class="ch-sec"><div class="wrap"><h2><span class="ch-num">4</span>Ton des textes</h2><div class="opts">{P["tones"]}</div></div></section>
<section class="ch-sec"><div class="wrap"><h2><span class="ch-num">5</span>Photos</h2><div class="opts">{P["photos"]}</div></div></section>
<section class="ch-sec"><div class="wrap"><h2><span class="ch-num">6</span>Sections et fonctions en plus</h2><p class="sub">Cochez celles qui vous intéressent (facultatif).</p><ul class="lst">{P["lst"]}</ul></div></section>
<section class="ch-sec"><div class="wrap"><h2><span class="ch-num">7</span>Votre adresse web</h2><p class="sub" id="domnote">Choisissez le nom de domaine de votre site. Tous ceux-ci étaient disponibles à l’envoi de notre mail.</p>
<div class="doms" id="doms"><label class="dom"><input type="radio" name="domaine" value="__autre"><span style="white-space:nowrap">Autre :</span><input type="text" name="domaine_autre" placeholder="monsite.fr" style="border:0;border-bottom:1.5px solid #8b93a1;padding:4px;width:100%;min-width:0"></label></div></div></section>
<section class="ch-sec"><div class="wrap"><h2><span class="ch-num">8</span>Vos informations</h2><div class="fm">
<div><label class="l" for="email">Votre e-mail *</label><input id="email" name="email" type="email" required autocomplete="email"></div>
<div class="row2"><div><label class="l" for="contact">Votre nom (facultatif)</label><input id="contact" name="contact" type="text" autocomplete="name"></div><div><label class="l" for="tel_contact">Téléphone (facultatif)</label><input id="tel_contact" name="tel_contact" type="tel" autocomplete="tel"></div></div>
<div><label class="l" for="services">Vos services à mettre en avant <small class="h">4 à 6, avec une phrase chacun</small></label><textarea id="services" name="services" rows="4"></textarea></div>
<div><label class="l" for="zone">Adresse et zone d’intervention</label><textarea id="zone" name="zone" rows="2"></textarea></div>
<div class="row2"><div><label class="l" for="horaires">Horaires</label><textarea id="horaires" name="horaires" rows="2"></textarea></div><div><label class="l" for="affiche">E-mail et téléphone à afficher sur le site</label><textarea id="affiche" name="affiche" rows="2"></textarea></div></div>
<div><label class="l" for="legal">Informations légales <small class="h">forme juridique, SIRET, assurance, médiateur si vous vendez à des particuliers</small></label><textarea id="legal" name="legal" rows="3"></textarea></div>
<div><label class="l" for="site_aime">Un site que vous aimez (facultatif)</label><input id="site_aime" name="site_aime" type="text"></div>
<div><label class="l" for="remarques">Autre chose à nous dire ?</label><textarea id="remarques" name="remarques" rows="2"></textarea></div>
<div style="position:absolute;left:-9999px" aria-hidden="true"><label>Ne pas remplir<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
<label class="check"><input type="checkbox" name="consent" value="1" required><span>J’accepte que ces informations soient utilisées par Stanislas Roux EI pour créer mon site (elles ne sont pas partagées). <a href="politique-confidentialite.html" style="text-decoration:underline">En savoir plus</a></span></label>
<div><button class="btn" id="send" type="submit">Enregistrer mes choix</button><div id="msg" class="msg" role="status"></div></div>
</div></div></section></form>
<section class="ch-sec" id="paiement" style="padding-bottom:60px"><div class="wrap"><h2><span class="ch-num">9</span>Paiement sécurisé</h2>
<div class="panel"><b>Mise en ligne de votre site</b><div class="price"><div><b>{E(str(pi))} €</b>une seule fois, aujourd’hui<br>création et mise en ligne</div><div><b>{E(str(pa))} €/mois</b>hébergement, domaine, sécurité<br>une modification par mois, sans engagement</div></div>
<p style="font-size:.92rem;opacity:.85">Paiement par carte, traité par Stripe : nous ne voyons jamais vos données bancaires. Vous recevez une facture par e-mail. Résiliation à tout moment par simple mail.</p>
<button class="btn" id="paybtn" type="button">Payer en ligne</button><div id="paymsg" class="msg" role="status"></div><div id="checkout"></div></div></div></section>
<script>document.body.setAttribute('data-nom',{json.dumps(p["nom"], ensure_ascii=False)})</script>{js}"""
    return page_shell(p, t, pal, "Mon site", body, "", extra_families=["Playfair Display", "Source Sans 3", "Space Grotesk", "Inter"] + families_of(t["h"], t["b"]), extra_css=CHOIX_CSS + COMMANDE_CSS)

def build_merci(p, t, pal):
    body = """<section class="ch-intro" style="padding-bottom:60px"><div class="wrap"><span class="kicker">Paiement</span><h1 id="t">Vérification du paiement…</h1>
<p id="d">Un instant, nous confirmons votre paiement.</p></div></section>
<script>(function(){var id=new URLSearchParams(location.search).get('session_id')||'';
if(!id){document.getElementById('t').textContent='Aucun paiement à vérifier';document.getElementById('d').textContent='Écrivez-nous à artilien.contact@gmail.com si besoin.';return}
fetch('/api/statut.php?session_id='+encodeURIComponent(id)).then(function(r){return r.json()}).then(function(j){
 if(j.ok&&j.paid){document.getElementById('t').textContent='Merci, paiement reçu !';document.getElementById('d').textContent='Nous lançons la mise en ligne de votre site. Vous recevez un e-mail de confirmation et votre facture dans les prochaines heures. Pour toute question, répondez simplement à nos e-mails.'}
 else{document.getElementById('t').textContent='Paiement non confirmé';document.getElementById('d').textContent='Votre paiement n’a pas abouti ou est encore en cours. Vous pouvez réessayer depuis la page précédente, ou nous écrire à artilien.contact@gmail.com.'}
}).catch(function(){document.getElementById('t').textContent='Vérification impossible';document.getElementById('d').textContent='Écrivez-nous à artilien.contact@gmail.com : nous vérifions votre paiement.'})})();</script>"""
    return page_shell(p, t, pal, "Merci", body, "", extra_css=CHOIX_CSS)

CHROME = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")

def make_pdf(out):
    """Rend personnalisation.html en PDF (Chrome sans interface). Retourne True si réussi."""
    if not CHROME:
        return False
    pdf = out / "personnalisation.pdf"
    r = subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={pdf}", (out / "personnalisation.html").as_uri()], capture_output=True, timeout=120)
    return pdf.exists() and pdf.stat().st_size > 1000

def build_site(path):
    p = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    t = theme_for(p, THEMES[p["secteur"]])
    pal = t["palettes"][p.get("palette", t["defaut_palette"])]
    out = ROOT / "dist" / p["slug"]
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    USED_FONTS.clear()
    pages = {"index.html": build_home, "presentation.html": build_pres, "contact.html": build_contact,
             "mentions-legales.html": build_mentions, "politique-confidentialite.html": build_privacy}
    for name, fn in pages.items():
        (out / name).write_text(fn(p, t, pal), encoding="utf-8")
    (out / "personnalisation.html").write_text(build_choix(p, t, pal, has_pdf=bool(CHROME)), encoding="utf-8")
    (out / "commande.html").write_text(build_commande(p, t, pal), encoding="utf-8")
    (out / "merci.html").write_text(build_merci(p, t, pal), encoding="utf-8")
    (out / "fonts").mkdir()
    for fn in sorted(USED_FONTS):
        shutil.copy(FONTS_DIR / fn, out / "fonts" / fn)
    pdf_ok = make_pdf(out)
    if CHROME and not pdf_ok:
        (out / "personnalisation.html").write_text(build_choix(p, t, pal, has_pdf=False), encoding="utf-8")
    if p.get("maquette", True):
        (out / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    print("OK", out, "(PDF)" if pdf_ok else "(sans PDF)")

if __name__ == "__main__":
    files = sys.argv[1:] or sorted(str(f) for f in (ROOT / "clients").glob("*.json"))
    for f in files:
        build_site(f)
