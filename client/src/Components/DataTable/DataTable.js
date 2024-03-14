import React, { useState, useEffect } from "react";
import { Table } from "react-bootstrap";

const DataTable = () => {
	const [data, setData] = useState([]);

	useEffect(() => {
		// fetch("http://localhost:8000/predict")
		// 	.then((response) => response.json())
		// 	.then((data) => setData(data));

		const dataset = [
			{
				id: 1,
				cdsLength: 1213,
				gcPercent: 1010,
				enc: 121,
				gc1: 12,
				gc2: 5,
				gc3: 425,
			},
			{
				id: 2,
				cdsLength: 1213,
				gcPercent: 101,
				enc: 11,
				gc1: 12434,
				gc2: 57,
				gc3: 425,
			},
		];
		setData(dataset);
	}, []);

	return (
		<Table striped bordered hover>
			<thead>
				<tr>
					<th>CDS Length</th>
					<th>GC %</th>
					<th>ENC</th>
					<th>GC1</th>
					<th>GC2</th>
					<th>GC3</th>
				</tr>
			</thead>
			<tbody>
				{data.map((row) => (
					<tr key={row.id}>
						<td>{row.cdsLength}</td>
						<td>{row.gcPercent}</td>
						<td>{row.enc}</td>
						<td>{row.gc1}</td>
						<td>{row.gc2}</td>
						<td>{row.gc3}</td>
					</tr>
				))}
			</tbody>
		</Table>
	);
};

export default DataTable;
