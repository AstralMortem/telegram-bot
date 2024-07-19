import axios from '@/plugins/axios'
import { defineStore } from 'pinia'
export const useGoldStore = defineStore('goldStore', {
    state: () => ({
        pending:false,
        amount: 1000000000,
        price: 1
    }),
    getters:{},
    actions:{
        async fetchGold(){
            this.pending = true
            axios.get("/gold").then((resp)=>{
                this.price = resp.data.gold_price
                this.amount = resp.data.total_gold
            })
            this.pending = false
        }
    }
})