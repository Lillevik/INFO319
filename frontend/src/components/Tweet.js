import React, {Component} from 'react'


class Tweet extends Component{

    constructor(props){
        super(props);
        this.state = {
            data:{}
        }
    }

    render(){
        return (
            <div className={"tweetContainer shadow"}>
                <img src={} />
            </div>
        )
    }
}

export {Tweet}