import { defineStore } from 'pinia'
import { type IUserList } from '../types'
import axios from '../plugins/axios'
import { socket } from '@/plugins/websocket'

export const useUsersStore = defineStore('usersStore', {
  state: () => ({
    pending: false,
    users: [] as IUserList[],
    current_user: {} as IUserList,
    limit: 10,
    offset: 0
  }),
  getters: {
    getUsers: (state) => state.users.filter((x) => x.id !== state.current_user.id)
  },
  actions: {
    async fetchUser(user_id: number) {
      this.pending = true
      await axios
          .get(`/users/${user_id}`)
          .then((response) => {
            const data = response.data as IUserList
            data.gold_amount = Number(data.gold_amount.toFixed(4))
            data.silver_amount = Number(data.silver_amount.toFixed(4))
            this.current_user = data
          })
          .catch((err) => {
            console.error(err)
          })
      this.pending = false
    },
    async fetchUsers() {
      this.pending = true
      await axios
        .get('/users', { params: { limit: this.limit, offset: this.offset } })
        .then((response) => {
          const data = response.data as IUserList[]
          data.map((x)=>{
            x.gold_amount = Number(x.gold_amount.toFixed(4))
            x.silver_amount = Number(x.silver_amount.toFixed(4))
          })
          this.users.push(...data)
          this.offset += this.limit
        })
        .catch((err) => {
          console.error(err)
        })

      this.pending = false
    },
    getSelectedUser(user_id: string) {
      return this.users.find((x) => x.id === Number.parseInt(user_id))
    },
    setCurrentUser(user_data:IUserList){
      this.current_user = user_data
    },
    bindEvents(){
      socket.on("connect", ()=>{
        socket.on("user:current", (data)=>{
          const dict = JSON.parse(data)
          if(this.current_user.id != dict.id){
            const index = this.users.findIndex(x => x.id === dict.id)
            this.users[index] = dict
          }
        })
      })
    },
  }
})
