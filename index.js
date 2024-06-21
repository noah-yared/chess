const express = require("express");
const { createServer } = require("http");
const app = express();
const session = require("express-session");
const httpServer = createServer(app);
const cors = require("cors");
const csurf = require("csurf");
require("dotenv").config();

// app.use(csurf())
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(
  session({
    secret: process.env.SECRET_KEY,
    cookie: {httpOnly: true},
    resave: false,
    saveUninitialized: false
  })
);

const authRoutes = require("./routes/auth.js");
app.set("view engine", "ejs");
app.use(authRoutes);

const io = require("./routes/sockets.js")(httpServer);

httpServer.listen(3000, () => {
  console.log("Listening on port 3000.");
});
