const express = require("express");
// const bodyparser = require("body-parser");
const authRoutes = require("./routes/auth.js");
const { createServer } = require("http");
const { Server } = require("socket.io");
const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: {
    origin: "*"
  }
});

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.set("view engine", "ejs");

// app.post("/login", (req, res) => {
//   console.log(req.body);
//   res.send(req.body);
// })

app.use("/login", authRoutes);

io.on("connection", socket => {
  console.log(socket.id);
});

app.listen(3000, () => {
  console.log("Listening on port 3000.");
});