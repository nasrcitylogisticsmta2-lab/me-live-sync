name: Final Sync Action

on:
  workflow_dispatch:

jobs:
  sync-process:
    runs-on: ubuntu-latest
    steps:
      - name: 1. Fetch Code
        uses: actions/checkout@v3

      - name: 2. Install Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: 3. Install Requirements
        run: pip install requests gspread oauth2client

      - name: 4. Execute Sync Script
        env:
          GOOGLE_CREDS: ${{ secrets.GOOGLE_CREDS }}
          API_TOKEN: ${{ secrets.TOKEN }}
        run: python sync.py
