import React from 'react';

function ResultsDisplay(props) {
    const { retrieved_sites, error_message } = props.data
    if (retrieved_sites === undefined) {
        return (<div>
            <h2>Search Unsuccessful: {error_message}</h2>
            <p>Try another query.</p>
        </div>)
    }

    const site_list = []
    for (let site of retrieved_sites) {
        site_list.push(<p>{site.title} <a href={site.link}>link</a> {site.score}</p>);
    }

    return (<div>
        <h2>Found {site_list.length} results</h2>
        {site_list}
    </div>)
}

export default ResultsDisplay