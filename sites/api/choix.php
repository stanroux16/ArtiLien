<?php
// Reçoit le formulaire de choix d'un client : un e-mail structuré part vers l'adresse de l'agence.
require __DIR__ . '/_lib.php';
if ($_SERVER['REQUEST_METHOD'] !== 'POST') out(['ok' => false, 'error' => 'methode'], 405);
rate_limit('choix', 12);
$in = $_POST;
if (clean_line($in['website'] ?? '') !== '') out(['ok' => true]);            // pot de miel : robot
if (time() - (int)($in['t0'] ?? 0) < 8) out(['ok' => false, 'error' => 'trop_rapide'], 400);
$slug = clean_line($in['slug'] ?? '', 90); $ref = clean_line($in['ref'] ?? '', 40);
if (!valid_slug($slug) || !valid_ref($ref)) out(['ok' => false, 'error' => 'maquette_inconnue'], 400);
$email = clean_line($in['email'] ?? '', 150);
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) out(['ok' => false, 'error' => 'email_invalide'], 400);
if (($in['consent'] ?? '') !== '1') out(['ok' => false, 'error' => 'consentement'], 400);

$labels = [
  'commerce' => 'Commerce', 'contact' => 'Nom du contact', 'tel_contact' => 'Téléphone du contact',
  'palette' => 'Couleurs', 'police' => 'Police', 'logo' => 'Logo', 'ton' => 'Ton des textes', 'photos' => 'Photos',
  'domaine' => 'Domaine choisi', 'domaine_autre' => 'Domaine proposé par le client',
  'services' => 'Services à mettre en avant', 'zone' => 'Adresse et zone', 'horaires' => 'Horaires',
  'affiche' => 'E-mail et téléphone à afficher', 'legal' => 'Informations légales', 'site_aime' => 'Site qu\'il aime', 'remarques' => 'Remarques',
];
$body = "Choix reçus depuis le formulaire du site.\n\nMaquette : https://" . ($_SERVER['HTTP_HOST'] ?? 'artilien.com') . "/m/$slug/\nRéférence prospect : " . ($ref ?: 'inconnue') . "\nE-mail du client : $email\n\n";
$codes = [];
foreach ($labels as $k => $lab) {
    $v = clean($in[$k] ?? '', $k === 'services' || $k === 'remarques' || $k === 'legal' ? 2500 : 300);
    if ($v !== '') { $body .= "$lab : $v\n"; if (in_array($k, ['palette','police','logo','ton','photos'], true)) $codes[] = "$lab $v"; }
}
$sec = $in['sections'] ?? [];
if (is_array($sec) && $sec) { $body .= "Sections en plus : " . implode(' ; ', array_map(fn($x) => clean_line((string)$x, 80), array_slice($sec, 0, 20))) . "\n"; }
if ($codes) $body .= "\nRésumé : " . implode(' – ', $codes) . "\n";
$to = cfg()['notify_email'] ?? 'artilien.contact@gmail.com';
$subj = 'Choix reçus – ' . clean_line($in['commerce'] ?? $slug, 80) . ' – ' . ($ref ?: $slug);
if (!send_mail($to, $subj, $body, $email)) out(['ok' => false, 'error' => 'envoi'], 500);
// accusé de réception au client
send_mail($email, 'Nous avons bien reçu vos choix', "Bonjour,\n\nMerci, nous avons bien reçu vos choix pour votre site. Nous préparons la nouvelle version de votre maquette et vous écrivons rapidement.\n\nVous pouvez répondre à ce mail pour toute précision.\n\nBelle journée,\nStanislas Roux\nSites internet pour artisans et commerçants\n\n--\nStanislas Roux EI - SIREN 133060277 - SIRET 13306027700018. Vos informations ne servent qu'à créer votre site.", $to);
out(['ok' => true]);
