import requests as req
import urllib3


'''
This code allows for interface with each device using GET
and POST HTTPS methods.
'''

# Suppresses warnings for not having an SSL certificate
urllib3.disable_warnings()

url = "https://169.254.140.147"
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


print(TRACKID)
iv = auth.cookies["iv"]
tag = auth.cookies["tag"]
userid = auth.cookies["userid"]
usrstr = auth.cookies["userstr"]
authByPasswd = auth.cookies["AuthByPasswd"]
cookies = {"iv":iv, "tag":tag, "userid":userid, "userstr":usrstr, "AuthByPasswd":authByPasswd, "TRACKID":TRACKID}
### SAMPLE CODE ###
ethernet = req.get(url + "/Device/Ethernet/HostName", cookies = auth.cookies, verify=False)
print(ethernet.cookies)
print(ethernet.content)
cookies["AuthByPasswd"] = ethernet.cookies["AuthByPasswd"]
post = req.post(url + "/Device", headers = {"X-CREST-XSRF-TOKEN":"false", "Cookie":"userstr=\""+usrstr+"\";Path=/;Secure;HttpOnly; userid=\"" + userid + "\";Path=/;Secure;HttpOnly;" +
 "iv=\"" + iv + "\";Path=/;Secure;HttpOnly; tag=\"" + tag + "\";Path=/;Secure;HttpOnly;AuthByPasswd=\"" + authByPasswd + "\";Path=/;Secure;HttpOnly;TRACKID=\""+TRACKID+"\";Path=/;Secure;HttpOnly;", "Referer": "169.254.140.147"}, data = '{"Device":{"Ethernet":{"HostName" : "NewHostName"}}}', verify=False)
print(post.content)

#auth = req.post(url + "/userlogin.html"
#                    ,headers={"Cookie":"TRACKID=" + TRACKID, "Origin":url, "Referer":url + "/userlogin.html"}
#                    ,data="login=admin&&passwd=Solutionz1!"
#                    ,verify=False)
#print(auth.content)
ethernet = req.get(url + "/Device/Ethernet/HostName", cookies = auth.cookies, verify=False)
print(ethernet.content)



# Logout of current session
req.get(url + "/logout", verify=False)