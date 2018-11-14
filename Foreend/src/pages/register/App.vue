<template>
  <div id="app">
    <el-container>
    <el-header height="100px" class="header">
      <div><NavigationBar></NavigationBar></div>
    </el-header>
    <el-main>
      <el-row :gutter="20">
        <el-col :span="24" class="banner">创建您的账户 </el-col>
      </el-row>

      <el-row :gutter="20" class = "warning_msg">
        <el-col :span="24">
          <el-alert v-show="input_error" :title="error_msg" type="error" center></el-alert>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="9" :offset="7"><div><RegisterUsername @new_username="username = $event"></RegisterUsername></div></el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="9" :offset="7"><div><RegisterPassword @new_password="passwd = $event"></RegisterPassword></div></el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="9" :offset="7"><div><RegisterEmail @new_email="email = $event"></RegisterEmail></div></el-col>
      </el-row>

      <el-row :gutter="10">
        <el-col :span="1" :offset="12"><el-button @click="check_register" type="text" size="medium"><span class="continue-btn">继续</span></el-button></el-col>
      </el-row>
    </el-main>
    </el-container>
  </div>
</template>

<script>
    import RegisterUsername from '../../components/RegisterUsername'
    import RegisterPassword from '../../components/RegisterPassword'
    import RegisterEmail from '../../components/RegisterEmail'
    import NavigationBar from '../../components/NavigationBar'

    export default {
        name: 'app',
        data:function(){
            return{
                input_error:false,
                error_msg:'输入错误',
                username:'',
                passwd:'',
                email:'',
            }
        },
        components: {
            RegisterUsername,
            RegisterPassword,
            RegisterEmail,
            NavigationBar
        },
        methods:{
            check_register:function () {
                if (this.username.length === 0 || this.email === 0 || this.passwd === 0 ){
                    this.input_error = true;
                    return;
                }
                this.input_error = false;
                this.$http.post('/register', {'username':this.username,'password':this.password,'email':this.email}).
                then(response => {
                    console.log("success!");
                }, response => {
                    console.log("fail!");
                });

            }
        }
    }
</script>

<style>

  .continue-btn{
    font-size:20px;
  }
  .banner{
    font-size:30px;
    background: #F0F8FF;
    text-align: center;
    font-family: "PingFang SC";
    padding: 40px 0px 40px 0px;
  }

  .warning_msg{
    margin-bottom: 50px;
  }
</style>