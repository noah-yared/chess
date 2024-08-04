const express = require("express");
const router = express.Router();
const { join } = require("path");

router.get("/:image", (req, res) => {
  console.log(`Sending ${req.params.image} image over.`);
  res.sendFile(join(__dirname, `../images/${req.params.image}.png`));
})

module.exports = router;
