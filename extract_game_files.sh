#!/bin/bash

if [ ! -f DepotDownloader ]; then
    wget https://github.com/SteamRE/DepotDownloader/releases/download/DepotDownloader_2.7.1/DepotDownloader-linux-x64.zip -O DepotDownloader-linux-x64.zip
    unzip -o DepotDownloader-linux-x64.zip DepotDownloader && rm DepotDownloader-linux-x64.zip
fi

if [ ! -f Decompiler ]; then
    wget https://github.com/ValveResourceFormat/ValveResourceFormat/releases/download/10.2/Decompiler-linux-x64.zip -O Decompiler-linux-x64.zip
    unzip -o Decompiler-linux-x64.zip && rm Decompiler-linux-x64.zip
fi

# Download Deadlock Game files
./DepotDownloader -app 1422450 -username "$STEAM_USERNAME" -password "$STEAM_PASSWORD"

mkdir -p depots/game
rsync -av --remove-source-files depots/*/*/game/* depots/game/
find depots/ -type d -empty -delete

# Extract chunked VPK files
for chunked_vpk_file in $(find depots -type f -name "*_dir.vpk"); do
    parent_dir=$(dirname "$chunked_vpk_file")

    echo "Extracting $(basename chunked_vpk_file)"
    # TODO: Decompile only required files
    ./Decompiler -i "$chunked_vpk_file" -d --threads 8 -o "$parent_dir"

    echo "Removing chunk files"
    rm "$parent_dir/$(basename "$chunked_vpk_file" | cut -c1-5)"*
done

# Extract Map-VPKs
maps_folder="depots/game/citadel/maps"
citadel_folder="depots/game/citadel"
for vpk_file in $(find "$maps_folder" -type f -name "*.vpk"); do
    echo "Extracting $(basename vpk_file)"
    # TODO: Decompile only required files
    ./Decompiler -i "$vpk_file" -d --threads 8 -o "$citadel_folder"

    echo "Removing VPK file"
    rm "$vpk_file"
done


# Extract non-chunked VPK files
for vpk_file in $(find depots -type f -name "*.vpk"); do
    parent_dir=$(dirname "$vpk_file")

    echo "Extracting $(basename vpk_file)"
    # TODO: Decompile only required files
    ./Decompiler -i "$vpk_file" -d --threads 8 -o "$parent_dir"

    echo "Removing VPK file"
    rm "$vpk_file"
done

# Extract Steam Info
mkdir -p res
cp "$citadel_folder"/steam.inf res/

# Extract vData files
mkdir -p vdata
cp "$citadel_folder"/scripts/abilities.vdata vdata/
cp "$citadel_folder"/scripts/heroes.vdata vdata/
cp "$citadel_folder"/scripts/generic_data.vdata vdata/

# Extract localization files
mkdir -p localization
cp -r "$citadel_folder"/resource/localization/citadel_gc/* localization/
cp -r "$citadel_folder"/resource/localization/citadel_heroes/* localization/

# Extract video files
mkdir -p videos
cp -r "$citadel_folder"/panorama/videos/hero_abilities videos/

# Extract css files
cp "$citadel_folder"/panorama/styles/objectives_map.css res/
cp "$citadel_folder"/panorama/styles/citadel_shared_colors.css res/

# Extract image files
mkdir -p images
cp -r "$citadel_folder"/panorama/images/heroes images/
cp "$citadel_folder"/panorama/images/hud/hero_portraits/* images/heroes/

mkdir -p images/abilities
cp -r "$citadel_folder"/panorama/images/hud/abilities images/
cp -r "$citadel_folder"/panorama/images/upgrades images/

mkdir -p images/maps
cp -r "$citadel_folder"/panorama/images/minimap/base/* images/maps/
