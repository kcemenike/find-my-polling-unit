# Find My Polling Unit

Interactive map of all **176,846 polling units** in Nigeria with the full collation centre hierarchy, walking/driving directions, and offline support.

**Live:** [kcemenike.github.io/find-my-polling-unit](https://kcemenike.github.io/find-my-polling-unit/)

![VoteNDC](votendc.jpg)

## Features

- **176,846 polling units** plotted on Google Maps tiles with marker clustering
- **Collation hierarchy** — tap any polling unit to see its Ward, LGA, State, and National collation centres
- **Estimated distances** and travel times between each level
- **Get Directions** — walking or driving via Google Maps from your current location
- **Locate Me** — GPS-based location to find your nearest polling unit
- **Search** — find any polling unit, ward, LGA, or state by name or code
- **Mobile-first** — responsive design optimised for on-the-go use
- **Offline support** — installable as a PWA, works without internet after first load
- **Satellite view** — toggle between road and satellite map tiles

## Data Source

All data is scraped directly from **INEC's official CVR portal** ([cvr.inecnigeria.org](https://cvr.inecnigeria.org/pu)) — the single source of truth.

| Data | Coverage |
|------|----------|
| Polling units | 176,846 (all 37 states, 774 LGAs, 8,809 wards) |
| INEC GPS coordinates | 163,170 (92.3% of PUs) |
| Ward centroid estimates | 13,676 (7.7% where INEC returned no coordinates) |

The coordinate source (INEC GPS vs estimated) is shown when you tap a polling unit.

## How It Works

1. **Search** for your polling unit by name or INEC code
2. **Tap** it to see the full collation hierarchy
3. **Tap "Walk" or "Drive"** on any level to get Google Maps directions
4. **Tap "Locate Me"** to see your current position and distances

## #VoteNDC #OK2027

Find your PU. Plan your vote. Defend your mandate.
