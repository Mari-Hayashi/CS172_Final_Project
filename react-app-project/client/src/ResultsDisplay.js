import React from 'react';

function ResultsDisplay(props) {
    const { retrieved_sites, error_message } = props.data
    if (retrieved_sites === undefined) {
        return (<div>
            <h2>Search Unsuccessful: {error_message}</h2>
            <p>Try another query.</p>
        </div>)
    }

    const titleStyle = {
        color: "Aqua",
        fontFamily: "Arial",
        padding: "0px"
    };
    const linkStyle = {
        fontSize: 17
    }

    const site_list = []
    for (let site of retrieved_sites) {
        site_list.push(<div><div style={titleStyle}>{site.title}</div><a href={site.link} style={linkStyle}>{site.link}</a><br/>SCORE: {site.score}<br /><br /></div>);
    }

    return (<div>
        <h2>Found {site_list.length} results</h2>
        <div
            style={{
                textAlign: "left"
            }}
        >
            {site_list}</div>
    </div>)
}

export default ResultsDisplay