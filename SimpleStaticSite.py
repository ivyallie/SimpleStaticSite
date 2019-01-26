#!/usr/bin/python
# SimpleStaticSite by John Allie. v.2
# johnwallie.com
# MIT License. Do as you will, at your own risk.

from os import listdir, path
from os.path import isfile, join
from bs4 import BeautifulSoup
import yaml
import markdown as md


def get_config():
    yaml_files = get_files_by_type('yaml', './')
    print(yaml_files)
    if yaml_files:
        file = yaml_files[0]
        print("Found config file",file)
        with open(file, 'r') as configfile:
            config = yaml.load(configfile)
            return config
    else:
        print('No config file found.')
        return False


def get_option(name, config):
    try:
        value = config[name]
    except KeyError:
        value = False
    return value


def get_title(inputfile):
    soup = BeautifulSoup(inputfile, 'lxml')
    title_stub = ''
    separator = ''
    if config:
        title_stub = get_option('title', config)
        separator = get_option('separator', config)
    h1 = soup.h1
    if h1 and title_stub:
        if separator:
            title = title_stub+separator+h1.string
        else:
            title = title_stub+': '+h1.string
    elif h1 and not title_stub:
        title = h1.string
    elif title_stub and not h1:
        title = title_stub
    else:
        title = 'Title'
    return title


def get_files_by_type(filetype,directory):
    return [f for f in listdir(directory) if isfile(join(directory, f)) and f.endswith("." + filetype)]


def handle_md():
    files = get_files_by_type('md', 'Pages/')
    for page in files:
        pageFilename = join('./Pages', page)
        md_source = open(pageFilename, 'r').read()
        html = md.markdown(md_source)
        title = get_title(html)
        write_output(page, html, title)


def handle_html():
    files = get_files_by_type('html', 'Pages/')
    for page in files:
        inputFilename = join('./Pages', page)
        sourceHTML = open(inputFilename, 'r').read()
        title = get_title(sourceHTML)
        write_output(page, sourceHTML, title)


def set_title(title,file):
    upper = open('Template_Upper.html', 'r').read()
    soup = BeautifulSoup(upper, 'lxml')
    title_element = soup.title
    title_element.string.replace_with(title)
    return str(soup)


def set_titles(files):
    for file in files:
        with open(file, 'r+') as page:
            markup = page.read()
            soup = BeautifulSoup(markup, 'lxml')
            title_element = soup.title
            title = get_title(markup)
            title_element.string.replace_with(title)
            page.seek(0)
            page.write(str(soup))
            page.truncate()
            page.close()


def write_output(page, content, title):
    outputFilename = join('./Output', str(path.splitext(page)[0]) + '.html')
    print("Now writing " + outputFilename + " from " + page)
    upper = open('Template_Upper.html', 'r')
    lower = open('Template_Lower.html', 'r')

    with open(outputFilename, 'w+') as output:
        for line in upper:
            output.write(line)
        for line in content:
            output.write(line)
        for line in lower:
            output.write(line)

    files_written.append(outputFilename)
    lower.close()
    output.close()


files_written = []
config = get_config()
handle_html()
handle_md()
set_titles(files_written)






