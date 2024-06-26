const express = require("express");
const bcrypt = require("bcryptjs");
const router = express.Router();
const pool = require("../db.js");
const { join, resolve } = require("path");

router.post("/auth", (req, res, next) => {
  console.log("POST /auth received", req.body);
  if (req.body.register) {
      registerUser(req)
      .then(() => storeSession(req))
      .then(() => next())
      // .then(() => {
      //   console.log("Registration successful!");
      //   res.sendFile(join(__dirname, "../homepage.html"))
      // })
      .catch(err => {
        console.log("Error with registration");
        res.sendFile(join(__dirname, "../register.html"));
      });
  } else {
      authenticateUser(req)
      .then(() => storeSession(req))
      .then(() => next())
      // .then(() => res.sendFile(join(__dirname, "../homepage.html")))
      .catch(err => {
        console.error(err);
        res.sendFile(join(__dirname, "../login.html"));
      });
  }
})

router.get("/homepage", (req, res, next) => {
  verifySession(req)
  .then(() => {
    console.log("sending file!");
    res.sendFile(join(__dirname, "../homepage.html"));
  })
  .catch(err => {
    console.error(err);
    /*res.sendFile(join(__dirname, "../login.html"));*/
    next();
  }); 
})

router.get("/login", (req, res) => {
  res.sendFile(join(__dirname, "../login.html"));
})

const registerUser = async (request) => {
  try {
    const loginInfo = request.body;
    const username = loginInfo.username.trim();
    const password = loginInfo.password.trim();
    const salt = await bcrypt.genSalt();
    const hash = await bcrypt.hash(password, salt);
    const sql = 'INSERT INTO users(username, password) VALUES($1, $2)';
    await pool.query(sql, [username, hash]);
    request.session.username = username; // store username in session with 'username' attribute
  } catch (err) {
    throw err; // propagate error
  }
}

const authenticateUser = async (request) => {
  try {
    const loginInfo = request.body;
    const username = loginInfo.username.trim();
    const password = loginInfo.password.trim();
    const sql = 'SELECT password FROM users WHERE username=$1';
    const res = await pool.query(sql, [username]);
    if (res.rows.length === 0) throw new Error("Invalid username");
    const validPassword = await bcrypt.compare(password, res.rows[0].password);
    if (!validPassword) throw new Error("Invalid password");
    request.session.username = username; // store username in session with 'username' attribute
  } catch (err) {
    throw err; // propagate error
  }
}

const storeSession = async (request) => {
  console.log(request.session); // see what session attribute looks like
  console.log(request.sessionID); // log unique session id
  try {  
    let sql = 'SELECT id FROM users WHERE username=$1';
    const res = await pool.query(sql, [request.session.username]);
    if (!res.rows.length) throw new Error("Username does not exist in db");
    const user_id = res.rows[0].id;
    sql = 'INSERT INTO sessions(session_id, user_id) VALUES($1, $2)';
    await pool.query(sql, [request.sessionID, user_id]);
  } catch (err) {
    console.error(err);
    throw err;
  }
};

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
