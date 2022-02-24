<template>              
    <div>
        <NavbarTop />  
        <h1>Hello {{ $store.state.username }}</h1>
    </div>
</template>

<script>
import NavbarTop from '../components/elements/navigation/navbar.vue'

export default {
    name: "Login",
    components: {
        'NavbarTop': NavbarTop
    }
}
</script>