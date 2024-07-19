import { defineStore } from 'pinia'
import {type IUserList} from "../types"
import axios from '../plugins/axios'

export const useCounterStore = defineStore('usersStore', {
    state: () => ({
        pending: false,
        users: [] as IUserList[],
        limit: 10,
        offset: 0
    }),
    getters: {
      
    },
    actions: {
        async fetchUsers(){
            this.pending = true
            axios.get("/users",{params:{"limit":this.limit, "offset":this.offset}})
            .then((response) => {
                this.users = response.data
                this.offset += this.limit
            }).catch((err)=>{
                console.error(err)
            })

            this.pending = false
        }
    },
  })