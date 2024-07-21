import { socket } from "@/plugins/websocket";
import { defineStore } from "pinia";

export const useConnectionStore = defineStore("connection", {
    state: () => ({
      isConnected: false,
    }),
  
    actions: {
      bindEvents() {
        socket.on("connect", () => {
          this.isConnected = true;
        });
  
        socket.on("disconnect", () => {
          this.isConnected = false;
        });
      },
  
      connect() {
        socket.connect();
      }
    },
  });