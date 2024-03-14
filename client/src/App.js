import React from "react";
import DataTable from "./Components/DataTable/DataTable";
import FileUploader from "./Components/FileUploader/FileUploader";
import "bootstrap/dist/css/bootstrap.min.css";

const App = () => {
	return (
		<div>
			<h1>Genome Calculator</h1>
			<FileUploader />
			<DataTable />
		</div>
	);
};

export default App;
