import { io } from "socket.io-client";
let url = import.meta.env.VITE_BACKEND_URL
export const socket = io(url,{
    "extraHeaders":{
        "ngrok-skip-browser-warning":"true"
    },
})

