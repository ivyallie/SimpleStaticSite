# SimpleStaticSite
A Python script that can compile HTML and MD files into a static HTML template.

# What it does, specifically
You provide content for webpages, and the script staples your HTML template onto it. Your template is divided into upper
and lower halves, which will be copied before and after your content, respectively. So everything that you want to remain
consistent in every page of your site needs to go in one of those template files. The content pages can be in HTML format,
or Markdown (.md) format. The title of the page will be grabbed from the first h1 element on the page.

# Setup
In the directory with the script, create two subdirectories: Pages and Output. In the Pages folder, you can put .html and .md 
files that have the content of your pages. In the same directory as the script, create two .html files, "Template_Upper.html" and 
"Template_Lower.html". The title element should be in Template_Upper. Now run the script, and it will take every .html and .md 
file from Pages/, merge them with the template pages, and write the results to Output/. Markdown will, of course, be converted to
HTML en route.

#Still to do
I'm sure more features will be added once I actually start using this.
