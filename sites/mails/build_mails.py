#!/usr/bin/env python3
"""Génère les modèles d'e-mails HTML (prospection, relance, après « OK ») : lisibles en thème clair ET sombre.
Règles : fond ET couleur de texte explicites sur chaque cellule (aucun texte blanc sur fond non défini),
attribut bgcolor (Outlook), bouton « bulletproof » en tableau, bloc @media (prefers-color-scheme: dark) pour les clients qui le gèrent.
Sortie : prospection.html, relance.html, apres-ok.html (placeholders {COMMERCE}, {COULEUR}, {URL}, …)."""
import pathlib
OUT = pathlib.Path(__file__).parent
FONT = "font-family:Arial,Helvetica,sans-serif"
HEAD = """<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark"><meta name="supported-color-schemes" content="light dark"><title>{COMMERCE}</title><style>:root{color-scheme:light dark;supported-color-schemes:light dark}a{text-decoration:none}@media (prefers-color-scheme:dark){.bg-out{background-color:#14171d!important}.bg-card{background-color:#1e232c!important}.bg-soft{background-color:#2a313e!important}.tx{color:#f1f3f7!important}.tx-mute{color:#b9c0cd!important}.chip{background-color:#2a313e!important;border-color:#55607a!important;color:#ffffff!important}.bd{border-color:#3b4455!important}.step{background-color:#f1f3f7!important;color:#1d2430!important}}@media only screen and (max-width:620px){.w{width:100%!important}.pad{padding-left:20px!important;padding-right:20px!important}.h1{font-size:25px!important}}</style></head>"""
TAIL = "</body></html>"

def wrap(preheader, inner):
    return (HEAD + f'<body class="bg-out" bgcolor="#f3f1ec" style="margin:0;padding:0;background-color:#f3f1ec">'
            f'<div style="display:none;max-height:0;overflow:hidden;opacity:0;font-size:1px;line-height:1px;color:#f3f1ec">{preheader}</div>'
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" class="bg-out" bgcolor="#f3f1ec" style="background-color:#f3f1ec"><tr><td align="center" style="padding:24px 10px">'
            f'<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" class="w bg-card" bgcolor="#ffffff" style="width:600px;max-width:100%;background-color:#ffffff;border-radius:12px;overflow:hidden">'
            + inner + '</table></td></tr></table>' + TAIL)

def band(kicker, title):
    return (f'<tr><td bgcolor="{{COULEUR}}" class="pad" style="background-color:{{COULEUR}};padding:30px 32px 26px;{FONT};color:#ffffff">'
            f'<div style="{FONT};font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#ffffff">{kicker}</div>'
            f'<div class="h1" style="{FONT};font-size:29px;line-height:1.2;font-weight:700;color:#ffffff;margin-top:10px">{title}</div></td></tr>')

def para(html, top=22, bottom=6):
    return (f'<tr><td class="pad bg-card tx" bgcolor="#ffffff" style="background-color:#ffffff;padding:{top}px 32px {bottom}px;{FONT};font-size:16px;line-height:1.6;color:#1d2430">{html}</td></tr>')

def button(label, url, primary=True, top=14, bottom=8):
    if primary:
        return (f'<tr><td align="center" class="bg-card" bgcolor="#ffffff" style="background-color:#ffffff;padding:{top}px 32px {bottom}px">'
                f'<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" bgcolor="{{COULEUR}}" style="background-color:{{COULEUR}};border-radius:9px">'
                f'<a href="{url}" style="display:inline-block;padding:17px 36px;{FONT};font-size:18px;font-weight:700;color:#ffffff;text-decoration:none;border-radius:9px">{label}</a></td></tr></table></td></tr>')
    return (f'<tr><td align="center" class="bg-card" bgcolor="#ffffff" style="background-color:#ffffff;padding:{top}px 32px {bottom}px">'
            f'<a href="{url}" class="tx" style="{FONT};font-size:15px;font-weight:700;color:{{COULEUR}};text-decoration:underline">{label}</a></td></tr>')

def checks(items):
    rows = "".join(f'<tr><td width="28" valign="top" class="bg-card" bgcolor="#ffffff" style="background-color:#ffffff;padding:5px 0;{FONT};font-size:17px;font-weight:700;color:{{COULEUR}}">✓</td>'
                   f'<td class="bg-card tx" bgcolor="#ffffff" style="background-color:#ffffff;padding:5px 0;{FONT};font-size:16px;line-height:1.5;color:#1d2430">{i}</td></tr>' for i in items)
    return f'<tr><td class="pad bg-card" bgcolor="#ffffff" style="background-color:#ffffff;padding:8px 32px 4px"><table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">{rows}</table></td></tr>'

def box(html):
    return (f'<tr><td class="pad bg-card" bgcolor="#ffffff" style="background-color:#ffffff;padding:16px 32px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>'
            f'<td class="bg-soft tx bd" bgcolor="#f3f1ec" style="background-color:#f3f1ec;border:1px solid #e0dccf;border-radius:10px;padding:18px 20px;{FONT};font-size:16px;line-height:1.55;color:#1d2430">{html}</td></tr></table></td></tr>')

def footer(extra=""):
    return (f'<tr><td class="pad bg-soft tx-mute" bgcolor="#f3f1ec" style="background-color:#f3f1ec;padding:16px 32px;{FONT};font-size:12px;line-height:1.55;color:#5b6270">{extra}'
            'Stanislas Roux EI – SIREN 133060277 – SIRET 13306027700018. {LIGNE_SOURCE}Répondez STOP pour ne plus être contacté.</td></tr>')

