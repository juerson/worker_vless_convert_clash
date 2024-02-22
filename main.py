import yaml
import logging
import os

FILES = ["vless_config.yaml", "server.txt", "rules.txt"]
BASE_CONFIG = r"""mode: rule
mixed-port: 7897
socks-port: 7898
port: 7899
allow-lan: false
log-level: info
ipv6: false
secret: ''
external-controller: 127.0.0.1:9097
dns:
  enable: true
  ipv6: false
  listen: 0.0.0.0:53
  enhanced-mode: fake-ip
  nameserver:
    - 223.5.5.5
    - 119.29.29.29
    - 8.8.8.8
  fallback:
    - 8.8.4.4
    - 1.1.1.1
    - tls://dns.google:853
    - tls://1.0.0.1:853
  fake-ip-filter:
    - +.stun.*.*
    - +.stun.*.*.*
    - +.stun.*.*.*.*
    - +.stun.*.*.*.*.*
    - '*.n.n.srv.nintendo.net'
    - +.stun.playstation.net
    - xbox.*.*.microsoft.com
    - '*.*.xboxlive.com'
    - '*.msftncsi.com'
    - '*.msftconnecttest.com'
    - WORKGROUP
    - '*.yeanson.cn'
    - '*.lan'
    - '*.nxtlnodes.com'
    - suo.yt
    - time.*.com
    - time.*.gov
    - time.*.edu.cn
    - time.*.apple.com
    - time1.*.com
    - time2.*.com
    - time3.*.com
    - time4.*.com
    - time5.*.com
    - time6.*.com
    - time7.*.com
    - ntp.*.com
    - ntp1.*.com
    - ntp2.*.com
    - ntp3.*.com
    - ntp4.*.com
    - ntp5.*.com
    - ntp6.*.com
    - ntp7.*.com
    - '*.time.edu.cn'
    - '*.ntp.org.cn'
    - +.pool.ntp.org
    - time1.cloud.tencent.com
  fallback-filter:
    geoip: true
    geoip-code: CN
    ipcidr:
      - 240.0.0.0/4
      - 0.0.0.0/32
      - 127.0.0.1/32
    domain:
      - +.google.com
      - +.facebook.com
      - +.twitter.com
      - +.youtube.com
      - +.xn--ngstr-lra8j.com
      - +.google.cn
      - +.googleapis.cn
      - +.googleapis.com
      - +.gvt1.com
global-client-fingerprint: chrome
"""
PROXY_GROUPS = {
    "select_group": """  - name: 🔰 节点选择
    type: select
    proxies:
      - ♻️ 自动选择
      - 🎯 全球直连
""",
    "auto_group": """  - name: ♻️ 自动选择
    type: url-test
    url: http://www.gstatic.com/generate_204
    interval: 300
    proxies:
""",
    "netflix_group": """  - name: 🎥 NETFLIX
    type: select
    proxies:
      - 🔰 节点选择
      - ♻️ 自动选择
      - 🎯 全球直连
""",
    "homeless_exile_group": """  - name: 🐟 漏网之鱼
    type: select
    proxies:
      - 🔰 节点选择
      - 🎯 全球直连
      - ♻️ 自动选择
""",
    "telegram_group": """  - name: 📲 电报信息
    type: select
    proxies:
      - 🔰 节点选择
      - 🎯 全球直连
""",
    "microsoft_group": """  - name: Ⓜ️ 微软服务
    type: select
    proxies:
      - 🎯 全球直连
      - 🔰 节点选择
""",
    "apple_group": """  - name: 🍎 苹果服务
    type: select
    proxies:
      - 🔰 节点选择
      - 🎯 全球直连
      - ♻️ 自动选择
""",
    "foreign_media_group": """  - name: 🌍 国外媒体
    type: select
    proxies:
      - 🔰 节点选择
      - ♻️ 自动选择
      - 🎯 全球直连
""",
    "national_media_group": """  - name: 🌏 国内媒体
    type: select
    proxies:
      - 🎯 全球直连
      - 🔰 节点选择
""",
    "hijacking_group": """  - name: 🚫 运营劫持
    type: select
    proxies:
      - 🛑 全球拦截
      - 🎯 全球直连
      - 🔰 节点选择
""",
    "adblock_group": """  - name: ⛔️ 广告拦截
    type: select
    proxies:
      - 🛑 全球拦截
      - 🎯 全球直连
      - 🔰 节点选择
""",
    "global_block_group": """  - name: 🛑 全球拦截
    type: select
    proxies:
      - REJECT
      - DIRECT
""",
    "direct_group": """  - name: 🎯 全球直连
    type: select
    proxies:
      - DIRECT
"""
}


class FileHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def read_yaml_info(self, file_path):
        # 验证文件路径
        if not os.path.exists(file_path):
            self.logger.error(f"文件不存在： {file_path}")
            return None

        with open(file_path, mode='r', encoding='utf-8') as stream:
            try:
                data = yaml.safe_load(stream)
                if not data:  # 如果文件内容为空
                    self.logger.error(f"YAML文件为空！")
                return data
            except yaml.YAMLError as exc:
                self.logger.error(f"YAML解析错误： {exc}")
                return None
            except Exception as e:
                self.logger.error(f"读取YAML文件时发生错误： {e}")
                return None

    def read_txt_server(self, file_path):
        # 验证文件路径
        if not os.path.exists(file_path):
            self.logger.error(f"文件不存在： {file_path}")
            return None

        with open(file_path, mode='r', encoding='utf-8') as f:
            try:
                servers = f.readlines()
                servers_strip = {server.strip() for server in servers if server != ""}
                if len(servers_strip) == 0:
                    self.logger.error(f"server.txt文件为空！")
                return list(servers_strip)
            except Exception as e:
                self.logger.error(f"读取server文件时发生错误： {e}")
                return None

    def read_txt_rules(self, file_path):
        # 验证文件路径
        if not os.path.exists(file_path):
            self.logger.error(f"文件不存在： {file_path}")
            return None

        with open(file_path, mode="r", encoding="utf-8") as f:
            try:
                data = f.read()
                if not data:
                    self.logger.error(f"rules.txt文件为空！")
                return data
            except Exception as e:
                self.logger.error(f"读取rules文件时发生错误： {e}")
                return None


if __name__ == '__main__':
    port = 8443  # 写入vless配置的，全部都用这个端口，可以改为443、2053、2083、2087、2096、8443
    # 设置日志记录器的配置
    logging.basicConfig(level=logging.ERROR)
    handler = FileHandler()
    conf = handler.read_yaml_info(FILES[0])
    servers = handler.read_txt_server(FILES[1])
    RULES = handler.read_txt_rules(FILES[2])
    if conf and servers and RULES:  # 读取到的内容合法，才执行下面的步骤
        node_names = []
        node_li = ["proxies:\n", ]
        for server in servers:
            name = f"{server}:{port}"
            conf["name"] = name
            conf["server"] = server
            conf["port"] = port
            node_names.append(name)
            node_info_str = f"  - {str(conf).replace(": True,", ": true,").replace(": False,", ": false,")}\n"
            node_li.append(node_info_str)
        node_names = [f"      - {item}" for item in node_names]
        proxy_groups_string = ""
        proxies = "".join(node_li)
        for k, v in PROXY_GROUPS.items():
            if k in ["select_group", "auto_group", "netflix_group", "homeless_exile_group", "telegram_group",
                     "microsoft_group", "apple_group", "foreign_media_group"]:
                proxy_groups_string += (v + "\n".join(node_names) + "\n")  # 这个添加节点名称
            else:
                proxy_groups_string += v  # 这个不需要添加节点名称
        # 构建clash的全部信息
        clash_content = BASE_CONFIG + proxies + "proxy-groups:\n" + proxy_groups_string + RULES
        with open("clash.yaml", mode="w", encoding="utf-8") as wf:
            wf.write(clash_content)
