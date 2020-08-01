import os,sys,json,string,time,random,re,traceback,hashlib

cur_Dir = sys.path[0]#os.getcwd()

global data
data = {}

def load_old_data():
    global data
    with open(os.path.join(cur_Dir,"index.json"),"r",encoding = "utf-8") as reader:
        data = json.loads(reader.read())
    
def _get_SHA1(path):
    sha1Obj = hashlib.sha1()
    with open(path, 'rb') as file:
        sha1Obj.update(file.read())
    return(sha1Obj.hexdigest())
def get_local_mod_version(path):
    if os.path.isfile(path):
        with open(path,"r",encoding = "utf-8") as reader:
            result = re.search(r'(?<=version_str \= ").*?(?=")',reader.read())
            return(str(result.group()) if result is not None else None)
    return(None)
def save_data():
    global data
    if os.path.isfile(os.path.join(cur_Dir,"index.json")):
        if os.path.isfile(os.path.join(cur_Dir,"index.json.bak")):
            os.remove(os.path.join(cur_Dir,"index.json.bak"))
        os.rename(os.path.join(cur_Dir,"index.json"), os.path.join(cur_Dir,"index.json.bak"))
    with open(os.path.join(cur_Dir,"index.json"),"w",encoding = "utf-8") as writer:
        writer.write(json.dumps(data,ensure_ascii=False,sort_keys=True,indent = 1))

def get_file_info_dict(path):
    info_dict = {}
    if os.path.isfile(path):
        info_dict["SHA-1"] = _get_SHA1(path)
        info_dict["m_time"] = os.path.getmtime(path)
        info_dict["size"] = os.path.getsize(path)
        if path.endswith(".py"):
            info_dict["version"] = get_local_mod_version(path)
    return(info_dict)
def process_data():
    global data
    if "mods" not in data:data["mods"] = {}
    for name,item in data.get("mods",{}).items():
        path = os.path.join(cur_Dir,"ba_mods"+os.sep,name)
        if os.path.exists(path):
            file_path = os.path.join(path,item.get("file"))
            if os.path.isfile(file_path):
                data["mods"][name] = dict(data["mods"][name] , **get_file_info_dict(file_path))


load_old_data()

process_data()

save_data()
