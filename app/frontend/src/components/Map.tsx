import React, {Component} from 'react';
import { GoogleMap, Marker, withGoogleMap, withScriptjs } from "react-google-maps";
import { ResultsProps } from './BusinessPage';

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
            markers.push(<Marker key={i} position={{lat: marker['latitude'], lng: marker['longitude']}} />)

            if (minLat == null || marker['latitude'] < minLat) {
                minLat = marker['latitude']
            }
            if (maxLat == null || marker['latitude'] > maxLat) {
                maxLat = marker['latitude']
            }
            if (minLng == null || marker['longitude'] < minLng) {
                minLng = marker['longitude']
            }
            if (maxLng == null || marker['longitude'] > maxLng) {
                maxLng = marker['longitude']
            }
        }
        return (
            <GoogleMap
                defaultZoom={5}
                defaultCenter={{lat: (minLat + maxLat) / 2, lng: (minLng + maxLng) / 2}}
            >
                {markers}
            </GoogleMap>
        );
    }
}

export default withScriptjs(withGoogleMap(Map))