import base64,zlib,json,sys,os,datetime

def _d(x):
    return json.loads(zlib.decompress(base64.b64decode(x)).decode())

def _fmt_gb(v):
    try:return f"{v/(1024**3):.2f} GB"
    except:return "?"

def _w(f,t,d):
    f.write(f"\n== {t} ==\n")
    if isinstance(d,dict):
        for k,v in d.items():f.write(f"{k}: {v}\n")
    elif isinstance(d,list):
        for i in d:f.write(f"- {i}\n")
    else:f.write(str(d)+"\n")

def build_report(data):
    out=[]

    A=data.get("A",{})
    B=data.get("B",{})
    C=data.get("C",{})
    D=data.get("D",{})
    T=data.get("T",0)

    out.append("### SYSTEM REPORT ###\n")

    out.append("[IDENTITY]")
    out.append(f"User: {A.get('id')}")
    out.append(f"Hostname: {A.get('h')}")
    out.append(f"Public IP: {A.get('ip',[None,None])[0]}")
    out.append(f"Local IP: {A.get('ip',[None,None])[1]}")
    out.append(f"Boot Time: {datetime.datetime.fromtimestamp(A.get('bt',0))}\n")

    out.append("[GEOLOCATION ~ APPROX]")
    out.append(f"City: {B.get('c')}")
    out.append(f"Region: {B.get('r')}")
    out.append(f"Country: {B.get('co')}")
    out.append(f"Latitude: {B.get('lt')}")
    out.append(f"Longitude: {B.get('ln')}")
    out.append(f"Timezone: {B.get('tz')}")
    out.append(f"ISP: {B.get('isp')}\n")

    sys=C.get("os",[])
    out.append("[SYSTEM]")
    out.append(f"OS: {' '.join([str(x) for x in sys if x])}")

    cpu=C.get("cpu",{})
    out.append(f"CPU Cores: {cpu.get('c')}")
    out.append(f"CPU Usage: {cpu.get('u')}%")

    ram=C.get("ram",{})
    out.append(f"RAM Total: {_fmt_gb(ram.get('t',0))}")
    out.append(f"RAM Used: {_fmt_gb(ram.get('u',0))}")
    out.append(f"RAM Usage: {ram.get('p')}%")

    dsk=C.get("dsk",{})
    out.append(f"Disk Total: {_fmt_gb(dsk.get('t',0))}")
    out.append(f"Disk Free: {_fmt_gb(dsk.get('f',0))}")
    out.append(f"Disk Usage: {dsk.get('p')}%")

    gpus=C.get("gpu",[])
    out.append("\n[GPU]")
    if gpus:
        for g in gpus:
            out.append(f"- {g.get('n')} | load:{g.get('l')} temp:{g.get('t')}")
    else:
        out.append("N/A")

    out.append("\n[ACTIVITY]")
    pr=D.get("pr",{})
    out.append(f"Processes: {pr.get('p')}")
    out.append(f"Threads: {pr.get('t')}")

    bt=D.get("bt",{})
    if bt:
        out.append(f"Battery: {bt.get('p')}% {'Charging' if bt.get('c') else 'Not Charging'}")
    else:
        out.append("Battery: N/A")

    out.append(f"Interfaces: {', '.join(D.get('if',[]))}")
    out.append(f"Drives: {', '.join(D.get('dr',[]))}")

    out.append("\n[NETWORK SNAPSHOT]")
    for l in D.get("ns",[]):out.append(l)

    out.append("\n[TIMESTAMP]")
    out.append(str(datetime.datetime.fromtimestamp(T)))

    return "\n".join(out)

def main():
    if len(sys.argv)<2:
        print("usage: python decode.py <file>")
        return

    path=sys.argv[1]

    try:
        with open(path,"r") as f:
            raw=f.read().strip()

        data=_d(raw)
        report=build_report(data)

        out_path=path+".decoded.txt"
        with open(out_path,"w",encoding="utf-8") as f:
            f.write(report)

        print(report)
        print("\n[+] saved to:",out_path)

    except Exception as e:
        print("error:",e)

if __name__=="__main__":
    main()