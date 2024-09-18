# Deadlock Static Assets API

![Uptime](https://status.manuel-hexe.de/api/badge/27/uptime/810?label=Uptime%20%2830%20days%29)
![Build](https://github.com/raimannma/deadlock-assets-api/actions/workflows/docker-image.yaml/badge.svg)

A static API containing most of the in-game items, assets and more from the game Deadlock.

**Documentation:** [https://deadlock.manuel-hexe.de/docs](https://deadlock.manuel-hexe.de/docs)

## Extract Data from Game Files

```bash
# Extract Game Files
STEAM_USERNAME=your_steam_username STEAM_PASSWORD=your_steam_password ./extract_game_files.sh
# Parse Game Data
python3 -m deadlock_assets_api.parse_game_data
```

### This runs the following steps:

1. Download DepotDownloader and Decompiler from GitHub-Releases
2. Download the newest Depot from Steam
3. Decompile all VPK files
4. Extract out the data we need
5. Parse the data into a JSON file
