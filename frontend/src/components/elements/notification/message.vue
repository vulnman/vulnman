<template>
    <CAlert color="danger" dismissible @close="alert">
        <strong>Login failed!</strong> Username and/or Password wrong
    </CAlert>
</template>

<script>
import CAlert from "@coreui/bootstrap-vue"


export default {
    name: 'Message'
}
</script>
