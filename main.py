import os
import shutil
import zipfile
import requests

# 下载zip文件
url = "https://github.com/ipverse/asn-ip/archive/refs/heads/master.zip"
r = requests.get(url)
with open("master.zip", "wb") as code:
  code.write(r.content)

# 解压zip文件
with zipfile.ZipFile("master.zip", 'r') as zip_ref:
  zip_ref.extractall(".")

# 将结果存储在这个列表中
ip_addresses = []
excluded_asns = ['209242', '13335', '149648', '132892', '139242', '202623', '203898', '394536']

# 遍历as文件夹
for root, dirs, files in os.walk("asn-ip-master/as"):
  # 只查看包含 'ipv4-aggregated.txt' 的文件
  if 'ipv4-aggregated.txt' in files:
    asn = root.split('/')[-1]
    # 排除指定的asn
    if asn not in excluded_asns:
      with open(os.path.join(root, 'ipv4-aggregated.txt'), 'r') as file:
        ips = file.read().splitlines()
        ip_addresses.extend(ips)

# 将结果写入一个新的文件
with open('merged_ips.txt', 'w') as file:
  for ip in ip_addresses:
    file.write(f"{ip}\n")

# 清理下载的zip文件和解压的文件夹
os.remove("master.zip")
shutil.rmtree("asn-ip-master")