SIGN = ('Belle journée,<br><b>Stanislas Roux</b><br><span class="tx-mute" style="color:#5b6270">Sites internet pour artisans et commerçants</span>')

prospection = wrap("Votre maquette de site est en ligne, sans engagement.",
    band("Maquette gratuite · sans engagement", "{COMMERCE}, votre site est prêt à visiter")
    + para("Bonjour,<br><br>En cherchant {METIER} à {VILLE}, j'ai vu que {COMMERCE} n'a pas encore de site internet. J'ai préparé <b>votre maquette</b> : vos services, vos horaires, un formulaire de contact.")
    + button("Voir ma maquette", "{URL}", top=16, bottom=12)
    + checks(["Votre métier, vos services, vos horaires", "Un formulaire pour que vos clients vous écrivent", "Tout se modifie selon vos envies"])
    + box("<b>{PRIX} € une seule fois</b>, puis <b>{ABO} €/mois à partir du 2e mois</b> (1er mois offert) : hébergement, nom de domaine, sécurité et une modification par mois. Sans engagement de durée.")
    + para("Ça vous plaît ? Répondez simplement <b>« OK »</b> : je vous envoie un lien pour choisir couleurs, logo et textes, et une dizaine de noms de domaine disponibles.<br><br>" + SIGN, top=4, bottom=26)
    + footer().replace("{LIGNE_SOURCE}", "Vous recevez ce message car votre adresse est publiée {SOURCE}. "))

relance = wrap("Avez-vous vu la maquette de votre site ?",
    band("Petit rappel", "{COMMERCE}, avez-vous vu votre maquette ?")
    + para("Bonjour,<br><br>Je voulais simplement savoir si vous aviez pu voir la maquette de site préparée pour {COMMERCE}. Elle reste en ligne quelques jours.")
    + button("Revoir ma maquette", "{URL}", top=14, bottom=12)
    + para("Si elle vous plaît, répondez <b>« OK »</b>. Sinon, dites-le moi et je ne vous écris plus.<br><br>" + SIGN, top=8, bottom=26)
    + footer().replace("{LIGNE_SOURCE}", ""))

CHIP = ('<span class="chip" style="display:inline-block;margin:4px 6px 4px 0;padding:8px 13px;border:1px solid #c9ced6;border-radius:8px;background-color:#f6f7f9;color:#1d2430;'
        f'{FONT};font-size:15px;font-weight:700">DOMAINE</span>')
def step(n, t, d):
    return (f'<tr><td width="42" valign="top" class="bg-card" bgcolor="#ffffff" style="background-color:#ffffff;padding:7px 0"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td width="32" height="32" align="center" class="step" bgcolor="#1d2430" style="background-color:#1d2430;border-radius:16px;{FONT};font-size:15px;font-weight:700;color:#ffffff">{n}</td></tr></table></td>'
            f'<td class="bg-card tx" bgcolor="#ffffff" style="background-color:#ffffff;padding:7px 0;{FONT};font-size:16px;line-height:1.45;color:#1d2430"><b>{t}</b><br><span class="tx-mute" style="color:#5b6270;font-size:14px">{d}</span></td></tr>')
steps = ('<tr><td class="pad bg-card" bgcolor="#ffffff" style="background-color:#ffffff;padding:10px 32px 4px"><table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">'
         + step(1, "Choisissez votre style", "couleurs, polices, logo, ton des textes : 2 minutes")
         + step(2, "Choisissez votre adresse web", "ces noms de domaine sont disponibles")
         + step(3, "Réglez en ligne, c’est parti", "paiement sécurisé sur la même page, mise en ligne ensuite")
         + '</table></td></tr>')
apres_ok = wrap("Votre site est en route : choisissez votre style et votre adresse web.",
    band("Votre site est en route", "Merci {COMMERCE} ! Personnalisons votre site")
    + para("Bonjour,<br><br>Merci pour votre réponse, je suis ravi de préparer le site de <b>{COMMERCE}</b>. Tout se fait sur <b>une seule page</b> : vous choisissez, vous validez, vous réglez.")
    + button("Choisir mon style et valider", "{URL_FORM}", top=16, bottom=6)
    + button("Voir toutes les options en PDF", "{URL_PDF}", primary=False, top=6, bottom=10)
    + steps
    + para('<b>Votre adresse web</b> : ces noms de domaine étaient disponibles à l’envoi de ce mail.<br>{CHIPS}', top=18, bottom=2)
    + box("<b>{PRIX} € une seule fois</b> (création et mise en ligne), puis <b>{ABO} €/mois à partir du 2e mois</b> (1er mois offert) : hébergement, nom de domaine, sécurité et une modification par mois. Sans engagement, vous restez propriétaire de vos contenus.")
    + para("Une question, un doute ? Répondez simplement à ce mail.<br><br>" + SIGN, top=4, bottom=26)
    + footer().replace("{LIGNE_SOURCE}", ""))

for name, html in [("prospection", prospection), ("relance", relance), ("apres-ok", apres_ok)]:
    (OUT / f"{name}.html").write_text(html, encoding="utf-8")
    print(name, len(html))
(OUT / "chip.html").write_text(CHIP, encoding="utf-8")
