import React from 'react';
import ResultsDisplay from './ResultsDisplay.js'

const state = {
    INITIAL: 'initial',
    FETCHING: 'fetching',
    FETCHED: 'fetched',
}

class SearchForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            query_string: '',
            search_result: undefined,
            current_state: state.INITIAL
        };

        this.HandleChange = this.HandleChange.bind(this);
        this.HandleSubmit = this.HandleSubmit.bind(this);
    }

    async CallSearch(query_string) {
        this.setState({ ...this.state, current_state: state.FETCHING })
        const url = "/search?query_string=" + query_string;
        const response = await fetch(url);
        const search_result = await response.json();
        this.setState({ ...this.state, search_result: search_result, current_state: state.FETCHED })
    }

    HandleChange(event) {
        this.setState({ ...this.state, query_string: event.target.value });
    }

    HandleSubmit(event) {
        const { query_string } = this.state;
        this.CallSearch(query_string)
        event.preventDefault()
    }

    GetComponent() {
        switch (this.state.current_state) {
            case state.INITIAL:
                return '';
            case state.FETCHING:
                return 'Loading...';
            case state.FETCHED:
                return <ResultsDisplay data={this.state.search_result} />;
        }
    }

    render() {
        const searchButtonStyle = {
            color: "white",
            backgroundColor: "DodgerBlue",
            padding: "10px",
            fontFamily: "Arial"
        };
        const searchBoxStyle = {
            color: "DodgerBlue",
            backgroundColor: "white",
            padding: "10px",
            fontFamily: "Arial"
        };
        return (
            <div>
                <form onSubmit={this.HandleSubmit}>
                    <label>
                        <input type="text" value={this.state.query_string} onChange={this.HandleChange} style={searchBoxStyle}/>
                    </label>
                    <input type="submit" value="Search" style={searchButtonStyle} />
                </form>
                <br></br>
                <p>{this.GetComponent()}</p>
            </div>
        );
    }
}

export default SearchForm