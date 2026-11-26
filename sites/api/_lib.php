<?php
// Bibliothèque commune des endpoints (formulaire de choix, paiement Stripe intégré).
// AUCUN secret ici : la configuration (clés Stripe) est dans un fichier HORS du dossier web :
//   <dossier du domaine>/artilien-config.php  (voir sites/api/README.md)
declare(strict_types=1);
header('X-Content-Type-Options: nosniff');

function root_dir(): string { return dirname($_SERVER['DOCUMENT_ROOT']); }

function cfg(): array {
    static $c = null;
    if ($c !== null) return $c;
    $f = root_dir() . '/artilien-config.php';
    $c = [];
    if (is_file($f)) { ob_start(); $r = include $f; ob_end_clean(); $c = is_array($r) ? $r : []; }
    return $c;
}

function out(array $data, int $code = 200): void {
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    echo json_encode($data, JSON_UNESCAPED_UNICODE);
    exit;
}

function data_dir(): string {
    $d = root_dir() . '/artilien-data';
    if (!is_dir($d)) @mkdir($d, 0750, true);
    return $d;
}

function clean(?string $s, int $max = 2000): string {
    $s = (string)$s;
    $s = str_replace("\0", '', $s);
    $s = strip_tags($s);
    return mb_substr(trim($s), 0, $max);
}
function clean_line(?string $s, int $max = 200): string { return preg_replace('/[\r\n]+/', ' ', clean($s, $max)); }

function valid_slug(string $slug): bool {
    return (bool)preg_match('/^[a-z0-9][a-z0-9-]{1,80}$/', $slug) && is_dir($_SERVER['DOCUMENT_ROOT'] . '/m/' . $slug);
}
function valid_ref(string $ref): bool { return $ref === '' || (bool)preg_match('/^[A-Za-z0-9_-]{1,40}$/', $ref); }

// limite simple par IP : $max requêtes par heure pour l'action $name
function rate_limit(string $name, int $max): void {
    $ip = $_SERVER['REMOTE_ADDR'] ?? '0';
    $f = data_dir() . '/rl-' . $name . '-' . md5($ip) . '.json';
    $now = time(); $hits = [];
    if (is_file($f)) $hits = array_filter((array)json_decode((string)file_get_contents($f), true), fn($t) => $t > $now - 3600);
    if (count($hits) >= $max) out(['ok' => false, 'error' => 'trop_de_demandes'], 429);
    $hits[] = $now;
    @file_put_contents($f, json_encode(array_values($hits)), LOCK_EX);
}

function send_mail(string $to, string $subject, string $body, string $replyTo = ''): bool {
    $c = cfg();
    $from = $c['mail_from'] ?? 'no-reply@' . ($_SERVER['HTTP_HOST'] ?? 'artilien.com');
    $h = "From: Sites ArtiLien <$from>\r\nMIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\n";
    if ($replyTo !== '' && filter_var($replyTo, FILTER_VALIDATE_EMAIL)) $h .= "Reply-To: $replyTo\r\n";
    $subject = '=?UTF-8?B?' . base64_encode(preg_replace('/[\r\n]+/', ' ', $subject)) . '?=';
    return @mail($to, $subject, $body, $h);
}

function stripe_call(string $method, string $path, array $params = []): array {
    $c = cfg();
    $key = $c['stripe_secret'] ?? '';
    if ($key === '') out(['ok' => false, 'error' => 'config_stripe_manquante'], 500);
    $ch = curl_init('https://api.stripe.com/v1/' . $path);
    $opts = [CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 25, CURLOPT_USERPWD => $key . ':',
             CURLOPT_HTTPHEADER => ['Stripe-Version: 2024-06-20']];
    if ($method === 'POST') { $opts[CURLOPT_POST] = true; $opts[CURLOPT_POSTFIELDS] = http_build_query($params); }
    curl_setopt_array($ch, $opts);
    $res = curl_exec($ch);
    $code = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    $j = is_string($res) ? (json_decode($res, true) ?: []) : [];
    if ($code >= 400) { error_log('stripe ' . $code . ' ' . ($j['error']['message'] ?? '')); out(['ok' => false, 'error' => 'stripe', 'detail' => $j['error']['message'] ?? ''], 502); }
    return $j;
}
