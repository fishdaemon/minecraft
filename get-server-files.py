import os, json
from client import Exaroton
from pathlib import Path
import urllib.parse
def p(data):
    print(json.dumps(data, indent=4))


def is_error(data):
    if type(data) is dict:
        if data.get("success") == False:
            raise Exception(f"{data}")
    return False

def save_file(child):
    file_name = Path("out" + child["path"])
    file_name.parent.mkdir(exist_ok=True, parents=True)
    write_mode = "w"
    if not child["isTextFile"]:
        write_mode = "wb"

    with open(file_name, write_mode) as f:

        if child["size"] > 0:
            data = exa.get_file_data(server_id, urllib.parse.quote(child["path"]))
            is_error(data)

            if child["isTextFile"]:
                f.write(str(data))
            else:

                if data is None:
                    print(f"skipping because none:  {child['path']}")
                else:
                    f.write(data)


def save_config_file(child):
    data = exa.get_config_options(server_id, child["path"])
    is_error(data)
    rows = list()
    for item in data["data"]:
        rows.append(f"{item['key']}={item['value']}")
    file_name = Path("out" + child["path"])
    file_name.parent.mkdir(exist_ok=True, parents=True)
    with open(file_name, "w") as f:
        f.write("\n".join(rows))

exa = Exaroton(os.environ["EXA_TOKEN"])

# print(exa.get_servers())
# exit(0)

server_id = "XxrkVHHSlNKwYznV"

def recurse(path):
    root_d = exa.get_file_info(server_id, path)
    for child in root_d["data"]["children"]:
        if not child["isDirectory"]:
            print(f"saving {child['path']}")
            if child["isConfigFile"]:
                save_config_file(child)
            else:
                save_file(child)
        else:
            if "/world" in child["path"]:
                print(f"skipping world {child['path']}")
                continue
            recurse(child["path"])



root_d = exa.get_file_info(server_id)
# with open("SilkTouchSpawners-1.1.0.jar", "wb") as f:
#     f.write(exa.get_file_data("ZvERSZ4gyiTeM5RV", "plugins/Clearlag.jar"))
recurse("")
exit(0)
with open("SilkTouchSpawners-1.1.0.jar", "wb") as f:
    f.write(exa.get_file_data("ZvERSZ4gyiTeM5RV", "plugins/SilkTouchSpawners-1.1.0.jar"))
