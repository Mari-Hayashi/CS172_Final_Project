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
            value: '',
            result: undefined,
            current_state: state.INITIAL
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    async CallSearch(query) {
        this.setState({ ...this.state, current_state: state.FETCHING })
        const url = "/search?query=" + query.value;
        const response = await fetch(url);
        const data = await response.json();
        this.setState({ ...this.state, result: data.results, current_state: state.FETCHED })
        console.log(data.results)
    }

    handleChange(event) {
        this.setState({ ...this.state, value: event.target.value });
    }

    handleSubmit(event) {
        const { value } = this.state;

        const query = { value }
        this.CallSearch(query)

        event.preventDefault()
    }

    getComponent() {
        switch (this.state.current_state) {
            case state.INITIAL:
                return '';
            case state.FETCHING:
                return 'Loading...';
            case state.FETCHED:
                return <ResultsDisplay data={this.state.result} />;
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
                <form onSubmit={this.handleSubmit}>
                    <label>
                        <input type="text" value={this.state.value} onChange={this.handleChange} style={searchBoxStyle}/>
                    </label>
                    <input type="submit" value="Search" style={searchButtonStyle} />
                </form>
                <br></br>
                <p>{this.getComponent()}</p>
            </div>
        );
    }
}

export default SearchForm