# OverRapid-Fanmade-Server

Awaiting Target Input..

## Introduction

A small local server for ```Project OverRide```, a fanmade fork of ```OverRapid```, implemented with ```Python``` and ```Flask```.

This fork was created specifically to play fanmade chart for ```OverRapid```.

This repo does not contain any copyright or trademark infringing content. Client package is not available on GitHub, and is provided on a per-request basis.

This server is not compatible with the official version. That version might be released in the future, depending on my mood...


## 简介

一个适用于```Project OverRide```（一个```OverRapid```魔改项目）的微型本地服务器，基于```Python```和```Flask```。

此魔改项目专为游玩自制谱设计。

此repo不含官方代码和素材。不含客户端安装包。可以来管我要或者加群。

此服务器不兼容官方版本。日后看心情吧兼容官方的版本可能会放出来...


## Manual

<details>
<summary>Click to expand</summary>
<br>

### Preface

Please join QQ group (511974777) to report issues. It is not encouraged to use the private server to play the official content. Help will not be provided for this.

### Server Setup and Connection

Download the server and respective platform's installation package from the group files.

Unzip the server to your PC or MAC (referred to as the machine) and install the application package to your mobile device (referred to as the device). Linux users should help themselves lol

Android package has been renamed and icon replaced to allow better distinction with the official client. You need jailbroken devices and tools such as trollstore to install on iOS.

Install ```python``` and ```pip``` on your machine. To install ```pip``` on MAC, you can use

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

Note that MAC uses ```python3```. Code examples in this document will use the default of Windows, which is ```python```. After the installation, install ```flask``` using ```pip install flask```

After it is installed, make sure your machine and device are under the same subnetwork, say, wifi. Open ```cmd``` on PC and type ```ipconfig```. Open ```terminal``` on MAC and type ```ifconfig```.

Use the output to find the machine's subnet IPV4. Open ```config.py``` inside the server folder and change the IP address to the one you just got. Change the port as you please.
 
Open cmd in the server directory and type python 6000.py. Wait a moment. Once the server started, Open ```OverRide``` on your device.

In the Connection UI, enter the server's ```http://ip:port/``` according to the specification.

Click OK, and enter a username, or an existing 24-digit ```UID``` (covered in the "Advanced" section).

Download all the resources and enter the game.

### Adding Charts

Download the chart's zip archive. Move the archive to the server folder. Do not import on your own, as naming conflict might happen.

Open ```cmd``` in the server directory and type ```python importer.py```

Enter the zip archive's name. If the pack fails the built-in basic file hierarchy checks, some error messages may be shown. Those should be directed to the charter.

After the successful import, you need to restart the client or click the file verification button in the settings page.
If you want to delete a chart, go to the "Game Ready" page and note the ```SID``` on the top right corner. Open ```cmd``` in the server directory and type ```python importer.py```
Enter the ```SID``` and press ```y``` to delete.

### Advanced

#### Log in using ```UID```:

Use if you have registered before and would like to set up a new device with it.

Go to the settings page on your old device. Click the "Account" text under the "Account Settings" header 4 times. Your ```UID``` will be displayed and can be saved via screenshot. Go to the new device, enter the ```UID``` on the username page, and click OK.

#### Disable registration

Set ```REGISTRATION``` in ```config.py``` to ```False```. Account can only be restored via UID after this is turned off.

#### Ban user

Open ```player.db``` using ```DB Browser``` and go to the specific player. change the ```banned``` value. 0 means not banned. 1 means the user cannot change their nickname nor submit scores to leaderboard. If the value is a string, the user will be prompted the string as the reason of their ban, and the client will close after the the text prompt is shown (after intro video is done).

#### Reset leaderboard

clear the ```rank``` table of the database.

### Charting

