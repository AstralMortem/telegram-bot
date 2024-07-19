import { defineStore } from 'pinia'
import {type IUserList} from "../types"
import axios from '../plugins/axios'
import { useWebApp } from 'vue-tg'

export const useUsersStore = defineStore('usersStore', {
    state: () => ({
        pending: false,
        users: [] as IUserList[],
        limit: 10,
        offset: 0
    }),
    getters: {
      getUsers: (state) => state.users 
    },
    actions: {
        async fetchUsers(){
            this.pending = true
            axios.get("/users",{params:{"limit":this.limit, "offset":this.offset}})
            .then((response) => {
                this.users.push(...response.data)
                this.offset += this.limit
            }).catch((err)=>{
                console.error(err)
            })

            this.pending = false
        }
    },
  })