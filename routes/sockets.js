const { Server } = require("socket.io");
const { join } = require("path");
const { randomUUID } = require("crypto");
const { move } = require("./auth");

let io;

module.exports = (server) => {
  io = new Server(server, {
    connectionStateRecovery: {}
  });

  const matchmaking = io.of("/matchmaking");
  const customRoom = io.of("/customRoom");

  const sockets = {};

  const matchmakingConnections = {};
  const openMatchmakingRooms = [];

  const customRoomConnections = {};
  const customRooms = {};

  const generateSide = () => Math.random() < 0.5 ? "white" : "black";

  const assignSides = (socket1, socket2) =>  {
    let socket1Color = generateSide();
    let socket2Color = socket1Color === "white" ? "black" : "white";
    socket1.emit("color", socket1Color);
    socket2.emit("color", socket2Color);
  } 

  const storeMatchmakingConnection = (socket1, socket2, room) => {
    matchmakingConnections[sockets[socket1.id]] = { "room": room, "opponent": sockets[socket2.id] };
    matchmakingConnections[sockets[socket2.id]] = { "room": room, "opponent": sockets[socket1.id] };
  }

  // const startGame = (socket1, socket2) => {
  //   socket1.emit("startGame");
  //   socket2.emit("startGame");
  // }

  let existingRoom, newRoom;
  let waitingSocket = null;
  matchmaking.on("connection", (socket) => {
    socket.on("findRoom", async () => {
      // assign room to user
      if (!waitingSocket) {
        waitingSocket = socket;
        console.log(`${sockets[waitingSocket.id]} is waiting for an available room.`);
      } else {
        newRoom = randomUUID();
        waitingSocket.join(newRoom); console.log(`${sockets[waitingSocket.id]} joined ${newRoom}`);
        socket.join(newRoom); console.log(`${sockets[socket.id]} joined ${newRoom}`);
        assignSides(waitingSocket, socket);
        storeMatchmakingConnection(waitingSocket, socket, newRoom);
        matchmaking.to(newRoom).emit("startGame");
        console.log('Sockets in newRoom:', matchmaking.adapter.rooms.get(newRoom));
        console.log("startGame event emitted!");
        // startGame(waitingSocket, socket);
      }
    });
    socket.on("disconnect", () => {
      console.log(`${sockets[socket.id]} disconnected from the room.`);
    })
    socket.on("getUsername", (username) => {
      console.log(`Got username! Username is ${username}`);
      sockets[socket.id] = username; // store socket.id-user connection
    });
    socket.on("move", (moveInfo) => {
      console.log("caught the emitted move event! now broadcasting for display!");
      let room = matchmakingConnections[sockets[socket.id]].room;
      socket.to(room).emit("displayMove", moveInfo);
    });
    socket.on("chatMessage", (message) => {
      console.log(`emitting message: ${message}`);
      let room = matchmakingConnections[sockets[socket.id]].room;
      socket.to(room).emit("displayMessage", message, sockets[socket.id]);
    });
    socket.on("gameOver", () => {
      let onlineRoom  = matchmakingConnections[sockets[socket.id]];
      console.log(`Opponent is ${onlineRoom.opponent}`);
      matchmaking.to(onlineRoom.room).emit("gameOver");
      delete onlineRoom;
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

