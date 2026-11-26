<?php
// Vérifie un paiement au retour sur le site et prévient l'agence (une seule fois par session).
require __DIR__ . '/_lib.php';
rate_limit('statut', 60);
$id = clean_line($_GET['session_id'] ?? '', 120);
if (!preg_match('/^cs_(test|live)_[A-Za-z0-9]+$/', $id)) out(['ok' => false, 'error' => 'session'], 400);
$s = stripe_call('GET', 'checkout/sessions/' . $id);
$paid = ($s['status'] ?? '') === 'complete' && in_array($s['payment_status'] ?? '', ['paid', 'no_payment_required'], true);
if ($paid) {
    $mark = data_dir() . '/paid-' . $id . '.txt';
    if (!is_file($mark)) {
        $amount = number_format(((int)($s['amount_total'] ?? 0)) / 100, 2, ',', '') . ' €';
        $ref = $s['client_reference_id'] ?? ''; $slug = $s['metadata']['slug'] ?? '';
        $email = $s['customer_details']['email'] ?? ($s['customer_email'] ?? '');
        $body = "Paiement reçu en ligne.\n\nMontant payé aujourd'hui : $amount\nRéférence prospect (client_reference_id) : $ref\nMaquette : https://" . ($_SERVER['HTTP_HOST'] ?? 'artilien.com') . "/m/$slug/\nE-mail du client : $email\nSession Stripe : $id\nMode : " . (str_starts_with($id, 'cs_test_') ? 'TEST' : 'RÉEL') . "\n";
        $to = cfg()['notify_email'] ?? 'artilien.contact@gmail.com';
        if (send_mail($to, 'Paiement reçu – ' . $amount . ' – ' . ($ref ?: $slug) . (str_starts_with($id, 'cs_test_') ? ' (TEST)' : ''), $body, $email)) @file_put_contents($mark, date('c'));
    }
}
out(['ok' => true, 'status' => $s['status'] ?? '', 'paid' => $paid]);
