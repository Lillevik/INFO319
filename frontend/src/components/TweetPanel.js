import React, {Component} from 'react'


class TweetPanel extends Component {

    constructor(props) {
        super(props);
        this.state = {
            tweets: [{text: "abd 123 earthquake", id: 1, screen_name:"Marius Lillevik"}, {text: "abd 123", id: 2, screen_name:"Marius Lillevik"}, {text: "abd 123 flood", id: 3, screen_name:"Marius Lillevik"},{text: "abd 123 flood", id: 4, screen_name:"Marius Lillevik"},{text: "abd 123 flood", id: 5, screen_name:"Marius Lillevik"}]
        }
    }

    render_words(words, id) {
        let word_spans = [];
        for (let i = 0; i < words.length; i++) {
            let word = words[i];
            if (word.toLowerCase().includes('earthquake') || word.toLowerCase().includes('flood')) {
                word_spans.push(<span key={i} className={"highlight"}>{word}&nbsp;</span>)
            } else if (word.startsWith('http')) {
                word_spans.push(<a key={i} href={word}>{word}</a>)
            } else if(word.startsWith("@")){
                word_spans.push(<a key={i} href={"http://twitter.com/" + word}>{word}</a>)
            } else {
                word_spans.push(<span key={i}>{word}&nbsp;</span>);
            }
        }
        return (word_spans)
    };

    render_tweet = (tweet) =>  {
        let words = [];
        if (tweet.extended_text) {
            words = tweet.extended_text.full_text.split(" ");
        } else {
            words = tweet.text.split(" ")
        }
        this.render_words(words, tweet.id);
        return (
            <div className={"col-4 pr-2 pb-2"}>
                <div key={tweet.id} className={"shadow tweetContainer mt-3"}>
                    <div className={"tweetImg"}>
                        <img className={"shadow"} src={tweet.user.profile_image_url} alt={"Profile"}/>
                    </div>
                    <h4 className={"text-center p-2"}><a href={"https://twitter.com/" + tweet.user.screen_name}>@{tweet.user.screen_name}</a></h4>
                    <div className={"p-2"}>
                        <p className={"tweetText"}>{this.render_words(words, tweet.id)}</p>
                    </div>
                </div>
            </div>
        )
    };

    render_tweets = (tweets) => {
        let counter = 0;
        let rows = [];
        let row = [];
        for (let i = 0; i < tweets.length; i++){
            if(counter === 3){
                counter = 0;
                rows.push(row);
                row = [];
            }
            row.push(this.render_tweet(tweets[i]))
            counter ++;
            if(i === tweets.length){
                rows.push(row);
            }
        }
        return (
            <div className={"container-fluid"}>
                {rows.map((row) =>{
                    return (
                        <div className={"row"}>
                            {row}
                        </div>
                    )
                }
                )}
            </div>
        )
    };



    render() {
        const {tweets} = this.props;
        return (
            <div id={"tweetPanel"} className={this.props.className}>
                {this.render_tweets(tweets)}
            </div>
        )
    }
}

export {TweetPanel}