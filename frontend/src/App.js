import React, { useState } from "react";

function App() {
    const [file, setFile] = useState(null);
    const [tableData, setTableData] = useState(null);

    const uploadFile = async () => {
        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch("http://127.0.0.1:8000", {
            method: "POST",
            body: formData,
        });

        const data = await response.json();
        setTableData(data);
    };

    return (
        <div>
            <h2>📊 Табличний переглядач</h2>
            <input type="file" onChange={(e) => setFile(e.target.files[0])} />
            <button onClick={uploadFile}>Завантажити</button>

            {tableData && (
                <table border="1">
                    <thead>
                        <tr>
                            {tableData.columns.map((col, idx) => (
                                <th key={idx}>{col}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {tableData.data.map((row, idx) => (
                            <tr key={idx}>
                                {tableData.columns.map((col, colIdx) => (
                                    <td key={colIdx}>{row[col]}</td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}

export default App;