```OverRide``` uses ```BMS``` charting specification. Audio playbacks are overwritten (keysound will not work, and the sound files specified within the chart file is ignored). Channel 0, 1, 2 are the left 3 lanes, 3, 4 are scratch lanes for left and right, and 5, 6, 7 are the right 3 lanes. Speed changes can be specified using BMS's built in ```bpm``` capability, and chart reverse can be assigned using ```0B``` and ```0C```.

Two ways to make charts:

1.	Use OSU! Mania to make 8k charts and convert the ```.osu``` file to ```.bms```. The conversion tool is in the group file. Note: Use text editor to remove negative value TimingPoint from the .osu charts, or the tool will report error. After conversion, use a text editor to replace all ```ZZ``` to ```01```. After that, open the ```.bms``` chart with ```pBMsc``` to fix and modify. The chart should not contain non-01 value.

2.	Use Malody to make 8k charts and convert the file to ```.bms```. Exploring...

// I will leave the actual charting to the professionals

You should have a ```mp3``` file and ```bms``` charts.

Make a ```id``` string for the song. Don't worry about collisions, as ```importer``` can address these. Find a thumbnail and name it ```id.jpg/png```.
Rename the charts to ```id_difficulty.bms```. Supported difficulties are ```EL,EX,PR,LPR,EL4,EX4,PR4```

Place charts to ```note``` folder. Place the thumbnail to ```thumbs``` folder. Place the music to ```music``` folder.
 
That's it for files. Next, let's modify ```manifest.json```.

```
[
  {
    "id": 1, // Ignore
    "title": "Music Name", // Music title
    "artist": "Music Artist", //Musician
    "isJapanese": false,	//Use Japanese display mode
    "bpm": 167,	//bpm number
    "sync_6k": "0/0/0/-1400", //Chart offset values. 6k: EL,EX,LPR,PR. 4k: EL,EX,PR.
    "sync_4k": "0/0/0",
    "diff_6k": "0/0/0/18",	// Chart difficulty。If not charted, use 0.
    "diff_4k": "0/0/0",
    "charter_6k": "-/-/-/charterA", //Charter information
    "charter_4k": "-/-/-",
    "mp3": "song",	//Song ID.
    "preview": "-1/-1", //Start time of 2 music previews, in seconds.
    "bga": "-1400/24/3559" // Delete this line if no BGA is available
    }
]
```

If you wish to make BGA, see section below. If not, delete the ```bga``` field.

That's it for the manifest. Select all files and folders, and compress to ```zip```. See "Adding Charts" section for chart importing.

### Importer File Checking

```importer``` will conduct basic check for the zip file. If the check is passed, only the necessary files will be copied to the server. 5 checks are conducted:

1.	A correctly named jpg or png should be in the thumbs folder.

Example: If the song ID is ```test```, a ```test.jpg``` or ```test.png``` should exist.

2.	The correctly named mp3 should be in the music folder.

Example: If the song ID is ```test```, a ```test.mp3``` should exist.

3.	If the manifest contains bga section, the bga zip file should be in the bga folder.

Example: If the song ID is ```test``` and has a ```bga``` section in manifest, a ```test.zip``` should exist.
 
4.	If the manifest does not have bga, there should not be a bga zip file in the bga folder.

Example: If song ID ```test``` does not have ```bga``` section in manifest, ```test.zip``` should not exist. Note: Did you forget to add the bga to manifest?

5.	All difficulties specified in the manifest should have a corresponding note file in the note folder.

Example: Song ID is ```test``` and manifest specifies multiple non-zero difficulties. All charts should exist.

### Making BGA

Download the MP4 from YouTube or other platforms. 360p is enough.

Put the video in the folder from the archive. Remember to ```pip install opencv-python```

Open ```cmd``` in the directory and type ```python v2b.py```

Follow the instructions. ```fps``` are typically 15 or 24. After the frames are extracted, go to the output folder and remove the black frame at the start and end to save some space.

ZIP all the images and fill the ```bga``` section of the manifest.

