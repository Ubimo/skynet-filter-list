# Skynet Custom Filter List

Bereinigte Kopie der Liste aus
[`jumpsmm7/GeneratedAdblock`](https://github.com/jumpsmm7/GeneratedAdblock).

## Dateien

- `filter.list`: operative Liste mit 40 am 22.07.2026 erfolgreich geprüften Quellen
- `generated/drb-ra-IPC2s-30day.ipv4`: SkyNet-kompatible Fassung des C2-CSV-Feeds
- `scripts/update_c2_feed.py`: reproduzierbare manuelle Aktualisierung der normalisierten C2-Liste
- `AUDIT.md`: Prüfergebnis mit Anzahl erkannter IP-/CIDR-Zeilen

## Verwendung mit Skynet

```sh
firewall banmalware https://raw.githubusercontent.com/Ubimo/skynet-filter-list/main/filter.list
```

Das Repository muss öffentlich sein, damit der Router die Raw-Datei ohne GitHub-Token abrufen kann.

## Bewusst nicht in `filter.list`

- `https://darklist.de/raw.php`: HTTP 200, aber aktuell ohne IP-Einträge
- `https://iplists.firehol.org/files/normshield_high_attack.ipset`: HTTP 200, aber leer und laut Header seit 19.04.2025 nicht aktualisiert
- `https://www.talosintelligence.com/documents/ip-blacklist`: HTTP 403 mit `Invoke-WebRequest` und `curl`

`https://voipbl.org/update` bleibt enthalten: Der Server meldet fälschlich `text/html`, liefert aber eine gültige Rohdatenliste mit 94.893 Netzblöcken.

## Normalisierter C2-Feed

Der Upstream-Feed
`https://raw.githubusercontent.com/drb-ra/C2IntelFeeds/master/feeds/IPC2s-30day.csv`
enthält Zeilen im Format `IP,Beschreibung`. SkyNet akzeptiert dagegen nur eine
IP/CIDR als erstes whitespace-getrenntes Feld. Deshalb verweist `filter.list` auf
die normalisierte Datei in `generated/`.

Manuelle Aktualisierung:

```sh
python scripts/update_c2_feed.py
```

## Abgleich mit ViktorJp/Skynet

Am 13.07.2026 wurde
[`ViktorJp/Skynet/filter.list`](https://github.com/ViktorJp/Skynet/blob/main/filter.list)
mit dieser Liste verglichen. Alle 33 Quellen waren erreichbar; 26 waren bereits enthalten.

Übernommen wurde `firehol_webserver.netset`. Nicht übernommen wurden vollständig oder weitgehend redundante Quellen, das seit 2019 unveränderte `maxmind_proxy_fraud.ipset` sowie zwei Listen, die das Blocking von Tor-Exit-Nodes auf praktisch das gesamte Tor-Netz erweitern würden. Details stehen in `AUDIT.md`.

## Pflege

Neue Quellen werden zeilenweise in `filter.list` ergänzt. Vor dem Einsatz prüfen:

1. HTTP 2xx ohne Authentifizierung
2. Antwort enthält mindestens eine SkyNet-kompatible IPv4-Adresse oder ein CIDR-Netz im ersten Feld
3. Keine Login-, Fehler- oder HTML-Seite
4. Quelle ist stabil und für automatisierte Abrufe vorgesehen
