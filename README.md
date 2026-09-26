# metabase-jev

## Français

CLI qui enrichit une question sauvegardée de décisions Jev.

Définissez les deux clés et exécutez le CLI sur une question sauvegardée. Il produit du JSONL et limite les résultats à 100 lignes.

## English

CLI enriching a saved question with Jev decisions.

Set `METABASE_API_KEY` and `JEV_API_KEY`; run `python metabase_jev.py --url https://metabase.example --card-id 7 --field review --question "Does this review recommend the movie?"`. The JSONL output contains `jev_route`, `jev_probability`, and a state digest. Results above 100 rows fail by default. It is an API companion, not an in-app Metabase plugin.

## Español

CLI que amplía una pregunta guardada con decisiones Jev.

Defina ambas claves y ejecute el CLI sobre una pregunta guardada. Produce JSONL y limita los resultados a 100 filas.

## Contract / Contrat / Contrato

`yes`, `no`, `review`, `failure`; threshold default `0.8`. `review` is a real undecided state. Empty or oversized input becomes `review`; transport or invalid-response errors become `failure`. The shared client caps input at 32 KiB, response at 100 KiB, timeout at 10 s and calls at 10,000 per process; YAML templates enforce their own input and response bounds. No raw input is logged by this project. User data goes to the TypeSafe Jev API.

FR : `review` exige une revue humaine ; `failure` signale une erreur. Le contenu est envoyé à l’API TypeSafe Jev.

ES: `review` requiere revisión humana; `failure` indica un error. El contenido se envía a la API TypeSafe Jev.

## TLS / TLS / TLS

FR : si votre installation Python ne trouve pas les certificats racines, définissez `SSL_CERT_FILE` vers un bundle CA valide (par exemple `certifi.where()`). Ne désactivez pas la vérification TLS.

EN: if Python cannot find root certificates, set `SSL_CERT_FILE` to a valid CA bundle (for example `certifi.where()`). Keep TLS verification enabled.

ES: si Python no encuentra los certificados raíz, defina `SSL_CERT_FILE` con un paquete CA válido (por ejemplo `certifi.where()`). Mantenga activa la verificación TLS.

## Development / Développement / Desarrollo

`python -m unittest discover -p "test_*.py" -v`

Platform / Plateforme / Plataforma: [Metabase documentation](https://www.metabase.com/docs/latest/people-and-groups/api-keys).

MIT license. Community project; not an official Metabase integration.