The 1st number is the millisecond offset. The 2nd number is the frame rate. The 3rd number is the frame number of the last frame.

Add the zip archive to the bga directory.

</details>

## 使用手册

<details>
<summary>点击放大</summary>
<br>

### 前言

如有错漏敬请加群（511974777）联系。不鼓励使用私服游玩官曲的行为。不会提供这方面的帮助。

### 搭建服务器和连接


群文件下载服务器，下载对应平台的安装包。

PC 或 MAC（统称主机）解压服务器，linux 自己去搞（

设备安装下载好的安装包。 Android 已修改包名和图标，不会和官方冲突。iOS 需要 trollstore 之类的 jailbroken 工具。

主机安装 ```python```，安装 ```pip```。MAC 安装 ```pip``` 可使用

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

注意 MAC 默认为 ```python3```。往后的示例默认用 windows 的默认，即 ```python```。安装完成后 ```pip install flask```

安装完成后，设备和主机确认在同一子网下，例如 wifi。

PC 打开 ```cmd``` 输入 ```ipconfig```。MAC 打开 ```terminal``` 输入 ```ifconfig```。进而找到本机的子网 IPV4。
主机打开服务器文件夹的 ```config.py``` 修改 IP 地址。Port 也可以更改。

服务器文件夹内 ```cmd``` 输入 ```python 6000.py```，等一小会。跑起来之后，设备打开 ```OverRide```.

接下来的连接窗口，按照格式输入服务器的 ```http://ip:port/```

点击 OK，输入用户名或已有的 24 位 ```UID```（高级操作章节）。下载资源，进入游戏。
 
### 添加谱面

下载曲包 zip 文件。将压缩包移到服务器文件夹内。不要自己导入。可能出现重名问题。

服务器文件夹内 ```cmd``` 输入 ```python importer.py```

接下来输入压缩包的名字。如果曲包没有通过基本文件格式检查将报错。请向谱师提供错误截图。导入成功后重启客户端，或进入设置点击文件校验按钮。

如想删除谱面，请进入游戏就绪界面，并记住右上角的 ```SID```.

服务器文件夹内 ```cmd``` 输入 ```python importer.py```

输入 ```SID```。输入 ```y``` 来确认删除。

### 高级操作

#### 使用 ```UID``` 登录：

你之前注册过账号，并想用这个账号在新设备上玩。

进入老设备的设置页面。点击 账号设置 下的标题文字 账号 4 次。```UID``` 将显示，可以截屏保存。在新的设备上的登陆界面输入 ```UID```，点击确认。

#### 关闭注册

把```config.py```里的```REGISTRATION```设成```False```。如果关闭，只能通过UID恢复已有账号来开始游戏。

#### 封禁用户

用```DB Browser```打开```player.db```。找到该用户。修改```banned```数值。0代表不封禁。1代表禁止昵称修改并禁止排行榜分数上传。如果数值是字符串，玩家在开场视频结束后将被提示封禁，该字符串将显示给玩家，作为封禁理由。客户端将会关闭。

#### 重置排行榜

清除```rank```数据库表。

### 制谱

```OverRide``` 使用 ```BMS``` 谱面格式。音频播放不可用（按键音不可用，谱面文件内的音频被无视）。0, 1, 2 轨为左侧 3 轨，3, 4 为左右划键，5, 6, 7 为右侧 3 轨。变速可在谱面内通过 ```BMS``` 自带的 ```bpm``` 设定，谱面倒退可以通过 ```0B``` 和 ```0C``` 来指定。

目前的两个制谱方式：
 
1.	通过 OSU! Mania 制 8k 谱并将 ```.osu``` 文件转至 ```.bms```。转码工具在群文件里。注意事项：提前用文本编辑器删除负值 ```TimingPoint```，否则工具会报错。转码后用文本编辑器将所有 ```ZZ``` 变成 01. 之后用 ```pBMsc``` 打开 ```bms``` 进行修改修复并保存。谱面内不应出现非 01 的值。

