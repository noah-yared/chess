const express = require("express");
const crypto = require("crypto");
const bcrypt = require("bcrypt");
const router = express.Router();

router.post("/", (req, res) => {
  console.log(req.body);
  res.send("Request received!");
})

module.exports = router;