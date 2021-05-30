import React from 'react';

function ResultsDisplay(props) {

    var searchResults = props.data
    if (searchResults === undefined) {
        searchResults = []
    }

    const results = []
    for (let website of searchResults) {
        results.push(<p>{website.title} <a href={website.link}>link</a></p>);
    }

    return (<div>
        <h2>Found {results.length} results</h2>
        {results}
    </div>)
}

export default ResultsDisplay