<?php
// Crée une session Stripe Checkout « intégrée » (paiement dans la page) : installation (une fois) + abonnement mensuel.
require __DIR__ . '/_lib.php';
if ($_SERVER['REQUEST_METHOD'] !== 'POST') out(['ok' => false, 'error' => 'methode'], 405);
rate_limit('checkout', 15);
$in = json_decode((string)file_get_contents('php://input'), true) ?: [];
$slug = clean_line($in['slug'] ?? '', 90); $ref = clean_line($in['ref'] ?? '', 40);
if (!valid_slug($slug) || !valid_ref($ref)) out(['ok' => false, 'error' => 'maquette_inconnue'], 400);
$c = cfg();
if (empty($c['stripe_secret']) || empty($c['stripe_publishable'])) out(['ok' => false, 'error' => 'config_stripe_manquante'], 500);
$host = $_SERVER['HTTP_HOST'] ?? 'artilien.com';
$p = [
  'ui_mode' => 'embedded', 'mode' => 'subscription', 'locale' => 'fr', 'adaptive_pricing' => ['enabled' => 'false'],
  'return_url' => "https://$host/m/$slug/merci.html?session_id={CHECKOUT_SESSION_ID}",
  'line_items' => [
    ['quantity' => 1, 'price_data' => ['currency' => 'eur', 'unit_amount' => (int)($c['abo_cents'] ?? 2900), 'recurring' => ['interval' => 'month'],
       'product_data' => ['name' => 'Abonnement mensuel (1er mois offert) : hébergement, nom de domaine, sécurité, une modification par mois']]],
    ['quantity' => 1, 'price_data' => ['currency' => 'eur', 'unit_amount' => (int)($c['install_cents'] ?? 19000),
       'product_data' => ['name' => 'Création et mise en ligne de votre site internet (une seule fois)']]],
  ],
  'metadata' => ['slug' => $slug, 'ref' => $ref],
  'subscription_data' => ['trial_period_days' => 30, 'metadata' => ['slug' => $slug, 'ref' => $ref]],
];
if ($ref !== '') $p['client_reference_id'] = $ref;
$em = clean_line($in['email'] ?? '', 150);
if (filter_var($em, FILTER_VALIDATE_EMAIL)) $p['customer_email'] = $em;
$s = stripe_call('POST', 'checkout/sessions', $p);
out(['ok' => true, 'clientSecret' => $s['client_secret'] ?? '', 'publishableKey' => $c['stripe_publishable']]);
