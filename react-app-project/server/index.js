const express = require("express");

const PORT = process.env.PORT || 3001;

const app = express();

app.get("/api", (req, res) => {
    res.json({ message: "Hello from server!" });
});

app.get("/search", (req, res) => {
    var query = req.query.query || "";
    var results = []
    results.push({ title: "Site 1", link: "https://youtube.com" })
    results.push({ title: "Site 2", link: "https://youtube.com" })
    results.push({ title: "Site 3", link: "https://youtube.com" })

    res.json({ results: results });
});

app.listen(PORT, () => {
    console.log(`Server listening on ${PORT}`);
});