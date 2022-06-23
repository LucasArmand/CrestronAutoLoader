import websocket
import asyncio
import ssl
import requests as req
import urllib3
# Suppresses warnings for not having an SSL certificate
urllib3.disable_warnings()

url = "https://169.254.108.215"
user = "admin"
passwd = "Solutionz1!"

# Get the initial TRACKID cookie from the login page
login = req.get(url + "/userlogin.html", verify=False)
TRACKID = login.cookies.get("TRACKID")

# Get authentication cookies to login
auth = req.post(url + "/userlogin.html"
                    ,headers={"Cookie":"TRACKID=" + TRACKID, "Origin":url, "Referer":url + "/userlogin.html"}
                    ,data="login=admin&&passwd=Solutionz1!"
                    ,verify=False)
iv = auth.cookies["iv"]
tag = auth.cookies["tag"]
userid = auth.cookies["userid"]
usrstr = auth.cookies["userstr"]
authByPasswd = auth.cookies["AuthByPasswd"]
websocket.enableTrace(True)
ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
ws.connect("wss://169.254.108.215/websockify", header=["Upgrade: websocket", 
                                                        "Connection: Upgrade",
                                                        "User-Agent: advanced-rest-client",
                                                        "Accept-Encoding: gzip, deflate, br", 
                                                        "Accept-Language: en-US, en;q=0.9",
                                                        "Sec-Websocket-Extensions: permessage-deflate; client_max_window_bits",
                                                        "Cookie:userstr="+usrstr+";userid=" + userid + ";" +
                                                        "iv=" + iv + ";tag=" + tag + ";AuthByPasswd=" + 
                                                        authByPasswd + ";TRACKID="+TRACKID+";"])
operations = req.get(url + "/Device/DeviceOperations", cookies = auth.cookies, verify=False)
print(operations.content)
ws.send('{"Device":{"DeviceOperations":{"FirmwareUpgrade":"", "FirmwareUpgradePath" : "/firmware/dm-nvx-ed30-enc_7.0.5057.00023_r453766.zip"}}}')
print(ws.recv())
operations = req.get(url + "/Device/DeviceOperations/UpgradeStatus", cookies = auth.cookies, verify=False)
print(operations.content)
ws.close()