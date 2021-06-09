# CS172 - Final Project

## Team members
- Van Truong (vtruo009)
- Mari Hayashi (mhaya010)
- Richard Duong (rduon008)

## How to run our program


## Collaboration Details


### Part 1 - Crawler
Overview of system, including (but not limited to)
(a) Architecture
(b) The Crawling or data collection strategy (do you handle duplicate URLs, is your crawler parallel, etc.)
(c) Data Structures employed
Limitations (if any) of the system.
Instruction on how to deploy the crawler. Ideally, you should include a crawler.bat (Windows) or crawler.sh (Unix/Linux) executable file that takes as input all necessary parameters. Example instructions for Web-based assignment: [user@server]./crawler.sh < seed − Fileseed.txt > < num − pages : 10000 > < hops − away : 6 > <output−dir >

### Part 2 - Indexer
Instructions on how to deploy the system. Ideally, you should include an indexer.bat (Windows) or indexer.sh (Unix/Linux) executable file that takes as input all necessary parameters .  Example: [user@server] ./indexer.sh < output − dir >

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
