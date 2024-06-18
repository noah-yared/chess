const express = require("express");
const bcrypt = require("bcryptjs");
const router = express.Router();
const pool = require("../db.js");
const { join, resolve } = require("path");

router.post("/", (req, res) => {
  // console.log(req.body);
  if (req.body.register) {
    try {
      registerUser(req.body, res);
      res.sendFile(join(__dirname, "../homepage.html"));
    } catch (err) {
      console.error(err);
    }
  } else {
    try {
      authenticateUser(req.body, res);
      res.sendFile(join(__dirname, "../homepage.html"));
    } catch (err) {
      console.error(err);
    }
  }
})

const registerUser = async (loginInfo, response) => {
  try {  
    const username = loginInfo.username.trim();
    const password = loginInfo.password.trim();
    const salt = await bcrypt.genSalt();
    const hash = await bcrypt.hash(password, salt);
    const sql = 'INSERT INTO users(username, password) VALUES($1, $2)';
    await pool.query(sql, [username, hash]);
    response.send({message:"Successfully registered!"});
  } catch (err) {
    response.send({message:"Registration attempt failed."});
    throw err; // propagate error
  }
}

const authenticateUser = async (loginInfo, response) => {
  try {
    const username = loginInfo.username.trim();
    const password = loginInfo.password.trim();
    const sql = 'SELECT password FROM users WHERE username=$1';
    const res = await pool.query(sql, [username]);
    if (res.rows.length === 0) throw new Error("Invalid username");
    const validPassword = await bcrypt.compare(password, res.rows[0].password);
    if (!validPassword) throw new Error("Invalid password");
    response.send({message:"Successfully logged in!"});
  } catch (err) {
    response.send({message:"Login attempt failed."});
    throw err; // propagate error
  }
}


module.exports = router;
