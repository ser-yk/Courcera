import requests, re
pattern = r'<a.*href=[\'|\"](\w*?\:\/\/)?(\w[\w*|\.|\-]*).*?[\'|\"].*?>'
set_url = set([i[1] for i in re.findall(pattern, requests.get('http://pastebin.com/raw/hfMThaGb').text)])
for url in sorted(set_url):
    print(url)

# 'https://pastebin.com/raw/7543p0ns'