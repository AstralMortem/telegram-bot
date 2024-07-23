import axios from '@/plugins/axios'
import { socket } from '@/plugins/websocket'
import { defineStore } from 'pinia'
export const useGoldStore = defineStore('goldStore', {
  state: () => ({
    pending: false,
    amount: 1000000000,
    price: 1,
    is_new_price_up: true
  }),
  getters: {},
  actions: {
    async fetchGold() {
      this.pending = true
      await axios.get('/gold').then((resp) => {
        this.price = Number(resp.data.gold_price.toFixed(8))
        this.calculateVector(resp.data.gold_price)
        this.amount = Number(resp.data.total_gold.toFixed(8))
      }).catch(error => console.error(error))
      this.pending = false
    },
    bindEvents(){
      socket.on("connect", ()=>{
        socket.on("gold:get", (data)=>{
          const dict = JSON.parse(data)
          this.amount = Number(dict.total_gold.toFixed(8))
          this.calculateVector(dict.gold_price)
          this.price = Number(dict.gold_price.toFixed(8))
        })
      })
    },
    calculateVector(new_price){
      this.is_new_price_up = new_price > this.price
    }
  }
})
