const express = require("express");
const util = require('util');

const PORT = process.env.PORT || 3001;

const app = express();

function GetQuery(query_string) {
    return util.format('{"query": {"match": {"body": "%s"} }}', query_string)
}

// Run the command and return stdout
async function RunCommand(command) {
    const { exec } = require("child_process");
    const { stdout, stderr, error } = await exec(command);
    // if (stderr) { console.error('stderr:', stderr); }
    // if (error) { console.error('error:', error.message); }
    var result = '';
    for await (const data of stdout) {
        result += data.toString()
    };
    return result
}

async function ElasticSearch(query_string) {
    const search_result = {
        retrieved_sites: undefined,
        error_message: ''
    }

    const command = util.format('echo %s > query.txt', GetQuery(query_string))
    await RunCommand(command)

    const elastic_search_command = 'curl -X GET -u elastic:WLBCezXn0g7t6xNdzPclj0ke "https://cs172-vrm.es.us-west1.gcp.cloud.es.io:9243/my-first-index/_search?pretty" -H "Content-Type: application/json" -d @query.txt'
    try {
        const search_stdout = await RunCommand(elastic_search_command)
        const search_results = JSON.parse(search_stdout)
        var retrieved_sites = []
        const sites = search_results.hits.hits
        sites.forEach(site => {
            if (site._source.title !== undefined && site._source.link !== undefined) {
                const website = {
                    title: site._source.title,
                    link: site._source.link,
                    score: site._score
                }
                retrieved_sites.push(website)
            }
        });
        search_result.retrieved_sites = retrieved_sites
        return search_result
    } catch (err) {
        console.error(err)
        search_result.error_message = err.toString()
        return search_result
    }
}

app.get("/search", async (req, res) => {
    var query_string = req.query.query_string || "";

    const { retrieved_sites, error_message } = await ElasticSearch(query_string);

    if (retrieved_sites === undefined) {
        res.json({ error_message: error_message })
    } else {
        res.json({ retrieved_sites: retrieved_sites })
    }
});

app.listen(PORT, () => {
    console.log(`Server listening on ${PORT}`);
});