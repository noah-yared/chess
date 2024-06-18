const { Server } = require("socket.io");
const { join } = require("path");
const { randomUUID } = require("crypto");
const { move } = require("./auth");

let io;

module.exports = (server) => {
  io = new Server(server);

  const matchmaking = io.of("/matchmaking");
  const customRoom = io.of("/customRoom");

  const matchmakingConnections = {};
  const customRoomConnections = {};
  const customRooms = {};
  const sockets = {};
  const openMatchmakingRooms = [];

  let existingRoom, newRoom;
  matchmaking.on("connection", (socket) => {
    socket.on("findRoom", () => {
      // assign room to user
      if (!openMatchmakingRooms.length) {
        // generate UUID for room
        newRoom = randomUUID();
        socket.join(newRoom);
        openMatchmakingRooms.push(newRoom);
      } else {
        // TODO: implement skill-based matchmaking as needed
        existingRoom = openMatchmakingRooms.pop();
        socket.join(existingRoom);
      }      
    });
    socket.on("getUsername", (username) => {
      sockets[socket.id] = username; // store socket.id-user connection
      matchmakingConnections[username] = room; // store user-room connection
    });
    socket.on("move", (moveInfo) => {
      const room = matchmakingConnections[sockets[socket.id]];
      matchmaking.to(room).emit("displayMove", moveInfo);
    });
    socket.on("gameOver", () => {
      delete matchmakingConnections[sockets[socket.id]];
    }) 
  });


  customRoom.on("connection", (socket) => {
    socket.on("getUsername", (username) => {
      sockets[socket.id] = username;
    })
    // assign room to user
    socket.on("joinRoom", (room, password) => {
      if (customRooms[room] === undefined ||
        customRooms[room].password != password ||
        customRooms[room].members >= 2){
          // reject join room request
          socket.emit("rejectJoinRoom");
        } else {
          // accept join requets
          socket.join(room);
          customRooms[room].members.push(sockets[socket.id]);
          customRoomConnections[sockets[socket.id]] = room;
        }
    });
    socket.on("createRoom", (room, password) => {
      if (customRooms[room] !== undefined) {
        socket.emit("rejectCreateRequest");
      } else {
        customRooms[room] = {
          "members": [sockets[socket.id]],
          "password": password
        };
        customRoomConnections[sockets[socket.id]] = room;
      }
    });
    socket.on("move", (moveInfo) => {
      const room = customRoomConnections[sockets[socket.id]];
      customRoom.to(room).emit("displayMove", (moveInfo));
    });
    socket.on("gameOver", () => {
      delete customRooms[room];
      delete customRoomConnections[sockets[socket.id]];
    })
  });
}

