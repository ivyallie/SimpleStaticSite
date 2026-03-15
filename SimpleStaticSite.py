#!/usr/bin/python
# SimpleStaticSite by Ivy Lynn Allie
# ivyallie.com
# MIT License. Do as you will, at your own risk.

import os
from os.path import isfile, join
from bs4 import BeautifulSoup
import yaml
import markdown as md
from io import StringIO
import pdb
import shutil
import re

def get_config():
    yaml_files = get_files_by_type('yaml', './')
    print(yaml_files)
    if yaml_files:
        file = yaml_files[0]
        print("Found config file",file)
        with open(file, 'r') as configfile:
            config = yaml.safe_load(configfile)
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

def assign_ids_to_headings(html):
    soup = BeautifulSoup(html, 'html.parser')
    heading_tags = ['h1','h2','h3','h4']
    ids = []
    for i, header in enumerate(soup.find_all(heading_tags)):
        id = header.decode_contents().replace(' ','_')
        if id in ids:
            id = f'{id}_{i}'
        ids.append(id)
        header['id']=id
    return(soup.prettify())

def get_files_by_type(filetype,directory):
    return [f for f in os.listdir(directory) if isfile(join(directory, f)) and f.endswith("." + filetype)]

def extract_metadata(filepath):
    product = {
        'meta': {},
        'content': ''
    }
    with open(filepath, 'r',) as file:
        scope = file.read()
        if scope.startswith('---'):
            end_index = scope.find('---',3)
            if end_index != -1:
                raw_metadata = scope[3:end_index].strip()
                metadata = yaml.safe_load(raw_metadata)
                content = scope[end_index+3:].strip()
                product['meta'] = metadata
                product['content'] = content
                return product
            else:
                raise ValueError(f'Metadata block malformed in {filepath}')
        else:
            product['content'] = scope
            return product

def get_structure(structurename):
    try:
        structure = config['structures'][structurename]
    except KeyError:
        print(f'Structure definition {structurename} not found, defaulting.')
        structure = config['structures']['default']
    return process_structure(structure)
    

def process_structure(structuredef):
    structure_list = structuredef.split('+')
    return [f.strip() for f in structure_list]
   

def process_source(directory):
    files = [f for f in os.listdir(directory) if isfile(join(directory, f)) and os.path.splitext(f)[1] in ['.html','.md']]
    for f in files:
        print(f)
        fsplit = os.path.splitext(f)    
        extension = fsplit[1]
        path = os.path.join(directory,f)
        initial = extract_metadata(path)
        title_stub = get_option('title', config)
        separator = get_option('separator', config)
        if extension == '.html':
            html = initial['content']
        else:
            html = md.markdown(initial['content'], extensions=['def_list'])
            html = assign_ids_to_headings(html)
        if 'title' in initial['meta']:
            title = f"{initial['meta']['title']}{separator}{title_stub}"
        else:
            title = title_stub
            
        if 'structure' in initial['meta']:
            if '+' in initial['meta']['structure']: #If there's a + then we know this is a per-page structure definition
                structure = process_structure(initial['meta']['structure'])
            else:
                structure = get_structure(initial['meta']['structure'])
        else:
            structure = default_structure

        if 'url' in initial['meta']:
            raw_url = os.path.normpath(initial['meta']['url'])
            if raw_url.startswith('/'):
                raw_url = '.'+raw_url #otherwise os.path gets confused and thinks we're talking about local root
            url = os.path.join('Output',raw_url,'index.html')
        else:
            url = os.path.join('Output',fsplit[0],'index.html')


        content_soup = BeautifulSoup(html, 'html.parser')
        textbox = StringIO()
        for s in structure:
            if s == "content":
                #soup.append(content_soup)
                for line in html:
                    textbox.write(line)
            elif s.startswith("<"):
                textbox.write(s)
            else:
                filepath = os.path.join(templates,s)
                with open(filepath, 'r') as f:
                    #soup2 = BeautifulSoup(f.read(), 'html.parser')
                    #soup.append(soup2)
                    for line in f:
                        textbox.write(line)

        text_with_substitutions = StringIO()

        textbox.seek(0)
        for line in textbox:
            substituables = re.findall(r"\{\{(.*?)\}\}", line)
            if substituables:
                for s in substituables:
                    try:
                        sub = initial['meta'][s]
                    except KeyError:
                        print('Substitution tag without a corresponding value:',s)
                        continue
                    tagstring = r'{{'+s+r'}}'
                    line = line.replace(tagstring,sub)
                    #breakpoint()
                text_with_substitutions.write(line)
            else:
                text_with_substitutions.write(line)

        soup = BeautifulSoup(text_with_substitutions.getvalue(), 'html.parser')
        title_element = soup.title
        title_element.string.replace_with(title)
        path_root = os.path.split(url)[0]
        if not os.path.exists(path_root):
            os.makedirs(path_root)
        with open(url, 'w') as o:
            o.write(str(soup.prettify()))
        #write_output(f,html,title)

def set_title(title,file):
    upper = open('Template_Upper.html', 'r').read()
    soup = BeautifulSoup(upper, 'lxml')
    title_element = soup.title
    title_element.string.replace_with(title)
    return str(soup)


def set_titles(files):
    for file in files:
        if file != './Output/index.html': #Don't add redundant text to main page title
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
    filename=str(os.path.splitext(page)[0])
    if not filename=='index':
        output_path = join('.','Output',filename)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
    else:
        output_path = join('.','Output')
    outputFilename = join(output_path,'index.html')
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


def refresh_extra_directories(source_dir,output_dir):
    print('Extra dir copy:',source_dir,'to',output_dir)
    dest = os.path.join('Output',output_dir)
    shutil.copytree(source_dir,dest,dirs_exist_ok=True)

def validate_conf(config):
    missing = []

    def check_var(name):
        try: config[name]
        except KeyError:
            missing.append(name)
    
    for n in ['title','structures']:
        check_var(n)

    if not missing:

        try:
            config['structures']['default']
        except KeyError:
            print('Config file is missing a default structure definition.')
            quit()

        return
    else:
        print('Config file is missing the following mandatory definitions:')
        for n in missing:
            print(n)
        quit()

   

files_written = []
templates = 'Templates/'
config = get_config()
validate_conf(config)
default_structure = get_structure('default')
process_source('Pages/')
extra_dirs = config.get('extra_dirs')
if extra_dirs:
    for key,value in extra_dirs.items():
        refresh_extra_directories(key,value)






