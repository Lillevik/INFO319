import React, {Component} from 'react';
import './App.css';
import {init_socket, received_tweet} from './api'

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            'tweets': []
        };
        init_socket();
        received_tweet((tweet) => {
            console.log(tweet);
            this.setState({
                'tweets': [tweet, ...this.state.tweets.slice(0,48)]
            })
        });
    };

    render() {
        const {tweets} = this.state;
        return (
            <div className="App">
                <header className="App-header">
                    {tweets.map((tweet) => {
                        let words = [];
                        if (tweet.extended_tweet) {
                            words = tweet.extended_tweet.full_text.split(" ");
                        } else {
                            words = tweet.text.split(" ");
                        }
                        return (
                            <div key={tweet.id} className={"tweet-container fade-in"}>{
                                words.map((word) => {
                                    if (word.toLowerCase().includes('earthquake') || word.toLowerCase().includes('flood')) {
                                        return (<span className={"highlight"}>{word}&nbsp;</span>)
                                    } else if(word.startsWith('http')){
                                        return (<a href={word}>{word}</a>)
                                    } else {
                                        return (<>{word}&nbsp;</>);
                                    }
                                })}
                            </div>
                        )
                    })}
                </header>
            </div>
        );
    }
}

export default App;
