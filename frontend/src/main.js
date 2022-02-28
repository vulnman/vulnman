import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from "axios"
//import '@coreui/coreui/dist/css/coreui.min.css'

axios.defaults.baseURL = "http://localhost:8000"


createApp(App).use(store).use(router, axios).mount('#app')
