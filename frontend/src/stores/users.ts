import { defineStore } from 'pinia'
import { type IUserList } from '../types'
import axios from '../plugins/axios'

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
            this.current_user = response.data
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
          this.users.push(...response.data)
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
    }
  }
})
