# Deadlock Static Assets API

A static API containing most of the in-game items, assets and more from the game Deadlock.

**Documentation:** [https://deadlock.manuel-hexe.de/docs](https://deadlock.manuel-hexe.de/docs)

## Extract Data from Game Files

```bash
export STEAM_USERNAME=your_steam_username
export STEAM_PASSWORD=your_steam_password

bash extract_game_files.sh

python3 -m deadlock_assets_api.parse_game_data
```

### This runs the following steps:

1. Download DepotDownloader and Decompiler from GitHub-Releases
2. Download the newest Depot from Steam
3. Decompile all VPK files
4. Extract out the data we need
5. Parse the data into a JSON file
