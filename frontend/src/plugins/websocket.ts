import { io } from "socket.io-client";
let url = import.meta.env.VITE_BACKEND_URL
export const socket = io(url,{
    "transports": ["websocket"],
    "extraHeaders":{
        "ngrok-skip-browser-warning":"true"
    },
    path: "/api/socket.io"
})

