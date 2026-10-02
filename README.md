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

## Exemple hors ligne / Offline example / Ejemplo sin conexión

FR : lancez `python3 -m examples.route_matrix` pour voir les quatre routes sur des valeurs synthétiques. L'entrée vide part en `review` sans appel fournisseur. Aucun serveur de plateforme ni clé API n'est nécessaire.

EN: run `python3 -m examples.route_matrix` to see all four routes on synthetic values. Empty input goes to `review` without a provider call. No platform server or API key is needed.

ES: ejecute `python3 -m examples.route_matrix` para ver las cuatro rutas con valores sintéticos. La entrada vacía va a `review` sin llamar al proveedor. No hace falta un servidor de plataforma ni una clave API.

## Contract / Contrat / Contrato

FR : le seuil par défaut est `0.8`. Les routes sont `yes`, `no`, `review` et `failure`. Une entrée vide ou supérieure à 32 Kio donne `review` ; une erreur de transport ou de réponse donne `failure`. Le client limite les appels à 10 000 par processus, à 10 s par appel et à 100 Kio par réponse. Un cache LRU conserve au plus 1 024 verdicts valides par empreinte SHA-256 ; il ne conserve pas le texte brut. Les données sont envoyées à TypeSafe Jev.

EN: the default threshold is `0.8`. Routes are `yes`, `no`, `review`, and `failure`. Empty input or input over 32 KiB becomes `review`; transport or response errors become `failure`. The client caps calls at 10,000 per process, 10 seconds per call, and 100 KiB per response. An LRU cache keeps at most 1,024 valid verdicts by SHA-256 digest; it does not store raw text. Data is sent to TypeSafe Jev.

ES: el umbral predeterminado es `0.8`. Las rutas son `yes`, `no`, `review` y `failure`. Una entrada vacía o superior a 32 KiB produce `review`; los errores de transporte o respuesta producen `failure`. El cliente limita las llamadas a 10 000 por proceso, a 10 s por llamada y a 100 KiB por respuesta. Una caché LRU conserva como máximo 1 024 decisiones válidas por huella SHA-256; no almacena el texto original. Los datos se envían a TypeSafe Jev.

## Pipeline export / Export de pipeline / Exportación de pipeline

FR : `--output` écrit le JSONL dans un fichier temporaire puis le remplace une fois toutes les décisions obtenues. `--strict` arrête l’export si une ligne donne `no`, `review` ou `failure` et préserve l’ancien fichier. `--limit` borne les lignes (1 à 1 000) et la réponse Metabase est limitée à 5 Mo.

EN: `--output` writes JSONL to a temporary file and replaces the destination only after every decision completes. `--strict` aborts export on any `no`, `review`, or `failure` row and preserves the previous file. `--limit` bounds rows (1 to 1,000), and the Metabase response is capped at 5 MB.

ES: `--output` escribe JSONL en un archivo temporal y sustituye el destino solo cuando terminan todas las decisiones. `--strict` cancela la exportación si alguna fila es `no`, `review` o `failure`, y conserva el archivo anterior. `--limit` limita las filas (de 1 a 1 000) y la respuesta de Metabase se limita a 5 MB.

```sh
python metabase_jev.py --url https://metabase.example --card-id 7 --field review \
  --question 'Does the review recommend the movie?' --limit 100 --strict \
  --output classified.jsonl
```

FR : ajoutez aussi une limite de lignes dans la question sauvegardée Metabase : `--limit` protège cet outil après la réponse mais ne limite pas l’exécution côté Metabase.

EN: add a row limit to the saved Metabase question as well: `--limit` protects this tool after the response but does not constrain Metabase execution.

ES: añada también un límite de filas en la pregunta guardada de Metabase: `--limit` protege esta herramienta después de la respuesta, pero no limita la ejecución en Metabase.

## TLS / TLS / TLS

FR : si votre installation Python ne trouve pas les certificats racines, définissez `SSL_CERT_FILE` vers un bundle CA valide (par exemple `certifi.where()`). Ne désactivez pas la vérification TLS.

EN: if Python cannot find root certificates, set `SSL_CERT_FILE` to a valid CA bundle (for example `certifi.where()`). Keep TLS verification enabled.

ES: si Python no encuentra los certificados raíz, defina `SSL_CERT_FILE` con un paquete CA válido (por ejemplo `certifi.where()`). Mantenga activa la verificación TLS.

## Development / Développement / Desarrollo

`python -m unittest discover -p "test_*.py" -v`

Platform / Plateforme / Plataforma: [Metabase documentation](https://www.metabase.com/docs/latest/people-and-groups/api-keys).

MIT license. Community project; not an official Metabase integration.
