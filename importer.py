import os
import zipfile
import json
import shutil
import hashlib

def calculate_md5_and_size(file_path):
    md5_hash = hashlib.md5()
    file_size = 0

    with open(file_path, "rb") as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            md5_hash.update(byte_block)
            file_size += len(byte_block)

    return md5_hash.hexdigest(), file_size

def process_folder(folder_path):
    md5_checksum_dict = {}
    size_dict = {}

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(file_path, folder_path)
            
            md5_checksum, file_size = calculate_md5_and_size(file_path)
            
            md5_checksum_dict[relative_path.replace("\\", "/")] = md5_checksum
            size_dict[relative_path.replace("\\", "/")] = file_size

    return md5_checksum_dict, size_dict

def write_to_file(file_name, data):
    with open(file_name, "w") as file:
        file.write(json.dumps(data, separators=(',', ':')))

def get_unique_song_file(existing_songs, song_file):
    counter = 1
    unique_song_file = song_file
    while unique_song_file in existing_songs:
        unique_song_file = f"{song_file}{counter}"
        counter += 1
    return unique_song_file

def get_chart_list(dir, manifest):
    chart_6k = manifest.get("diff_6k").split('/')
    chart_4k = manifest.get("diff_4k").split('/')
    dir_list = []
    all_chart = chart_6k + chart_4k
    diff_table = ["_EL.bms", "_EX.bms", "_LPR.bms", "_PR.bms", "_EL4.bms", "_EX4.bms", "_PR4.bms"]
    for i in range(len(all_chart)):
        if all_chart[i] != "0":
            path = os.path.join(dir, "note", manifest.get("mp3") + diff_table[i])
            dir_list.append(path)
    return dir_list

def deleteChart(song_id):

    # Find the song manifest to remove.

    playmanifest_path = "OverRide/playmanifest.json"
    with open(playmanifest_path, 'r', encoding='utf-8') as f:
        playmanifest = json.load(f)

    manifest_to_remove = None
    for manifest in playmanifest:
        if manifest[0].get("id") == song_id:
            manifest_to_remove = manifest
            break

    # We now have the manifest to remove, which is aquired after looping through the main manifest.

    if manifest_to_remove is None:
        print("That song ID not found. 没有找到此歌曲ID。")
        return
    
    # Confirm with the user one last time by printing out some useful data.

    song_title = manifest_to_remove[0].get("title")
    diff_str = manifest_to_remove[0].get("diff_6k") + "/" + manifest_to_remove[0].get("diff_4k")
    charter = manifest_to_remove[0].get("charter_6k") + "/" + manifest_to_remove[0].get("charter_4k")
    print(f"Are you sure you want to delete the song '{song_title}', difficulty '{diff_str}', charted by '{charter}'?")
    print(f"你确定要删除这首歌吗？名为 '{song_title}'，难度 '{diff_str}'，谱师为 '{charter}'?")
    confirm = input("(y/n): ")
    if confirm.lower() != 'y':
        print("Deletion cancelled. 删除终止。")
        return

    song_name = manifest_to_remove[0].get("mp3")

    # Remove everything but the chart.

    paths_to_check = [
        (os.path.join("OverRide", "bga", f"{song_name}.zip"), False),
        (os.path.join("OverRide", "music", f"{song_name}.mp3"), False),
        (os.path.join("Resources", "data", f"{song_name}.jpg"), False),
        (os.path.join("Resources", "data", f"{song_name}.png"), False),
    ]

    for path, _ in paths_to_check:
        if os.path.exists(path):
            os.remove(path)

    # Remove charts

    charts = get_chart_list(os.path.join("OverRide"), manifest_to_remove[0])

    for chart in charts:
        print(chart)
        if os.path.exists(chart):
            os.remove(chart)

    # Remove the charts from the zip.

    note_zip_path = os.path.join("OverRide", "Note.zip")
    if os.path.exists(note_zip_path):
        temp_zip_path = os.path.join("OverRide", "temp_Note.zip")
        with zipfile.ZipFile(note_zip_path, 'r') as note_zip:
            with zipfile.ZipFile(temp_zip_path, 'w') as temp_zip:
                for item in note_zip.infolist():
                    check_name = "offlineNote2_" + song_name + "_"
                    file_name = item.filename
                    if not file_name.startswith(check_name):
                        # write file
                        temp_zip.writestr(item, note_zip.read(item.filename))

        os.remove(note_zip_path)
        os.rename(temp_zip_path, note_zip_path)

    # Remove the manifest, and refresh the metadata.

    playmanifest.remove(manifest_to_remove)
    with open(playmanifest_path, 'w', encoding='utf-8') as f:
        json.dump(playmanifest, f, indent=4)

    # Correct the main sync and metadata.
    update_metadata()
    print("Song has been deleted from the server. 歌曲已从服务器删除。")

