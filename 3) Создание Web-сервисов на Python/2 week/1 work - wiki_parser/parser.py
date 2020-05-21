from bs4 import BeautifulSoup
import unittest


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


class TestParse(unittest.TestCase):
    def test_parse(self):
        test_cases = (
            ('wiki/Stone_Age', [13, 10, 12, 40]),
            ('wiki/Brain', [19, 5, 25, 11]),
            ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
            ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
            ('wiki/Spectrogram', [1, 2, 4, 7]),)

        for path, expected in test_cases:
            with self.subTest(path=path, expected=expected):
                self.assertEqual(parse(path), expected)


if __name__ == '__main__':
    unittest.main()

