<template>
  <div id="app">
    <el-container>
      <el-header height="100px" class="header">
        <div><NavigationBar :username="musername"></NavigationBar></div>
      </el-header>
    </el-container>

    <el-container>
      <el-main>
        <div v-if="title !== '#'">
          <h1>{{title}}</h1>
          <p class="normal-msg-content">{{msg}}</p>
        </div>

        <div v-else>
          <p class="error-msg-content">{{msg}}</p>
        </div>
      </el-main>
    </el-container>

    <el-container>
      <el-footer>
        <CCPFooter></CCPFooter>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
    import NavigationBar from '../../components/NavigationBar'
    import CCPFooter from '../../components/CCPFooter'
    import axios from 'axios'

    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.headers.common = {
        'X-CSRFToken':document.querySelector('#csrf-token input').value,
        'X-Requested-With': 'XMLHttpRequest'
    };

    export default {
        name: 'app',
        props:{
            musername:{
                default:'',
                type:String,
            },
            title:{
                default:'',
                type:String,
            },
            msg:{
                default:'error',
                type:String
            },
            url:{
                default:'',
                type:String
            }
        },
        data() {
            return {

            }
        },
        components: {
            NavigationBar,
            CCPFooter
        },
        mounted:function () {
            if (this.url !== '#'){
                let vm = this;
                setTimeout(function () {
                    window.location.href = vm.url;
                },3000);
            }
        }
    }
</script>

<style>
  .error-msg-content{
    color: darkred;
    font-size: 20px;
  }
</style>