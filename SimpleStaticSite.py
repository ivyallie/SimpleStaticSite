# SimpleStaticSite by John Allie. v.1
# johnwallie.com
# MIT License. Do as you will, at your own risk.

from os import listdir, path
from os.path import isfile, join
from bs4 import BeautifulSoup
import markdown as md


def get_title(input):
    soup = BeautifulSoup(input, 'lxml')
    h1 = soup.h1
    if h1:
        return h1.string
    return "Title"


def get_files_by_type(type):
    return [f for f in listdir('./Pages') if isfile(join('./Pages', f)) and f.endswith("." + type)]


def handle_md(files):
    for page in files:
        pageFilename = join('./Pages', page)
        md_source = open(pageFilename, 'r').read()
        html = md.markdown(md_source)
        title = get_title(html)
        write_output(page, html, title)


def handle_html(files):
    for page in files:
        inputFilename = join('./Pages', page)
        sourceHTML = open(inputFilename, 'r').read()
        title = get_title(sourceHTML)
        write_output(page, sourceHTML, title)


def set_title(title):
    upper = open('Template_Upper.html', 'r').read()
    soup = BeautifulSoup(upper, 'lxml')
    title_element = soup.title
    title_element.string.replace_with(title)
    return str(soup)


def write_output(page, content, title):
    outputFilename = join('./Output', str(path.splitext(page)[0]) + '.html')
    print("Now writing " + outputFilename + " from " + page)
    upper = set_title(title)
    lower = open('Template_Lower.html', 'r')

    with open(outputFilename, 'w+') as output:
        for line in upper:
            output.write(line)
        for line in content:
            output.write(line)
        for line in lower:
            output.write(line)

    lower.close()
    output.close()


handle_html(get_files_by_type('html'))
handle_md(get_files_by_type('md'))






