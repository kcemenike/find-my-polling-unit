# Find My Polling Unit

Interactive map of all **176,846 polling units** in Nigeria with the full collation centre hierarchy, walking/driving directions, and offline support.

**Live:** [kcemenike.github.io/find-my-polling-unit](https://kcemenike.github.io/find-my-polling-unit/)

[![Watch the Demo](https://img.shields.io/badge/Watch_Demo-Launching_Oct_20-00a651?style=for-the-badge&logo=google-maps&logoColor=white)](https://kcemenike.github.io/find-my-polling-unit/)

> **Launching October 20, 2026.** Visit the [landing page](https://kcemenike.github.io/find-my-polling-unit/) to see the interactive demo and countdown. The full map is available at [/map.html](https://kcemenike.github.io/find-my-polling-unit/map.html).

## Features

- **176,846 polling units** plotted on Google Maps tiles with marker clustering
- **Collation hierarchy** — tap any polling unit to see its Ward, LGA, State, and National collation centres
- **Estimated distances** and travel times between each level
- **Get Directions** — walking or driving via Google Maps from your current location
- **Locate Me** — GPS-based location to find your nearest polling unit
- **Search** — find any polling unit, ward, LGA, or state by name or code
- **Mobile-first** — responsive bottom sheet with tap-to-toggle
- **Offline support** — installable as a PWA, works without internet after first load
- **Lazy loading** — FCT loads first (363KB), remaining states stream in background
- **Satellite view** — toggle between road and satellite map tiles

## Data Sources

Every location on the map is a real building — zero centroids or estimates.

| Data | Count | Source |
|------|-------|--------|
| Polling units | 176,846 | [INEC CVR portal](https://cvr.inecnigeria.org/pu) GPS coordinates |
| Ward collation centres | 8,809 | [INEC state-specific PDFs](https://inecnigeria.org/documents/resources/rac/) — actual INEC-designated buildings |
| LGA collation centres | 775 | [INEC CVR locator](https://cvr.inecnigeria.org/locator/browse) — INEC LGA office addresses |
| State collation centres | 37 | [INEC state offices](https://inecnigeria.org/about/state-offices) — INEC state HQ addresses |
| National collation centre | 1 | ICC Abuja |

## Raw INEC Data

The complete raw data from INEC is available in the [`inec_scraped/`](inec_scraped/) directory for anyone who wants to use it. This data is public and free to use.

### Structure

Each state has two files:

- `state_{id}_{name}.json` — full hierarchy (LGAs → wards → polling units)
- `state_{id}_{name}_coords.json` — GPS coordinates keyed by INEC polling unit ID

### Hierarchy file format

```json
{
  "id": "15",
  "name": "FCT",
  "lgas": [
    {
      "id": "276",
      "code": "01",
      "name": "ABAJI",
      "wards": [
        {
          "id": "3234",
          "code": "01",
          "name": "ABAJI CENTRAL",
          "pus": [
            {
              "id": "41840",
              "code": "001",
              "name": "UNG. MAIKANO/KOFAR MAI UNGUWA I"
            }
          ]
        }
      ]
    }
  ]
}
```

### Coordinates file format

```json
{
  "41840": { "lat": 8.4702, "lng": 6.9439 },
  "41841": { "lat": 8.4698, "lng": 6.9442 }
}
```

Keys are INEC's internal polling unit IDs (matching the `id` field in the hierarchy file). Coordinates with `null` values mean INEC did not return GPS data for that polling unit.

### Using the data

The `id` fields are INEC's internal database identifiers. You can use them to query INEC's CVR API:

- **LGAs for a state:** `GET https://cvr.inecnigeria.org/PublicApi/lgas/1/Search?data[Search][state_id]={state_id}`
- **Wards for an LGA:** `GET https://cvr.inecnigeria.org/PublicApi/wards/1/Search?data[Search][local_government_id]={lga_id}`
- **PUs for a ward:** `GET https://cvr.inecnigeria.org/PublicApi/pus/1/Search?data[Search][registration_area_id]={ward_id}`
- **Coordinates:** `POST https://cvr.inecnigeria.org/pu_locator/index` with form data `data[Search][state_id]`, `data[Search][local_government_id]`, `data[Search][registration_area_id]`, `data[Search][polling_unit_id]` — returns a redirect to Google Maps with `?q=lat,lng`

The scrape script (`inec_scraped/scrape_inec.py`) is included if you want to re-run or update the data.

## How It Works

1. **Search** for your polling unit by name or INEC code
2. **Tap** it to see the full collation hierarchy
3. **Tap "Walk" or "Drive"** on any level to get Google Maps directions
4. **Tap "Locate Me"** to see your current position and distances

## #VoteNDC #OK2027

Find your PU. Plan your vote. Defend your mandate.

[![Join SmartBallot](https://img.shields.io/badge/Join_SmartBallot-NDC-1a237e?style=for-the-badge)](https://smartballotapp.com/supergroup?code=NCZOG5PL-PCI6G75L)
