import urllib.request

#  try:
#  def unshorturl(url):
url = 'http://t.cn/EA4CEJX'
res = urllib.request.urlopen(url, timeout=2000)
#  return res.text
print(res.geturl())
#  except BaseException:
#  pass
#  print(unshorturl('http://t.cn/EAzx3mO'))
#  import httplib

#  conn = httplib.HTTPConnection("http://t.cn/EAzx3mO")
#  conn.request("HEAD", "/hOH39")
#  res = conn.getresponse()
#  print(res.getheader("location"))
