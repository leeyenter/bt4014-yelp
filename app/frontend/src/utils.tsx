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
