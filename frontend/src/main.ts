import './assets/style.css'

import VueTelegram from 'vue-tg'
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import { OhVueIcon, addIcons } from 'oh-vue-icons'
import { MdLeaderboard, MdHome } from 'oh-vue-icons/icons'


const app = createApp(App)
addIcons(MdLeaderboard, MdHome)

app.use(createPinia())
app.use(router)
app.use(VueTelegram)
app.component('v-icon', OhVueIcon)

app.mount('#app')
