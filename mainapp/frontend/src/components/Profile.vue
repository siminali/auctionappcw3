<script setup lang="ts">
import NavBar from './NavBar.vue';

</script>

<script lang="ts">

import { defineComponent, reactive, ref, toRefs } from "vue";

export default defineComponent({
    data(){
        return{
            email: undefined,
            dob: undefined,
            previewImage: "https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/aval-bg.webp",
            profile: {}
        }

    },
    created(){
        this.searchUser()
    },
    mounted(){
        console.log("starting")
        console.log(this.$forceUpdate.params)
    }
    methods:{
        uploadImage(e){
            const [image]: any = e.target.files;
            const reader: any = new FileReader();
            reader.readAsDataURL(image);
            reader.onLoad = e => {
                this.previewImage = e.target.result;
                //need to make ajax request to change the name
                console.log(this.previewImage);
            };
        },

        async updateEmail(email: String){
            var url: string = `http://localhost:8000/api/User/${this.$route.params.username}`;
            const requestOptions: any = {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json '},
                body: JSON.stringify({
                    email: email,
                }),
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",

            };
            console.log(requestOptions)
            let response: Response = await fetch(url, requestOptions);
            this.profile.email = email
            let data: JSON = await response.json();
            return (data)

        },
        async updateDob(dob: String){
            var url: String = `http://localhost:8000/api/User/${this.$route.params.username}`;
            const requestOptions: any = {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json '},
                body: JSON.stringify({ dob: dob }),
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",

            };
            console.log(requestOptions)
            let response: Response = await fetch(url, requestOptions);
            this.profile.dob = dob
            let data: JSON = await response.json();
            return (data)
        },
        async searchUser(){
            var url = `http://localhost:8000/api/user/${this.$route.params.username}`;
            const res: Response = await fetch(url), {
                credentials: "include",
                mode: "cors",

            }
            console.log(this.profile)
        },
        getData(): {} {
            return this.profile
        }

    }

})

</script>