def importChart(name):

    # Create a temp directory for unzipping the provided zip file.

    extract_to = "_temp"
    if os.path.exists(extract_to):
        shutil.rmtree(extract_to)
    os.makedirs(extract_to)

    if not os.path.isfile(name):
        print(f"Error: The file '{name}' does not exist.")
        return

    # Safely opens the zip file.

    try:
        with zipfile.ZipFile(name, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    except zipfile.BadZipFile:
        print(f"Error: '{name}' is not a valid zip file.")
        return
    except PermissionError:
        print(f"Error: Permission denied. Check your permissions for '{extract_to}'.")
        return
    except Exception as e:
        print(f"An unexpected error occurred when unzipping: {e}")
        return

    # Safely read the song manifest

    manifest_path = os.path.join(extract_to, "manifest.json")

    if not os.path.isfile(manifest_path):
        print(f"Error: The file '{manifest_path}' does not exist.")
        return
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    except Exception as e:
        print(f"JSON parse failed for manifest failed: {e}")
        return
    
    for song in manifest:
        song_file = song.get("mp3")

        # get list of charts

        charts = get_chart_list(extract_to, song)

            # Sanity check everything

        standard_check = True
        reason_fail = ""

        bga_data = song.get("bga")

        # New sanity check: 
        # (1): either the jpg and png version of the thumbnail should exist. 

        img1_path = os.path.join(os.path.join(extract_to, "thumbs"), f"{song_file}.jpg")
        img2_path = os.path.join(os.path.join(extract_to, "thumbs"), f"{song_file}.png")

        if os.path.exists(img1_path) == False and os.path.exists(img2_path) == False:
            standard_check = False
            reason_fail += "\nSong thumbnail (music_name.jpg or music_name.png) is missing from the thumbs folder. "

        # (2): The correct mp3 file should be there.

        song_path = os.path.join(os.path.join(extract_to, "music"), f"{song_file}.mp3")

        if os.path.exists(song_path) == False:
            standard_check = False
            reason_fail += "\nMusic file (music_name.mp3) is missing from the Music folder. "

        # (3): If bga data is present, bga file should be there.

        bga_path = os.path.join(os.path.join(extract_to, "bga"), f"{song_file}.zip")

        if bga_data != None and os.path.exists(bga_path) == False:
            standard_check = False
            reason_fail += "\nSince manifest specified BGA, there should be a music_name.zip in the bga folder. "

        # (4): If bga data is not present but there is a song_name.zip in bga folder.

        if bga_data == None and os.path.exists(bga_path):
            standard_check = False
            reason_fail += "\nManifest did not specify BGA, but there is a music_name.zip in the bga folder. While this is not a breaking issue, if you wish to use the BGA please specify it in the manifest. "

        # (5): All the charts specified in the manifest should exist

        for chart in charts:
            if os.path.exists(chart) == False:
                standard_check = False
                reason_fail += "\nA chart that is specified in manifest is missing from the note folder: " + chart + ". "

        # That is it!

        if standard_check == False:
            print("The song contains issues and is not imported. 此曲目存在问题，没有导入。")
            print("The reasons are as follows. 原因如下。")
            print(reason_fail)
            shutil.rmtree(extract_to)
            continue
        
        playmanifest_path = "OverRide/playmanifest.json"
        with open(playmanifest_path, 'r', encoding='utf-8') as f:
            playmanifest = json.load(f)
        
        existing_song_files = [item[0].get("mp3") for item in playmanifest]
        unique_song_file = get_unique_song_file(existing_song_files, song_file)

        # Copy bga zip file if bga is specified

        if bga_data != None:
            new_bga_name = unique_song_file + ".zip"
            new_bga_path = os.path.join("OverRide", "bga", new_bga_name)
            os.makedirs(os.path.dirname(new_bga_path), exist_ok=True)
            shutil.move(bga_path, new_bga_path)

        # Copy music file

        new_song_name = unique_song_file + ".mp3"
        new_song_path = os.path.join("OverRide", "music", new_song_name)
        os.makedirs(os.path.dirname(new_song_path), exist_ok=True)
        shutil.move(song_path, new_song_path)

        # Copy the thumbnails

        if os.path.exists(img1_path):
            img_path = img1_path
            append = ".jpg"
        else:
            img_path = img2_path
            append = ".png"

        new_img_name = unique_song_file + append
        new_img_path = os.path.join("Resources", "data", new_img_name)
        os.makedirs(os.path.dirname(new_img_path), exist_ok=True)
        shutil.move(img_path, new_img_path) 

        # Copy all the charts

        for chart in charts:
            new_chart_name = os.path.basename(chart)
            new_chart_name = new_chart_name.replace(song_file, unique_song_file)
            new_chart_path = os.path.join("OverRide", "note", new_chart_name)
            os.makedirs(os.path.dirname(new_chart_path), exist_ok=True)
            shutil.copy(chart, new_chart_path)

        # Add charts to zip

        note_zip_path = os.path.join("OverRide", "Note.zip")
        new_charts = []
        for chart in charts:
            new_chart_name = chart.replace(song_file, f"offlineNote2_{unique_song_file}")
            new_chart_name = new_chart_name.replace(".bms", "")
            os.rename(chart, new_chart_name)
            new_charts.append(new_chart_name)

        with zipfile.ZipFile(note_zip_path, 'a') as note_zip:
            for chart in new_charts:
                note_zip.write(chart, arcname=os.path.basename(chart))

        # Merge the manifest

        if playmanifest:
            last_id = playmanifest[-1][0].get("id", 0)
        else:
            last_id = 0

        song["id"] = last_id + 1
        song["mp3"] = unique_song_file

        playmanifest.append([song])
        with open(playmanifest_path, 'w', encoding='utf-8') as f:
            json.dump(playmanifest, f, indent=4)

        print(f"Song added: 歌曲已添加：{unique_song_file}")

    # Refresh the metadata and we are done!
    update_metadata()
    shutil.rmtree(extract_to)
        

def update_metadata():
    resources_folder = "Resources"
    
    md5_checksum_dict, size_dict = process_folder(resources_folder)
    
    md5_file_name = "OverRide/Md5ListChecksum.json"
    size_file_name = "OverRide/SizeList.json"
    
    write_to_file(md5_file_name, md5_checksum_dict)
    write_to_file(size_file_name, size_dict)

    print(f"MD5 and size checksums saved.")

def main():
    print("Override Concierge - 您的Override管家")
    print("For music import, simply enter the zip file's path. For music deletion, simply enter its SID as displayed in-game.")
    print("曲目导入请输入zip文件的目录。曲目删除请输入游戏内显示的SID。")
    user_input = input("Input 输入: ")

    if user_input.isdigit():
        deleteChart(int(user_input))
    elif not user_input.endswith(".zip"):
        print("The file is not zip. 文件不是zip。")
    else:
        importChart(user_input)

if __name__ == "__main__":
    main()