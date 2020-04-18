import React, {Component} from 'react';

import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import {Button, Col, Form, Toast} from "react-bootstrap";

class SignUp extends Component {
    constructor(props) {
        super(props);
        this.signUp = this.signUp.bind(this);
        this.state = {
            ans: "",
            code: null,
            showA: false,
            message: "",
            redirectVar: false,
            test: false,
            isAddressCorrect: null,
            isAddressCorrectMessage: null
        }
    }

    toggleShowA = () => this.setState({showA: !this.state.showA})

    signUp = (e) => {
        e.preventDefault();

        const data = {};
        for (let i = 0; i < e.target.length; i++) {
            if (e.target[i].id !== "") {
                data[e.target[i].id] = e.target[i].value;

            }
        }

        console.log(data)

        //axios.post("http://ec2-user@ec2-34-217-19-29.us-west-2.compute.amazonaws.com:8080", data)
        axios.post("http://localhost:7070", data)
            .then((response) => {
                console.log("response from Python")
                console.log(response.data)
                const code = response.data.code
                const message = response.data.message
                if (code !== "200") {
                    this.setState({ans: "", code: code, message: message, showA: true})
                } else {
                    this.setState({ans: response.data.ans, showA: false})
                }
            }).catch((err) => {
                console.log("In catch")
                console.log(err)
            })
    };

    nl2br(str, is_xhtml) {
        var breakTag = (is_xhtml || typeof is_xhtml === 'undefined') ? '<br />' : '<br>';
        return (str + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1' + breakTag + '$2');
    }


    render() {
        return (
            <div style={styles.container}>
                <h3 style={styles.message}>Vini Aswal - Python Finance Info HW</h3>
                {this.state.code !== null &&
                    <Toast show={this.state.showA} onClose={this.toggleShowA}>
                        <Toast.Header>
                            <img src="holder.js/20x20?text=%20" className="rounded mr-2" alt="" />
                            <strong className="mr-auto">Error</strong>
                        </Toast.Header>
                        <Toast.Body>{this.state.message}</Toast.Body>
                    </Toast>}

                <Form onSubmit={this.signUp}>
                    <Form.Row>
                        <Form.Group as={Col} controlId="ticker">
                            <Form.Label>Ticker Symbol</Form.Label>
                            <Form.Control placeholder="Ticker Symbol" required/>
                        </Form.Group>
                    </Form.Row>

                    <Button style={styles.signUpButton1} variant="primary" type="submit">
                        Fetch
                    </Button>
                </Form>

                <td dangerouslySetInnerHTML={{__html: this.nl2br(this.state.ans)}}/>
            </div>
        );
    }
}

const styles = {
    container: {
        display: "flex",
        alignItems: "center",
        flexDirection: "column",
    },
    message: {
        fontWeight: "bold",
        paddingTop: "2rem"
    },
    email: {
        width: "30rem",
    },
    signUpButton1: {
        width: "10rem",
        backgroundColor: "#2F99EA",

    },
};

export default SignUp;


