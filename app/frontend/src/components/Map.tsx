import React, { Component } from "react";
import {
    GoogleMap,
    Marker,
    withGoogleMap,
    withScriptjs
} from "react-google-maps";
import { ResultsProps } from "./BusinessPage";
import { Modal } from "semantic-ui-react";
import { SentimentBar } from "../charts";
import { generateChartData } from "../utils";

class Map extends Component<ResultsProps> {
    render() {
        let markers = [];
        let minLat, maxLat, minLng, maxLng: number;
        minLat = this.props.info[0].latitude;
        minLng = this.props.info[0].longitude;
        maxLat = this.props.info[0].latitude;
        maxLng = this.props.info[0].longitude;
        for (let i = 0; i < this.props.info.length; i++) {
            let marker = this.props.info[i];
            let location = marker["address"] + ", " + marker["city"];
            let phrases = [];

            for (
                let result_i = 0;
                result_i < this.props.results.length;
                result_i++
            ) {
                let result = this.props.results[result_i];
                let sentiments: number[] = [];
                let phrase_set = {
                    phrase: result.phrase,
                    sentiments: sentiments
                };

                for (let j = 0; j < result.locations.length; j++) {
                    if (result.locations[j] == location) {
                        phrase_set.sentiments.push(result.sentiments[j]);
                    }
                }

                if (phrase_set.sentiments.length > 0) {
                    let chart = (
                        <div>
                            <h3>{phrase_set.phrase}</h3>
                            <SentimentBar
                                data={generateChartData(phrase_set.sentiments)}
                            />
                        </div>
                    );
                    phrases.push(chart);
                }
            }

            markers.push(
                <Modal
                    key={i}
                    size={"fullscreen"}
                    trigger={
                        <Marker
                            key={i}
                            position={{
                                lat: marker["latitude"],
                                lng: marker["longitude"]
                            }}
                        />
                    }
                >
                    <Modal.Header>{marker["address"]}</Modal.Header>
                    <Modal.Content image>
                        <div className="map-modal-body">
                            <div>
                                <h3>Overall Sentiments</h3>
                                <SentimentBar
                                    data={
                                        this.props.locationSentiments[location]
                                            .values
                                    }
                                />
                            </div>
                            {phrases}
                        </div>
                    </Modal.Content>
                </Modal>
            );

            if (minLat == null || marker["latitude"] < minLat) {
                minLat = marker["latitude"];
            }
            if (maxLat == null || marker["latitude"] > maxLat) {
                maxLat = marker["latitude"];
            }
            if (minLng == null || marker["longitude"] < minLng) {
                minLng = marker["longitude"];
            }
            if (maxLng == null || marker["longitude"] > maxLng) {
                maxLng = marker["longitude"];
            }
        }
        return (
            <GoogleMap
                defaultZoom={5}
                defaultCenter={{
                    lat: (minLat + maxLat) / 2,
                    lng: (minLng + maxLng) / 2
                }}
            >
                {markers}
            </GoogleMap>
        );
    }
}

export default withScriptjs(withGoogleMap(Map));
