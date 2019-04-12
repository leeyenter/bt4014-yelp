import React, { Component } from "react";
import {
    Form,
    Input,
    Select,
    Button,
    Segment,
    Loader,
    Dimmer,
    SegmentGroup,
    Statistic,
    Table,
    Grid,
    Accordion,
    Icon
} from "semantic-ui-react";
import {
    valueCounts,
    parseValueCounts,
    sentimentColours,
    generateChartData
} from "../utils";

import { Bar, Line } from "react-chartjs-2";
import Map from "./Map";
import { SentimentBar } from "../charts";

const math = require("mathjs");
const _ = require("lodash");

const bizOptions = [
    { key: "1", text: "Shake Shack", value: "shake-shack" },
    { key: "2", text: "In-N-Out Burger", value: "in-n-out" },
    { key: "3", text: "The Cheesecake Factory", value: "cheesecake" }
];

interface Record {
    phrase: string;
    count: number;
    score: number;
    sentiments: number[];
    locations: string[];
}

interface State {
    query: string;
    biz: string;
    loading: boolean;

    activeIndex: number;
    numReviews: number;
    results: Record[];
    locationSentiments: any;
    info: any;
}

class BusinessPage extends Component<{}, State> {
    constructor(props: {}) {
        super(props);
        this.state = {
            query: "",
            biz: bizOptions[0].value,
            loading: false,

            activeIndex: 0,
            numReviews: 0, 
            results: [],
            locationSentiments: {},
            info: []
        };

        // this.doSearch();
    }

    doSearch = () => {
        this.setState({ loading: true });
        fetch("/backend/business/" + this.state.biz + "/" + this.state.query)
            .then((resp: any) => {
                return resp.json();
            })
            .then((json: any) => {
                console.log(json);
                this.setState({
                    numReviews: json.num_reviews, 
                    results: json.results,
                    locationSentiments: json.location_sentiments,
                    info: json.info,
                    loading: false
                });
            });
    };

    handleChange = (e: any, param: any) => {
        const { name, value } = param;
        switch (name) {
            case "query":
                this.setState({ query: value });
                break;
            case "biz":
                this.setState({ biz: value });
                break;
        }
    };

    handleAccordionChange = (e: any, titleProps: any) => {
        const { index } = titleProps;
        const { activeIndex } = this.state;
        const newIndex = activeIndex === index ? -1 : index;

        this.setState({ activeIndex: newIndex });
    };

    render() {
        return (
            <div>
                <Segment>
                    <Dimmer active={this.state.loading} inverted>
                        <Loader />
                    </Dimmer>
                    <Form onSubmit={this.doSearch}>
                        <Form.Group widths="equal">
                            <Form.Field
                                control={Input}
                                name="query"
                                value={this.state.query}
                                onChange={this.handleChange}
                                label="Search Term"
                            />
                            <Form.Field
                                control={Select}
                                label="Business"
                                options={bizOptions}
                                name="biz"
                                value={this.state.biz}
                                onChange={this.handleChange}
                            />
                        </Form.Group>
                        <Form.Field control={Button}>Search</Form.Field>
                    </Form>
                </Segment>
                {this.state.results.length > 0 && (
                    <Results
                        {...this.state}
                        handleAccordionChange={this.handleAccordionChange}
                    />
                )}
            </div>
        );
    }
}

export interface ResultsProps {
    numReviews: number;
    results: Record[];
    locationSentiments: any;
    info: any;
    activeIndex: number;
    handleAccordionChange: any;
}

class Results extends Component<ResultsProps> {
    render() {
        return (
            <div>
                <Segment>
                    <Statistic>
                        <Statistic.Value>
                            {Object.keys(this.props.locationSentiments).length}
                        </Statistic.Value>
                        <Statistic.Label>Branches</Statistic.Label>
                    </Statistic>

                    <Statistic>
                        <Statistic.Value>
                            {this.props.numReviews}
                        </Statistic.Value>
                        <Statistic.Label>Reviews</Statistic.Label>
                    </Statistic>

                    <Statistic>
                        <Statistic.Value>
                            {this.props.results.length}
                        </Statistic.Value>
                        <Statistic.Label>Phrases Found</Statistic.Label>
                    </Statistic>
                </Segment>
                <Segment>
                    <Map
                        {...this.props}
                        googleMapURL="https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places&key=AIzaSyBknhTH5oSCrZD27utNlpzEAzk-dFopNwQ"
                        loadingElement={<div style={{ height: `100%` }} />}
                        containerElement={<div style={{ height: `400px` }} />}
                        mapElement={<div style={{ height: `100%` }} />}
                    />
                </Segment>
                <Accordion fluid styled>
                    <LocationSentiments {...this.props} />
                    <ResultsTable {...this.props} />
                </Accordion>
            </div>
        );
    }
}

class LocationSentiments extends Component<ResultsProps> {
    render() {
        let locationSentiments = [];
        for (let location in this.props.locationSentiments) {
            
            locationSentiments.push(
                <Grid.Column key={location}>
                    <h3>{location}</h3>
                    <SentimentBar data={this.props.locationSentiments[location].values} />
                </Grid.Column>
            );
        }
        return (
            <div>
                <Accordion.Title
                    active={this.props.activeIndex == 1}
                    index={1}
                    onClick={this.props.handleAccordionChange}
                >
                    <Icon name="dropdown" />
                    Distribution of Sentiment For Each Branch
                </Accordion.Title>
                <Accordion.Content active={this.props.activeIndex == 1}>
                    <Grid columns={3}>{locationSentiments}</Grid>
                </Accordion.Content>
            </div>
        );
    }
}

class ResultsTable extends Component<ResultsProps> {
    render() {
        let tblRows = [];

        for (let i = 0; i < this.props.results.length; i++) {
            let row = this.props.results[i];
            let locations = parseValueCounts(valueCounts(row.locations));
            tblRows.push(
                <Table.Row key={i}>
                    <Table.Cell>{row.phrase}</Table.Cell>
                    <Table.Cell>{row.count}</Table.Cell>
                    <Table.Cell className="chart-cell">
                        {math.mean(row.sentiments).toFixed(2)} (std:{" "}
                        {math.std(row.sentiments).toFixed(2)})<br />
                        <SentimentBar data={generateChartData(row.sentiments)} />
                    </Table.Cell>
                    <Table.Cell>{locations}</Table.Cell>
                </Table.Row>
            );
        }

        return (
            <div>
                <Accordion.Title
                    active={this.props.activeIndex == 2}
                    index={2}
                    onClick={this.props.handleAccordionChange}
                >
                    <Icon name="dropdown" />
                    List of Phrases Found
                </Accordion.Title>
                <Accordion.Content active={this.props.activeIndex == 2}>
                    <Table celled>
                        <Table.Header>
                            <Table.Row>
                                <Table.HeaderCell>Phrase</Table.HeaderCell>
                                <Table.HeaderCell>Count</Table.HeaderCell>
                                <Table.HeaderCell>Sentiment</Table.HeaderCell>
                                <Table.HeaderCell>Locations</Table.HeaderCell>
                            </Table.Row>
                        </Table.Header>

                        <Table.Body>{tblRows}</Table.Body>
                    </Table>
                </Accordion.Content>
            </div>
        );
    }
}

export default BusinessPage;
