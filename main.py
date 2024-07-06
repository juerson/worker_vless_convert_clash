import yaml
import logging
import os
import re
import shutil


class FileHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def read_node_config(self, file_path: str) -> dict | None:
        # 验证文件路径
        if not os.path.exists(file_path):
            self.logger.error(f"文件不存在： {file_path}")
            return None

        with open(file_path, mode="r", encoding="utf-8") as stream:
            try:
                data = yaml.safe_load(stream)
                if not data:  # 如果文件内容为空
                    self.logger.error(f"YAML文件为空！")
                return data
            except yaml.YAMLError as exc:
                self.logger.error(f"YAML解析错误： {exc}")
                return None
            except Exception as e:
                self.logger.error(f"读取文件时发生错误： {e}")
                return None

    def read_txt_server(self, file_path: str) -> list | None:
        # 验证文件路径
        if not os.path.exists(file_path):
            self.logger.error(f"文件不存在： {file_path}")
            return None

        with open(file_path, mode="r", encoding="utf-8") as f:
            try:
                servers = f.readlines()
                servers_strip = {
                    server.strip() for server in servers if server.strip() != ""
                }
                if len(servers_strip) == 0:
                    self.logger.error(f"server.txt文件为空！")
                return list(servers_strip)
            except Exception as e:
                self.logger.error(f"读取server文件时发生错误： {e}")
                return None

    def read_clash_config(self, file_path: str) -> str | None:
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
                self.logger.error(f"读取文件时发生错误： {e}")
                return None

    def clear_output_folder(self, folder_path: str):
        # 检查文件夹是否存在
        if not os.path.exists(folder_path):
            # 如果不存在，创建文件夹
            os.makedirs(folder_path)
        else:
            # 如果存在，删除文件夹中的所有文件
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except OSError as e:
                    self.logger.error(f"删除文件失败：{file_path}. 原因: {e}")


def split_dict(raw_dict: dict, max_size: int) -> list:
    """
    将给定的字典拆分成多个小字典，每个小字典的大小不超过max_size。

    参数:
    raw_dict (dict): 需要被拆分的原始字典。
    max_size (int): 每个拆分后的小字典的最大大小。

    返回:
    list: 包含多个小字典的列表。
    """
    # 将字典转换为键值对列表
    items = list(raw_dict.items())

    # 将列表拆分成多个大小不超过max_size的子列表
    split_items = [items[i : i + max_size] for i in range(0, len(items), max_size)]

    # 将子列表转换回字典列表
    return [dict(sublist) for sublist in split_items]


if __name__ == "__main__":
    files = ["resources/node_config.yaml", "server.txt", "resources/clash_config.yaml"]
    # 设置日志记录器的配置
    logging.basicConfig(level=logging.ERROR)
    handler = FileHandler()
    conf = handler.read_node_config(files[0])
    servers = handler.read_txt_server(files[1])
    clash_config = handler.read_clash_config(files[2])
    handler.clear_output_folder("./output")  # 创建/清空文件夹里面的所有文件
    default_port = conf.get("port")
    if default_port:
        port = default_port  # 如果配置文件中有端口，就使用配置文件中的端口
    else:
        port = 8443  # 如果配置文件中，没有端口就使用这个端口，当然也可以改为443、2053、2083、2087、2096等端口
    if conf and servers and clash_config:  # 读取到内容（合法），才执行下面的步骤
        proxies_data_dict = {}
        for server in servers:
            # 分割出IP地址/域名、端口
            ip_with_port = re.split(r"\s+", server)
            if len(ip_with_port) > 1 and ip_with_port[1].isdigit():
                proxy_name = f"{ip_with_port[0]}:{ip_with_port[1]}"
                conf["port"] = ip_with_port[1]
            else:
                proxy_name = f"{ip_with_port[0]}:{port}"
                conf["port"] = port
            conf["name"] = proxy_name
            conf["server"] = ip_with_port[0]

            if proxy_name not in proxies_data_dict:
                proxies_data_dict[proxy_name] = "  - {}".format(
                    str(conf).replace(": True", ": true").replace(": False", ": false")
                )
        # 将字典拆分成多个小字典，每个小字典的大小不超过300(即，每个配置文件最多300个节点)
        chunk_data = split_dict(proxies_data_dict, 300)

        for index, sub_dict in enumerate(chunk_data):
            indexing = str(index + 1).zfill(len(str(len(chunk_data))))
            proxy_name_string = "\n".join(
                [f"      - {item}" for item in sub_dict.keys()]
            )
            nodes_string = "\n".join(map(str, sub_dict.values()))
            clash_config = clash_config.replace(
                "  - {name: 01, server: 127.0.0.1, port: 80, type: ss, cipher: aes-128-gcm, password: a123456}",
                nodes_string,
            ).replace("      - 01", proxy_name_string)
            with open(
                "output/clash_{}.yaml".format(indexing), mode="w", encoding="utf-8"
            ) as file:
                file.write(clash_config)
