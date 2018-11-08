import React, {Component} from 'react';
import WordCloud from 'react-d3-cloud';


class WordcloudPanel extends Component {


    render() {
        let fontSizeMapper = word => Math.log2(word.value) * 5;
        let rotate = word => word.value % 360;
        let height = (window.innerHeight / 2) - 30;
        let width = ((window.innerWidth / 12) * 4) - 8;
        if(window.innerWidth <= 792){
            width = window.innerWidth - 10;
        }

        return (
            <div className={this.props.className}>
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
    }
}

export {WordcloudPanel}