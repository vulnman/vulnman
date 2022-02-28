<template>
  <div class="container-fluid">
    <router-view/>
  </div>
</template>

<script>
import axios from 'axios'


export default {
  name: "Vulnman",
  beforeCreate() {
    this.$store.commit('initializeStore')

    const token = this.$store.state.token
    if ( token ) {
      axios.defaults.headers.common["Authorization"] = "Token " + token
    } else {
      axios.defaults.headers.common["Authorization"] = ''
    }
  }
}
</script>
