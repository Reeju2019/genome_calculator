import React, { useState } from "react";
import { Form, Button } from "react-bootstrap";

const FileUploader = () => {
	const [file, setFile] = useState(null);

	const handleChange = (event) => {
		setFile(event.target.files[0]);
	};

	const handleSubmit = async (event) => {
		event.preventDefault();

		if (file) {
			// Simulate uploading the file to the server
			const formData = new FormData();
			formData.append("file", file);

			// Replace with your actual upload logic
			const response = await fetch("http://8.8.8.8", {
				// const response = await fetch("http://localhost:8000/upload", {
				method: "POST",
				body: formData,
			});

			if (response.ok) {
				console.log("File uploaded successfully!");
			} else {
				console.error("Error uploading file");
			}
		}
	};

	return (
		<Form onSubmit={handleSubmit}>
			<Form.Group controlId="formFile" className="mb-3">
				<Form.Label>Upload file</Form.Label>
				<Form.Control type="file" onChange={handleChange} />
			</Form.Group>
			<Button variant="primary" type="submit">
				Submit
			</Button>
		</Form>
	);
};

export default FileUploader;
