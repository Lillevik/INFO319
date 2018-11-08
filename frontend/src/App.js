import React, {Component} from 'react';

import './App.css';
import {WordcloudPanel} from "./components/WordcloudPanel";
import {TweetPanel} from "./components/TweetPanel";
import {init_socket, received_tweet, reveived_hashtag, reveived_wordcount} from './api'


class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            tweets: [],
            wordCount: [],
            hashtagCount: []

        };
        init_socket();

        received_tweet((tweet) => {
            this.setState({
               tweets:[tweet, ...this.state.tweets.slice(0,50)]
            });
        });

        reveived_wordcount((count) => {
            this.setState({
                wordCount: JSON.parse(count),
            });
        });

        reveived_hashtag((count) => {
            this.setState({
                hashtagCount: JSON.parse(count),
            });
        });
    }

    render() {

        return (
            <div className="App container-fluid">
                <div className={"row"}>
                    <TweetPanel
                        tweets={this.state.tweets}
                        className={"col-xs-12 col-sm-12 col-md-12 col-sm-12 col-lg-8"}
                    />
                    <WordcloudPanel
                        className={"col-xs-12 col-sm-12 col-md-12 col-sm-12 col-lg-4"}
                        wordCount={this.state.wordCount}
                        hashtagCount={this.state.hashtagCount}
                    />
                </div>
            </div>
        );
    }
}

export default App;
