import React, { Component } from "react";
import { Bar } from "react-chartjs-2";
import { sentimentColours } from "./utils";

export class SentimentBar extends Component<{data: any}> {
    render() {
        let data = this.props.data;
        let labels = [-1, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8]
        let chartData = {
            labels: labels,
            datasets: [
                {
                    data: data,
                    label: "No. of reviews",
                    backgroundColor: sentimentColours
                }
            ]
        };
        let options = {
            scales: {
                xAxes: [
                    {
                        categoryPercentage: 1.0,
                        barPercentage: 0.95
                    }
                ]
            }
        };

        return <Bar data={chartData} options={options} width={200} height={150} />;
    }
}
