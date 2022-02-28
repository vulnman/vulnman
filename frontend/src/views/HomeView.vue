<template>              
    <div>
        <NavbarTop />  
        <h1>Hello {{ $store.state.username }}</h1>

        <div class="list-group mt-3">
            <a class="list-group-item list-group-item-action" v-for="project in projects">
                <div class="row">
                    <div class="col-sm-12">
                        <div class="clearfix">
                            <div class="float-start">
                                <p>{{ project.name }} ({{project.client.name }})</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-sm-12">
                        <div class="clearfix">
                            <div class="float-start">
                                <small class="text-muted"><i>Last updated: {{ project.date_updated|timesince }} ago</i></small>
                            </div>
                        </div>
                    </div>
                </div>
            </a>
        </div>
    </div>
</template>

<script>
import NavbarTop from '../components/elements/navigation/navbar.vue'
import axios from 'axios'


export default {
    name: "Login",
    components: {
        'NavbarTop': NavbarTop
    },
    data () {
        return {
            "projects": []
        }
    },
    mounted () {
      this.getProjects()  
    },
    methods: {
        getProjects: function() {
            axios.get("/api/v1/projects/").then(response => {
                this.projects = response.data.results
            })
        }
    }
}
</script>