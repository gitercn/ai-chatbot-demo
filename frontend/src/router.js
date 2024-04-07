import Vue from 'vue'
import VueRouter from 'vue-router'
import Chat from './components/Chat.vue'


Vue.use(VueRouter)

const routes = [
  { path: '/', component: Chat },
]

const router = new VueRouter({
  routes
})

export default router