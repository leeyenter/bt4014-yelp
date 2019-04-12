import React from "react";
import { Table } from "semantic-ui-react";

let _ = require("lodash");

interface strMap {
    [key: string]: number;
}

export function valueCounts(values: string[]) {
    let results: strMap = {};
    for (let i = 0; i < values.length; i++) {
        let val = values[i];
        results[val] = results[val] ? results[val] + 1 : 1;
    }

    var sortable = [];
    for (var val in results) {
        sortable.push({key: val, value: results[val]});
    }

    return _.orderBy(sortable, ['value'], ['desc']);
}

export function parseValueCounts(valueCounts: any) {
    let counts = [];
    for (let i = 0; i < valueCounts.length; i++) {
        counts.push(
            <Table.Row key={i}>
                <Table.Cell>{valueCounts[i].key}</Table.Cell>
                <Table.Cell>{valueCounts[i].value}</Table.Cell>
            </Table.Row>
        );
    }
    return <Table compact><Table.Body>{counts}</Table.Body></Table>;
}

export const sentimentColours = [
    "#DE1724", 
    "#D93416", 
    "#D55D16", 
    "#D18516",
    "#CDAB15",
    "#C2C815",
    "#97C415",
    "#6EC014", 
    "#46BC14",
    "#20B814"
];

export function generateChartData(sentimentValues: number[]) {
    let counts = [0,0,0,0,0,0,0,0,0,0];
    for (let i = 0; i < sentimentValues.length; i++) {
        let index = Math.floor((sentimentValues[i] + 1) * 5);
        if (index == 10) {
            index = 9;
        }
        counts[index]++
    }
    return counts;

    return {
        labels: [-1, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8], 
        datasets: [{
            data: counts, 
            label: 'No. of phrases', 
            backgroundColor: sentimentColours
        }]
    }
}