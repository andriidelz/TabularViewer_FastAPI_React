import React, { useState } from "react";

function App() {
    const [file, setFile] = useState(null);
    const [tableData, setTableData] = useState(null);

    const apiUrl = process.env.REACT_APP_API_URL;

    const uploadFile = async () => {
        if (!file) {
            alert("Будь ласка, оберіть файл!");
            return;
        }
        
        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch(apiUrl, {
                method: "POST",
                body: formData,
            });
    
            const data = await response.json();
    
            if (!response.ok) {
                alert(data.error || "Помилка під час завантаження");
                return;
            }
    
            setTableData(data);
        } catch (error) {
            alert("Сервер недоступний");
        }
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
