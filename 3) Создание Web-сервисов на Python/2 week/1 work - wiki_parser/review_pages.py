import re
import time

from bs4 import BeautifulSoup

def parse(path_to_file):
    with open(path_to_file, encoding='utf8') as html_file:
        soup = BeautifulSoup(html_file.read(), 'lxml').find(id='bodyContent')
        # Find a images with width lager than 200.
        imgs = len([img for img in soup.find_all('img', width=True) if int(img['width']) >= 200])
        # Find headers 'h' that starts with are E, T, C.
        headers = len([header for header in soup.find_all(('h1', 'h2', 'h3', 'h4', 'h5', 'h6'))
                       if header.text[:1] in ('E', 'T', 'C')])
        # Find max sequence of tags 'a'.
        linkslen = 0
        for tag in soup.recursiveChildGenerator():
            if tag.name == 'a':
                cnt = 1
                next_tags = tag.find_next_siblings()
                if next_tags:
                    for i in next_tags:
                        if i.name == 'a':
                            cnt += 1
                        else:
                            break
                    if linkslen < cnt:
                        linkslen = cnt
        # Find ul, ol if one is not nested in other
        lists = sum(
            1 for tag in soup.find_all(['ol', 'ul']) if not tag.find_parent(['ol', 'ul']))

        return [imgs, headers, linkslen, lists]


def build_bridge(path, start_page, end_page, cnt=1, visited=None):
    """возвращает список страниц, по которым можно перейти по ссылкам со start_page на
    end_page, начальная и конечная страницы включаются в результирующий список"""
    visited = visited or set()
    all_links = {1: {start_page}}
    new_vis = dict()
    if start_page == end_page:
        return [end_page]
    while True:
        if all_links[cnt]:
            next_link = all_links[cnt].pop()
            visited.add(next_link)
            temp = find_all_links_on_page(path, next_link, cnt+1, visited, all_links)
            if temp:
                if cnt in new_vis:
                    new_vis[cnt][next_link] = temp
                else:
                    new_vis[cnt] = {next_link: temp}

                if end_page in temp:
                    return search_path(next_link, cnt, start_page, new_vis) + [end_page]
        else:
            cnt += 1


def search_path(last_link, cnt, start_page, branch_links):
    if cnt == 1:
        return list(branch_links[cnt].keys())
    for up_link in branch_links[cnt-1]:
        if last_link in branch_links[cnt-1][up_link]:
            res = search_path(up_link, cnt-1, start_page, branch_links)
            if res:
                return res + [last_link]


def find_all_links_on_page(path, start_page, cnt, visited, all_links):
    try:
        with open(f'{path}{start_page}', encoding='utf8') as f:
            soup = BeautifulSoup(f.read(), 'lxml')
            links = [link for link in BeautifulSoup.recursiveChildGenerator(soup) if link.name == 'a']
            temp = set()
            # Добавляем подходящие ссылки в словарь
            for link in links:
                try:
                    pattern = f'^([\w\/]*wiki\/(\w*\D*\w+\D\w*))$'
                    href = link.get('href')
                    file_name = re.findall(pattern, href)
                    if file_name:
                        if file_name[0][1] not in visited:
                            temp.add(file_name[0][1])
                            if cnt in all_links:
                                all_links[cnt].add(file_name[0][1])
                            else:
                                all_links[cnt] = set(file_name[0][1])
                except:
                    continue
            return temp
    except:
        return


def get_statistics(path, start_page, end_page):
    """собирает статистику со страниц, возвращает словарь, где ключ - название страницы,
    значение - список со статистикой страницы"""
    statistic = dict()
    pages = build_bridge(path, start_page, end_page)
    for page in pages:
        statistic[page] = parse(path+page)
    return statistic


# Python_(programming_language)
t1 = time.time()
print(get_statistics(r'wiki/', 'Stone_Age', 'Artificial_intelligence'))
print(time.time() - t1)


