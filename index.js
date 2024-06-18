const express = require("express");
const { createServer } = require("http");
const app = express();
const httpServer = createServer(app);
const cors = require("cors");

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const authRoutes = require("./routes/auth.js");
app.set("view engine", "ejs");
app.use("/auth", authRoutes);

const io = require("./routes/sockets.js")(httpServer);

httpServer.listen(3000, () => {
  console.log("Listening on port 3000.");
});