2.	通过 Malody 制 8k 谱并将谱面转至 ```.bms```。正在探索中。

//具体制谱思路让专业的来写（

现在，你应该有歌曲的 ```mp3``` 音乐文件，和 ```bms``` 谱面。

给歌曲定个 ```id``` 字符串。不用担心和别人重名，如果使用 ```importer``` 导入会自动解决。找到歌曲的封面并重命名为 歌曲 ```id.jpg/png```.
将谱面重命名为 ```id_难度.bms```，支持的难度为 ```EL,EX,PR,LPR,EL4,EX4,PR4```.
谱面放到 ```note``` 文件夹。歌曲封面放到 ```thumbs```。音乐文件放到 ```music```。不要放无关的文件。至此，文件安放完毕。接下来要修改 ```manifest.json```.

```
[
  {
    "id": 1, // 无视
    "title": "Music Name", // 曲名
    "artist": "Music Artist", //曲师
    "isJapanese": false,	//是否用日语模式显示 
    "bpm": 167,	//bpm 数字
    "sync_6k": "0/0/0/-1400", //谱面偏移值. 6k: EL,EX,LPR,PR. 4k: EL,EX,PR.
    "sync_4k": "0/0/0",
    "diff_6k": "0/0/0/18",	// 谱面难度。如果没有谱面填 0.
    "diff_4k": "0/0/0",
    "charter_6k": "-/-/-/charterA", //谱师信息
    "charter_4k": "-/-/-",
    "mp3": "song",	//歌曲 ID。
    "preview": "-1/-1", //两段音乐 preview 开始时间，以秒计
    "bga": "-1400/24/3559" //如曲目没有BGA删除此行
  }
]

```

如果想做 BGA 可以参考下方。如果不想做必须删除 ```bga``` 行。

至此，```manifest``` 编辑完成。全选所有文件夹和 ```manifest.json```，压缩成 ```zip```。
 
导入可以参考“添加谱面”章节。

### Importer 文件检查


Importer 会对包体进行基本检查。如果检查通过，只会将需要的文件拷贝到服务器里。总共检查 5 项内容：

1.	至少一个正确命名的 jpg 或 png 图片应该在 thumbs 文件夹里。

举例：如果歌曲 ID：```test```，```test.jpg``` 或者 ```test.png``` 应该存在。

2.	正确命名的 MP3 文件应该在 music 文件夹里。

举例：如果歌曲 ID：```test```，```test.mp3``` 应该存在。

3.	如果 manifest 里有 bga，则 bga 压缩包应该在 bga 文件夹里。

举例：如果歌曲 ID：```test``` 且 manifest 里有 ```bga``` 行，```test.zip``` 应该存在。

4.	如果 manifest 里没有 ```bga``` 而 ```bga``` 文件夹里存在 ```bga``` 压缩包。虽然不会出现错误程序也会提示。

举例：歌曲 ID：```test``` 且 manifest 里没有 ```bga``` 行，而 ```test.zip``` 存在。是不是忘写进 manifest 了？

5.	写进 manifest 的谱面难度应该都在 note 文件夹里。

举例：歌曲 ID：```test``` 且 manifest 里写明有多个非 0 难度，而 ```note``` 里缺少谱面。


### 制作 BGA

油管或者其他平台下载视频 MP4 文件。清晰度只要是 360p 以上就行。

将视频文件放到解压的文件夹里。记得 ```pip install opencv-python```

文件夹内 ```cmd``` 输入 ```python v2b.py```

根据提示操作，一般 ```fps``` 为 15 或 24. 完成后进入文件夹，删除黑屏的帧来节省空间。
 
所有图片压 zip 包，填写 manifest 里的 ```bga```。

第一个数字为毫秒偏移。第二个数字为帧率。第三个数字为最后一帧的数字。将压好的 zip 包放到 ```bga``` 文件夹里。

</details>