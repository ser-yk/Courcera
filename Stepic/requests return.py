import requests, re

def search_url(first_url, pattern, i_find, cnt=2, check=False):
    if cnt != 0:
        cnt -= 1
        for url in re.findall(pattern, requests.get(first_url).text):
            if url.strip() == i_find and cnt == 0:
                return True
            else:
                check = search_url(url.strip(), pattern, i_find, cnt)
                if check:
                    return check
    else:
        return check

pattern = r'https\S*[.*]html'
line = 'https://stepic.org/media/attachments/lesson/24472/sample0.html'
two_url = 'https://stepic.org/media/attachments/lesson/24472/sample2.html'

if search_url('https://stepic.org/media/attachments/lesson/24472/sample0.html', pattern,
              'https://stepic.org/media/attachments/lesson/24472/sample1.html') == True:
    print('Yes')
else:
    print('No')

if search_url(line, pattern, two_url) == True:
    print('Yes')
else:
    print('No')
