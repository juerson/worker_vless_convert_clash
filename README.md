将代码下载或git clone到本地电脑中，然后按下面的步骤操作：

#### 一、安装Python和PyYAML第三方库（懂的人就忽略）

1. **下载Python安装包**：
   访问Python的官方网站（https://www.python.org/downloads/ ），选择适用于您操作系统的Python版本进行下载。一般来说，Linux和macOS系统会使用.tar.xz格式的包，而Windows系统则会使用.exe安装程序。

2. **安装Python**：

   - 对于Windows系统，运行下载的.exe安装程序，按照提示完成安装。安装时建议将Python添加到系统环境变量中，这样可以在任何命令行界面中直接使用Python。
   - 对于macOS系统，下载.tar.xz包后，解压到指定目录，然后可以通过终端使用`python3`命令来调用Python。
   - 对于Linux系统，也是下载.tar.xz包后，解压到指定目录，然后可以通过终端使用`python3`命令来调用Python。

3. **验证安装**：
   打开命令行工具（在Windows中是cmd或PowerShell，macOS和Linux中是Terminal），输入`python`（或者`python3`），如果能够进入Python的交互式环境，则说明Python安装成功。

4. **安装必要的PyYAML库**：
   你可以使用 pip 来安装 PyYAML。在命令行中运行以下命令：

   ```bash
   pip install PyYAML
   ```

    如果你使用的是 Linux 或 macOS 系统，可能需要使用 `pip3` 命令来确保为 Python3 安装 PyYAML：

   ```bash
   pip3 install PyYAML
   ```

#### 二、修改 `resources/node_config.yaml` 里面的配置信息，并且将优选的CF IP或反代IP、优选域名写入到[server.txt](https://github.com/juerson/worker_vless_convert_clash/blob/master/server.txt)文件中(支持IP、域名，还支持在后面指定端口)
- vless+ws+tls：

```yaml
type: vless
name: ""
server: ""
port: 443
uuid: 9b72b1d0-9b64-48ed-aec4-b74e05b058fc # 这里修改为自己的UUID
network: ws
tls: true
udp: false
sni: xxx.pages.dev # 这里修改成自己的域名
client-fingerprint: chrome
ws-opts:
  path: "/?ed=2048" # 这个看你的情况修改
  headers:
    host: xxx.pages.dev # 这里修改成自己的域名
```
- trojan+ws+tls：

```yaml
type: trojan
name: ""
server: ""
port: 443
password: 9b72b1d0-9b64-48ed-aec4-b74e05b058fc # 修改为自己的密码 
network: ws
udp: false
sni: xxx.pages.dev # 这里修改成自己的域名
ws-opts:
  path: /
  headers:
    Host: xxx.pages.dev # 这里修改成自己的域名，这个好像可以删除，一样能使用
```
理论上，修改成其它代理协议（vmess）是可以的，程序只使用到前面的`server`、`port`和`name`字段；其它key-value，你的数据结构是怎么样的就怎么样的，自己可以灵活修改。


#### 三、执行`python main.py`命令运行

#### 四、生成的 `./output`文件夹中文件就是你需要的clash配置文件，将它导入 [clash verge](https://github.com/clash-verge-rev/clash-verge-rev) 或绝版 [clash_for_windows_pkg(英文版)](https://archive.org/download/clash_for_windows_pkg) 、[Clash for Windows V0.20.39(汉化版)](https://github.com/Z-Siqi/Clash-for-Windows_Chinese/releases/tag/CFW-V0.20.39_CN) 、[clash-nyanpasu](https://github.com/LibNyanpasu/clash-nyanpasu)、[clash-verge-rev](https://github.com/clash-verge-rev/clash-verge-rev)、[FlClash](https://github.com/chen08209/FlClash)使用即可。
