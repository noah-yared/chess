const express = require("express");
const router = express.Router();
const pool = require("../db.js");
const { join } = require("path");

router.get("/online-options", (req, res) => {
  verifySession(req)
  .then(() => res.sendFile(join(__dirname, "../online-options.html")))
  .catch(err => res.redirect("/login"));
})

router.get("/quick-match", (req, res) => {
  // verifySession(req)
  // .then(() => console.log("About to send the file"))
  // .then(() => res.sendFile(join(__dirname, "../quick-match.html")))
  // .catch(err => res.redirect("/login"));
  res.sendFile(join(__dirname, "../quick-match.html"));
})

router.get("/get-username", (req, res) => {
  // res.send("req.session.username");
  let randomNum = Math.random();
  let name = randomNum <= 0.33 ? 'playerA' : randomNum <= 0.66 ? 'playerB' : 'playerC';
  res.send(name);
})


const verifySession = async (request) => {
  try {
    let sql = 'SELECT user_id FROM sessions WHERE session_id=$1';
    const res = await pool.query(sql, [request.sessionID]);
    if (!res.rows.length) throw new Error("Session does not exist");
  } catch(err) {
    console.error(err);
    throw err;
  }
}

module.exports = router;