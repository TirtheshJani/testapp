# Phase 3 Placeholder Metrics

The "Client Satisfaction" percentage displayed on the dashboard is currently hard-coded. It is intended as a placeholder metric for demonstration purposes.

In a future phase the client may provide survey data or a formula for calculating this value dynamically. The implementation should be revisited when those requirements are clarified.

## Analytics page

The dashboard now includes a **📊 View Analytics** button linking to `/analytics`. This route displays a "Coming soon" message. Full reporting features are planned for Phase 5, so this button and page act as placeholders in Phase 3.

## Top Rankings

A `/api/rankings/top` endpoint returns five hard-coded athletes with an overall score. This serves as an interim data source until the multi-factor ranking system is developed in Phase 4.

## Media upload

A new **📁 Upload Media** option on the dashboard links to `/media/upload`. The page presents a simple form to pick an athlete and upload a file. This demonstrates the media workflow from Phase 2 without persisting large files during the demo.
