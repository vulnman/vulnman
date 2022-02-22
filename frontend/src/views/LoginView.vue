<template>
    <div class="row no-gutter">
        <div class="d-none d-md-flex col-md-4 col-lg-6 bg-image border-end"></div>
        <div class="col-md-8 col-lg-6">
            <div class="login d-flex align-items-center py-5">
                <div class="container">
                    <div class="row">
                        <div class="col-md-9 col-lg-8 mx-auto">
                            <h3 class="login-heading mb-4">Welcome back!</h3>
                            <CForm>
                            <form v-on:submit.prevent="submitForm" class="form-horizontal">
                                <div class="form-floating mb-3">
                                    <input type="text" id="username" name="username" v-model="username" class="form-control" />
                                    <label for="username">Username</label>
                                </div>
                                <div class="form-floating mb-3">
                                    <input type="password" id="password" name="password" v-model="password" class="form-control" />
                                    <label for="password">Password</label>
                                </div>
                                </form>
                            </CForm>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import axios from 'axios'
import CForm from "@coreui/coreui"

export default {
    name: "Login",
    data () {
        return {
            username: '',
            password: ''
        }
    },
    methods: {
        submitForm(e){
            const formData = {
                username: this.username,
                password: this.password
            }
            axios.post("/api-token-auth", formData).then(response => {
                console.log(response.data)
                const token = response.data.token
                this.$store.commit('setToken', token)
                axios.defaults.headers.common["Authorization"] = "Token " + token
                localStorage.setItem("token", token)
            }).catch(error => {
                console.log(error)
            })
        }
    }
}
</script>
<style scoped>
        :root {
            --input-padding-x: 1.5rem;
            --input-padding-y: 0.75rem;
        }

        .login {
            min-height: 100vh;
        }

        .bg-image {
            background-image: url('http://localhost:8000/static/images/logo.png');
            background-size: auto;
            background-repeat: no-repeat;
            background-position: center;
        }

        .login-heading {
            font-weight: 300;
        }

        .form-label-group > input,
        .form-label-group > label {
            padding: var(--input-padding-y) var(--input-padding-x);
            height: auto;
            border-radius: 2rem;
        }

        .form-label-group > label {
            position: absolute;
            top: 0;
            left: 0;
            display: block;
            width: 100%;
            margin-bottom: 0;
            /* Override default `<label>` margin */
            line-height: 1.5;
            color: #495057;
            cursor: text;
            /* Match the input under the label */
            border: 1px solid transparent;
            border-radius: .25rem;
            transition: all .1s ease-in-out;
        }

        .form-label-group input::-webkit-input-placeholder {
            color: transparent;
        }

        .form-label-group input:-ms-input-placeholder {
            color: transparent;
        }

        .form-label-group input::-ms-input-placeholder {
            color: transparent;
        }

        .form-label-group input::-moz-placeholder {
            color: transparent;
        }

        .form-label-group input::placeholder {
            color: transparent;
        }

        .form-label-group input:not(:placeholder-shown) {
            padding-top: calc(var(--input-padding-y) + var(--input-padding-y) * (2 / 3));
            padding-bottom: calc(var(--input-padding-y) / 3);
        }

        .form-label-group input:not(:placeholder-shown) ~ label {
            padding-top: calc(var(--input-padding-y) / 3);
            padding-bottom: calc(var(--input-padding-y) / 3);
            font-size: 12px;
            color: #777;
        }

    </style>