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

## Data Sources

| Data | Source | Coverage |
|------|--------|----------|
| Polling unit list (176,846) | [INEC IReV](https://github.com/Emeka-Onwuepe/Polling_Units_in_Nigeria) | All 37 states |
| GPS coordinates (95,154) | [mykeels/inec-polling-units](https://github.com/mykeels/inec-polling-units) | 54% of PUs |
| Ward centroids (8,809) | [temikeezy/nigeria-geojson-data](https://github.com/temikeezy/nigeria-geojson-data) | All wards |

Polling units without GPS coordinates are placed at their ward centroid with a small random offset. The coordinate source (GPS vs estimated) is shown when you tap a polling unit.

## How It Works

1. **Search** for your polling unit by name or INEC code
2. **Tap** it to see the full collation hierarchy
3. **Tap "Walk" or "Drive"** on any level to get Google Maps directions
4. **Tap "Locate Me"** to see your current position and distances

## #VoteNDC #OK2027

Find your PU. Plan your vote. Defend your mandate.
