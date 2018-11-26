import React, {Component} from 'react';
import WordCloud from 'react-d3-cloud';


class WordcloudPanel extends Component {

    constructor() {
        super();
        this.state = {
            status: 'cloud'
        }
    }

    enableCloud = () => {
        this.setState({
            status: 'cloud'
        })
    }

    enableTable = () => {
        this.setState({
            status: 'table'
        })
    };

    renderWordClouds = () => {
        let fontSizeMapper = word => Math.log2(word.value) * 5;
        let rotate = word => word.value % 360;
        let height = (window.innerHeight / 2) - 50;
        let width = ((window.innerWidth / 12) * 4) - 8;
        if (window.innerWidth <= 792) {
            width = window.innerWidth - 10;
        }
        return (
            <div>
                <div className={"wordCloud shadow mt-3"}>
                    <WordCloud
                        data={this.props.wordCount}
                        fontSizeMapper={fontSizeMapper}
                        rotate={rotate}
                        width={width}
                        height={height}
                        padding={2}
                    />
                </div>
                <div className={"wordCloud shadow mt-3"}>
                    <WordCloud
                        data={this.props.hashtagCount}
                        fontSizeMapper={fontSizeMapper}
                        rotate={rotate}
                        width={width}
                        height={height}
                        padding={2}
                    />
                </div>
            </div>
        )
    };

    renderTable = () => {
        let wordPairs = this.props.wordCount.slice(0, 4);
        let hashtagPairs = this.props.hashtagCount.slice(0, 4);
        return (
            <div>
                <table className={"table table-striped countTable shadow mt-3"}>
                    <thead>
                        <th scope="col">Word</th>
                        <th scope="col">Count</th>
                    </thead>
                    <tbody>
                    {wordPairs.map((wordPair) => {
                        return (
                        <tr scope={"row"} key={wordPair.text}>
                            <td>{wordPair.text}</td>
                            <td>{wordPair.value}</td>
                        </tr>)
                    })}
                    </tbody>
                </table>

                <table className={"table table-striped countTable shadow mt-3"}>
                    <thead>
                        <th scope="col">Word</th>
                        <th scope="col">Count</th>
                    </thead>
                    <tbody>
                    {hashtagPairs.map((hashtagPair) => {
                        return (
                        <tr scope={"row"} key={hashtagPair.text}>
                            <td>{hashtagPair.text}</td>
                            <td>{hashtagPair.value}</td>
                        </tr>)
                    })}
                    </tbody>
                </table>
            </div>
        )
    };

    render() {


        return (
            <div className={this.props.className}>
                <div className={"wordCloudWrapper pt-1"}>

                    <ul className={"nav nav-tabs"}>
                        <li className={"nav-item"}>
                            <a className={"nav-link " + (this.state.status === 'cloud' ? 'active' : '')} href={"#"}
                               onClick={this.enableCloud}>Cloud</a>
                        </li>
                        <li className={"nav-item"}>
                            <a className={"nav-link " + (this.state.status === 'table' ? 'active' : '')} href={"#"}
                               onClick={this.enableTable}>Table</a>
                        </li>
                    </ul>
                    {this.state.status === 'cloud' ? this.renderWordClouds() : this.renderTable()}
                </div>
            </div>
        )
    }
}

export {WordcloudPanel}