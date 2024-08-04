const express = require("express");
const { createServer } = require("http");
const app = express();
const session = require("express-session");
const httpServer = createServer(app);
const cors = require("cors");
const { join } = require("path");
const csurf = require("csurf");
require("dotenv").config();

// app.use(csurf())

app.set("view engine", "ejs");

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

app.use('/images', express.static(join(__dirname, "images")));

app.get('/game.js', (req, res) => {
  res.sendFile(join(__dirname, "./game.js"));
})

const authRoutes = require("./routes/auth.js");
app.use(authRoutes);

const profileRoutes = require("./routes/profile.js");
app.use(profileRoutes);

// const imageRoutes = require("./routes/images.js");
// app.use("/images", imageRoutes);

const io = require("./routes/sockets.js")(httpServer);

httpServer.listen(3000, () => {
  console.log("Listening on port 3000.");
});