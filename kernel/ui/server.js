const express = require('express');
const path = require('path');
const fs = require('fs');
const app = express();
const port = 8080;

app.use((req, res, next) => {
    console.log(`[REQUEST] ${req.method} ${req.url}`);
    next();
});

// הגדרה מפורשת של קבצי GLB
app.get('/mother_character.glb', (req, res) => {
    const filePath = path.join(__dirname, 'mother_character.glb');
    
    if (fs.existsSync(filePath)) {
        console.log(`[SUCCESS] Sending GLB file from: ${filePath}`);
        // הגדרת ה-Header הנכון כדי שהדפדפן במובייל לא יחסום את הקובץ
        res.setHeader('Content-Type', 'model/gltf-binary');
        res.sendFile(filePath);
    } else {
        console.log(`[ERROR] GLB file not found at: ${filePath}`);
        res.status(404).send('File not found');
    }
});

app.use(express.static(__dirname));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(port, '0.0.0.0', () => {
    console.log(`IMA Web UI is running with strict MIME-type handling!`);
});
