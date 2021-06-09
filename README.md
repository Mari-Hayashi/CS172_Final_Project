# CS172 - Final Project

## Team members
- Van Truong (vtruo009)
- Mari Hayashi (mhaya010)
- Richard Duong (rduon008)

## Collaboration Details
Richard worked on Part 1.
Van and Mari worked on Part 2.
Mari worked on Part 3.

### Part 1 - Crawler
Overview of system, including (but not limited to)
(a) Architecture
(b) The Crawling or data collection strategy (do you handle duplicate URLs, is your crawler parallel, etc.)
(c) Data Structures employed
Limitations (if any) of the system.

#### Crawler Setup Instructions

1. Move to project directory
```
    cd CS172_Final_Project
```

2. Generate Virtual Environment
```
    chmod +x scripts/setup.sh
    scripts.setup.sh
```

3. Load Virtual Environment
```
    source env/bin/activate
```

4. You should be able to run the crawler now. (crawl.py)



#### How to run the crawler

1. To view the help (recommended)
```
    python crawl.py --help
```

2. To run the crawler on urls up to a depth of 3
```
    $ python crawler.py --url google.com bing.com yahoo.com -depth 3
```

3. To run the crawler on a file of urls on 10 threads up to 1000 pages
```
    $ python crawler.py --urlfile urls.txt -pages 10000 -threads 10
```

crawl.py --help

```
usage: crawl.py [-h] (--url URL [URL ...] | --urlfile [URLFILE])
                [--output OUTPUT] [--decoder DECODER] [-depth DEPTH]
                [-size SIZE] [-pages PAGES] [-threads [THREADS]]
                [-interval [INTERVAL]] [-verbose] [-clean]

Crawl websites and store html files locally

optional arguments:
  -h, --help            show this help message and exit

INPUTS:
  Set input urls

  --url URL [URL ...]   urls to scrape, use the --urlfile flag to load urls
                        from a file instead
  --urlfile [URLFILE]   input file with urls

OUTPUT:
  Set output names

  --output OUTPUT       output zipfile, default = htmls/
  --decoder DECODER     decoder of file names, default = filenames.txt

LIMITS:
  Set limits on crawling, default = 100 pages

  -depth DEPTH          depth of crawling
  -size SIZE            crawling size
  -pages PAGES          number of pages

SETTINGS:
  Set settings for crawler

  -threads [THREADS]    set number of threads, default = 1
  -interval [INTERVAL]  set crawling wait interval, default = 1
  -verbose              enable verbose actions, default = false
  -clean                clean old crawled data, default = false

Examples: 

    python crawl.py -h                                    ===>   Launch help page with all options
    python crawl.py --url google.com                      ===>   Crawl google.com with default depth 1
    python crawl.py --url google.com bing.com yahoo.com   ===>   Crawl multiple links
    python crawl.py --url google.com --verbose            ===>   Crawl google.com with verbose prints
    python crawl.py --urlfile urls.txt                    ===>   Crawl urls listed in urls.txt file
    python crawl.py --urlfile urls.txt -threads 5         ===>   Crawl urls.txt with 5 threads
```



Instruction on how to deploy the crawler. Ideally, you should include a crawler.bat (Windows) or crawler.sh (Unix/Linux) executable file that takes as input all necessary parameters. Example instructions for Web-based assignment: [user@server]./crawler.sh < seed − Fileseed.txt > < num − pages : 10000 > < hops − away : 6 > <output−dir >

### Part 2 - Indexer
Instructions on how to deploy the system. Ideally, you should include an indexer.bat (Windows) or indexer.sh (Unix/Linux) executable file that takes as input all necessary parameters .  Example: [user@server] ./indexer.sh < output − dir >
The crawler gives us a zip folder containing HTML files. Our code in ```html_upload.py``` parses the HTML files and creates a "bulk document". This information is then used to perform a bulk upload to ElasticSearch with curl commands that we wrote into the code. Doing so allows us to parse the HtmL files, format the uploads, and perform a bulk upload all in one file.

Note: The HTML files in the zip file does not have a URL associated with it. What we did is we have a text file called ```filenames.txt```, which has mapping of the name of the HTML files to the link/URL. Our code references ```filenames.txt``` to get the link/URL for each HTML file.

Thus, to perform all of the steps mentioned above, we can run the command ```python html_upload.py <html_folder_name> filesname.txt <index_name>```.

### Part 3 - Extension
For an extension, we developed a web-based interface that allows user to enter the query and search for the documents that are relevant to the user query. I used React  to build the front-end components and Node.js to build the back-end component. Node.js communicate with the Elastic Search to get the results.

The ranked documents output from the Elastic Search is in a json format, so the users who are not familiar with json-format will have difficulty going through the results. Having web-based interface allows the users to see the ranked documents result in a formatted way and easily navigate through the results.

#### Steps to view  the website

1. Run the following commands to install server dependencies and start the server program.
```
    cd react-app-project
    npm install
    npm start
```

2. In another command prompt window, run the following commands to install client dependencies and start the client program.

```
    cd react-app-project
    cd client
    npm install
    npm start
```
When the client side starts, the website opens in new window automatically.

![Alt Image text](/images/1.gif)
![Alt Image text](/images/1.png?raw=true)
![Alt Image text](/images/2.png?raw=true)
![Alt Image text](/images/3.png?raw=true)
