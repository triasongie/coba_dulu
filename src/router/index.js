import { createRouter, createWebHistory } from "vue-router"
import Home from "../pages/Home.vue"
import Features from "../pages/Feature.vue"
import ResultPage from "../pages/Resultpage.vue"
import History from "../pages/History.vue"
import AppPage from "../pages/AppPage.vue"
import HowToUse from "../pages/HowTo.vue"
import Contact from "../pages/Contact.vue"
import Login from "../pages/Login.vue"
import Register from "../pages/Register.vue"
import Detail from "../pages/Detail.vue"

const routes = [
  { path: "/", component: Home },
  { path: "/features", component: Features },
  { path: "/results", name: "ResultPage", component: ResultPage, meta: { hideNavbar: true } },
  { path: "/history", component: History, meta: { hideNavbar: true } }, 
  { path: "/appPage", component: AppPage, meta: { hideNavbar: true } },
  { path: "/howToUse", component: HowToUse },
  { path: "/contact", component: Contact },
  { path: "/auth", component: Login, meta: { hideNavbar: true }, showBackButton: true },
  { path: "/register", component: Register, meta: { hideNavbar: true }, showBackButton: true },
  { path: "/detail", component: Detail, meta: { hideNavbar: true } },

]

export default createRouter({
  history: createWebHistory(),
  routes
})

  