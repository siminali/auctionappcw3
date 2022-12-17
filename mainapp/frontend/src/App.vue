<!-- <template>
  <div id="nav">
    <router-link to="/">Home</router-link> |
    <router-link to="/username/profile">Profile</router-link>
  </div>
  <router-view/>
</template> -->



<template>
  <div>
      <!-- <NavBar /> -->
      
          

              <div>
              <ul>
              
              <li v-for="User in Users" class="text-left font-weight-light text-primary"> 
               {{Users}}
               </li>
               </ul>
               <button class="btn btn-success d-block" @click="fetchUser">Fetch User</button>
              </div>
               </div>

              <img :src="previewImage" class="img-fluid my-5"/>
              <label><b>Change Profile Image</b>: <input type="file" name="image" accept="image/" id="id_image" @change="uploadImage"></label>


              <h1>Profile Page: {{ this.profile.name }}</h1>

              <h6 class="text-dark">Email: {{ this.profile.email }}</h6>
              <input type="text" name="dob" id="id_email" v-model="email"/>
              <button type="button" @click="updateEmail(String(email))">Update</button>

             
              <h6 class="text-dark">Date of Birth: {{ this.profile.dob }}</h6>
              <input type="datetime-local" name="dob" id="id_dob" v-model="dob"/>
              <button type="button" @click="updateDob(String(dob))">Update</button>

        
    


  
</template>



<script>

import { defineComponent, reactive, ref, toRefs } from "vue";

export default defineComponent({
  data(){
      return{
          email: undefined,
          dob: undefined,
          previewImage: "https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/aval-bg.webp",
          profile: {},
          Users: [],
      }

  },
  created(){
      this.fetchUser()
  },
  mounted(){
      console.log("starting")
      console.log(this.$forceUpdate.params)
  },
  methods:{
      uploadImage(e){
          const [image] = e.target.files;
          const reader = new FileReader();
          reader.readAsDataURL(image);
          reader.onLoad = e => {
              this.previewImage = e.target.result;
              //need to make ajax request to change the name
              console.log(this.previewImage);
          };
      },

      async fetchUser(){
          //Perform an Ajax Request to fetch the list of movies
          var url = `http://localhost:8000/api/User/email/${this.$route.params.username}`;
        //   let response = await fetch(`http://localhost:8000/api/User/${this.$route.params.username}`)
        //   let data = await response.json()
        //   this.Users = data.Users


          const requestOptions = {
              method: 'GET',
              headers: { 'Content-Type': 'application/json '},
              body: JSON.stringify({
                  Users: Users,
              }),
              credentials: "include",
              mode: "cors",
              referrerPolicy: "no-referrer",

          };
          console.log(requestOptions)
          let response = await fetch(url, requestOptions);
          this.Users = email
          let data = await response.json();
          return (data)
      
      },

      async updateEmail(email){
          var url = `http://localhost:8000/api/User/email/${this.$route.params.username}`;
          const requestOptions = {
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
          let response = await fetch(url, requestOptions);
          this.profile.email = email
          let data = await response.json();
          return (data)

      },
      async updateDob(dob){
          var url = `http://localhost:8000/api/User/dob/${this.$route.params.username}`;
          const requestOptions = {
              method: 'PUT',
              headers: { 'Content-Type': 'application/json '},
              body: JSON.stringify({ dob: dob }),
              credentials: "include",
              mode: "cors",
              referrerPolicy: "no-referrer",

          };
          console.log(requestOptions)
          let response = await fetch(url, requestOptions);
          this.profile.dob = dob
          let data = await response.json();
          return (data)
      },
      // async searchUser(){
      //     var url = `http://localhost:8000/api/user/${this.$route.params.username}`;
      //     const res: Response = await fetch(url), {
      //         credentials: "include",
      //         mode: "cors",

      //     }
      //     console.log(this.profile)
      // },
      getData() {
          return this.profile
      }

  }

})

</script>

