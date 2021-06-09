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
Overview of system, including (but not limited to)<br>
(a) Architecture:
```
Crawler3/                   # crawler package
    __init__.py
    Crawler3.py             # crawler core
    agents.txt              # list of agents for headers
    Helpers/                # helper modules
        FileHandler.py      # file helper - handles system directories / files
        TimeHandler.py      # timer helper - handles timers for verbose flag
        URLHandler.py       # url helper - simplifies urls
        RoboHandler.py      # robo helper - INCOMPLETE manages robots.txt
    Legacy/                 # legacy crawlers
        Crawler1/
        Crawler2/
```

Features - multithreading, argument parser, parallel thread for limits (depth, pages, size), handles url duplicates, random agent rotations, removes non-html extensions<br><br>
Limitations - no robots.txt, no identifying duplicate pages, may reach a crawling limit due to in-memory visited links, cannot identify some non-html pages<br><br>
Initial seeds are put into a queue with an initial depth of 0, and will be given to crawler threads. Crawler threads will first check if the given link is visited. If not, the crawling thread will identify neighboring links and add them to the queue with previous depth + 1. The crawling thread will then download the file, and encode the filename and store the encoding + the original url into a file for retrieval. This is because most operating systems have size limits to their filenames and urls can become very long. The crawlers will stop crawling when there are no more links in the queue, or the limits have been reached. A parallel limit thread will occasionally check if any limits have been surpassed, being the depth, download size, or page count. If any of these have been surpassed, then the parallel limit thread will signal to end all crawlers.<br>

(b) The Crawling or data collection strategy (do you handle duplicate URLs, is your crawler parallel, etc.):<br>
Our crawler is multithreaded and can handle threads based on cpu and I/O limitations of the computer running the crawler. We handle duplicate URLs by putting them in a visited set. With any of the data structures we use, we must apply blocking so that we don't get a race condition. Our queue, set, and decoding file has locks to ensure that no threads will write simultaneously.

(c) Data Structures employed:
- Locks (for all data structures)
- Links Queue (for next to visit)
- Visited Set (for urls already visited)
- Decoder File (to append decoding + url pairs)

#### Crawler Setup Instructions

1. Move to project directory
```
    cd CS172_Final_Project
```

2. Generate Virtual Environment
```
    chmod +x scripts/setup.sh
    ./scripts/setup/sh
```

3. Load Virtual Environment
```
    source env/bin/activate
```

4. You should be able to run the crawler now. (crawl.py)
<br><br>



#### How to run the crawler

1. To view the help (recommended)
```
    python crawl.py --help
```

2. To run the crawler on urls up to a depth of 3 (verbose)
```
    python crawler.py --url google.com bing.com yahoo.com -depth 3 -verbose
```

3. To run the crawler on a file of urls on 20 threads up to 10000 pages (verbose)
```
    python crawler.py --urlfile urls.txt -pages 10000 -threads 20 -verbose
```




### Part 2 - Indexer
The crawler gives us a zip folder containing HTML files. Our code in ```html_upload.py``` parses the HTML files and creates a "bulk document". This information is then used to perform a bulk upload to ElasticSearch with curl commands that we wrote into the code. Doing so allows us to parse the HtmL files, format the uploads, and perform a bulk upload all in one file.

Note: The HTML files in the zip file does not have a URL associated with it. What we did is we have a text file called ```filenames.txt```, which has mapping of the name of the HTML files to the link/URL. Our code references ```filenames.txt``` to get the link/URL for each HTML file.

Thus, to perform all of the steps mentioned above, we can run the command ```python html_upload.py <html_folder_name> filenames.txt <index_name>```.

### Part 3 - Extension
For an extension, we developed a web-based interface that allows user to enter the query and search for the documents that are relevant to the user query. I used React  to build the front-end components and Node.js to build the back-end component. Node.js communicate with the Elastic Search to get the results.

The ranked documents output from the Elastic Search is in a json format, so the users who are not familiar with json-format will have difficulty going through the results. Having web-based interface allows the users to see the ranked documents result in a formatted way and easily navigate through the results.

Also, during testing, we found that the operating system changes the format of the query string. What works on Windows fails on MacOS and vice versa. To address this issue, we added checks to determine the OS that the program is running on and return the correct format for the query string.

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
