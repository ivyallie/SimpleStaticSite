# SimpleStaticSite
A Python script that can compile HTML and MD files into a static HTML template.

## What it does, specifically
You provide HTML snippets forming a template, and content for webpages, and the script staples your content into the template. 
You can set up as many different template structures as you like, and the script will follow your instructions to concatenate
them into HTML pags. The content pages can be in HTML format,
or Markdown (.md) format.

## Setup
In the directory with the script, create three subdirectories: Pages, Templates, and Output. In the Pages folder, you can put .html and .md 
files that have the content of your pages. In the Templates folder, place HTML files that will provide the generic components of your pages.
The resulting HTML pages will be copied to the Output folder.

## Configuration options
If you add a .yaml file to the directory where the script is, you can take advantage of some configuration options. At the moment, these are:
- title: The title stub, which will be added to the beginning of all page titles
- separator: A string placed between the title stub and the rest of the title
- structures: Strings defining the various structures the site uses
- extra_dirs: Extra directories to be copied to Output (things like images, scripts, etc.)

## Pages
The content of your pages is placed in HTML and MD files in the Pages folder. Each page can be supplemented with metadata in YAML format
at the top of the document. This section must begin and end with `---`. For example:
```
---
structure: minimal
title: "Foo"
---
```
This will cause the page to be rendered with a structure called **minimal** (which must be defined in your config.yaml file), with the title
**Foo**. **structure** can also be a valid structure definition string (see below).

## Structure strings
Every structure is defined as a string, with various files and snippets conjoined with + signs. For example:
```
default: "Template_Upper.html + <div class='textframe'> + <h1>{{title}}</h1> + content + </div> + Template_Lower.html"
```

This definition states that a page using the **default** structure will first grab the content of the file Templates/Template_Upper.html,
then create two elements, a div and an h1, then the page's content, then close the div, and finally Template_Lower.html.

The types of structure components are:
- Components ending in .html will be matched to files in the Templates directory
- HTML snippets (must start with `<`)
- The word `content` is reserved and indicates where to place the content of the page.

The config.yaml file can contain as many different structure definitions as you like, in the **structures** dictionary, but 
it must contain one named **default**, to be used whenever a page does not otherwise specify its structure.

## Substitution strings
Within your content or structures, you can use double curly brackets to insert variables from a page's metadata into the page's source.
For example, `{{title}}` will be replaced with the page's title at build time.

## Extra dirs
The extra_dirs dictionary in the config file contains key-value pairs that represent source folders and their corresponding destinations
in your Output folder. So a pair like `assets/images: images` will copy the dir `assets/images` (relative to CWD) to `Output/images`.

## Previewing your webpage
I suggest using the Python http server to see what your page will look like before you upload it to the web. CD into the output
folder and run `python -m http.server` to serve the contents. Press Ctrl+C to stop serving.


## Still to do
I'm sure more features will be added once I actually start using this.
