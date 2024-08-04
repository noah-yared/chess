const pool = require("./db.js");

function stringifyMoves(moves) {
  return moves.join();
}

async function getUserId(username) {
  try {
    let sql = 'SELECT id from Users WHERE username=$1';
    const res = await pool.query(sql, [username]);
    if (!res.rows.length) throw new Error("username does not exist in database");
    return res.rows[0].id;
  } catch (err) {
    console.error(err);
    throw err;
  }
}

export async function loadSavedGameData(white, black) {
  try {
    const whiteId = await getUserId(white);
    const blackId = await getUserId(black);
    let sql = 'SELECT moves FROM active_games WHERE white=$1 AND black=$1';
    const res = await pool.query(sql, [whiteId, blackId]);
    return res.rows.length ? res.rows[0].moves : "";
  } catch (err) {
    console.error(err);
  }
}

export async function saveGameData(white, black, moveData) {
  try {
    const whiteId = await getUserId(white);
    const blackId = await getUserId(black);
    const stringifiedMoves = stringifyMoves(moveData)
    let sql = 'UPDATE active_games SET moves = $1 WHERE white=$2 AND black=$3';
    const res = await pool.query(sql, [stringifiedMoves, whiteId, blackId]);
    if (!res.rowCount) {
      sql = 'INSERT INTO active_games (white, black, moves) VALUES ($1, $2, $3)';
      await pool.query(sql, [whiteId, blackId, stringifiedMoves])
    }
  } catch (error) {
    console.error(error);
  }
}

