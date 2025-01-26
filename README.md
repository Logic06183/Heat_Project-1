# HE2AT Data Acquisition Dashboard

This repository contains the HE2AT Center's data acquisition progress dashboard, which visualizes the current status of data collection and processing across different sites.

## Overview

The dashboard displays:
- Overall data acquisition progress
- RP1 specific progress
- Johannesburg site progress
- Abidjan site progress

## Setup

1. Clone this repository
2. The dashboard is hosted using GitHub Pages and can be accessed at `https://[your-username].github.io/[repository-name]`

## Updating the Dashboard

The visualizations are updated monthly. To update:
1. Run the Python scripts to generate new visualizations
2. Place the new visualizations in the corresponding month's folder
3. Update the `index.html` file to point to the new visualizations

## Deployment
The interactive visualizations are available at:
- Johannesburg Progress: [Bar Chart](interactive_plots/johannesburg_bar.html) | [Donut Chart](interactive_plots/johannesburg_donut.html)
- RP1 Progress: [Bar Chart](interactive_plots/rp1_bar.html) | [Donut Chart](interactive_plots/rp1_donut.html)
- Abidjan Progress: [Bar Chart](interactive_plots/abidjan_bar.html) | [Donut Chart](interactive_plots/abidjan_donut.html)

Last updated: 2025-01-26

## File Structure

```
├── index.html              # Main dashboard page
├── styles.css             # Dashboard styling
├── README.md              # This file
└── Jan 2025/             # Monthly visualization folders
    ├── overall_progress.png
    ├── rp1_progress.png
    ├── johannesburg_progress.png
    └── abidjan_progress.png
```

## License

 2025 HE2AT Center. All rights reserved.
