import { createStore } from 'vuex'

export default createStore({
  state: {
    token: '',
    isAuthenticated: false,
    username: ''
  },
  getters: {
  },
  mutations: {
    initializeStore(state){
      if ( localStorage.getItem('token')) {
        state.token = localStorage.getItem('token')
        state.isAuthenticated = true
      } else {
        state.token = ""
        state.isAuthenticated = false
      }

      if (localStorage.getItem("username")) {
        state.username = localStorage.getItem("username")
      }
    },
    setToken(state, token) {
      state.token = token
      state.isAuthenticated = true
    },
    removeToken(state, token) {
      state.token = ''
      state.isAuthenticated = false
    },
    setUsername(state, username) {
      state.username = username
    }
  },
  actions: {
  },
  modules: {
  }
})
