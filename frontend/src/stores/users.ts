import { defineStore } from 'pinia'
import { type IUserList } from '../types'
import axios from '../plugins/axios'
import { useWebApp } from 'vue-tg'

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
    async fetchMe() {
      const tgApp = useWebApp()
      this.pending = true
      if (tgApp.initDataUnsafe.user) {
        axios
          .get(`/users/${tgApp.initDataUnsafe.user.id}`)
          .then((response) => {
            this.current_user = response.data
          })
          .catch((err) => {
            console.error(err)
          })
      }

      this.pending = false
    },
    async fetchUsers() {
      this.pending = true
      axios
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
    getSelectedUser(user_id: number) {
      return this.users.filter((x) => x.id === user_id)
    }
  }
})
