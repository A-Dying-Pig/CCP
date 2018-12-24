<template>
  <div id="app">
    <el-container>
    <el-header height="100px" class="header">
      <div><NavigationBar></NavigationBar></div>
    </el-header>

      <el-main>
      <div class = "login_main_page">
      <el-row :gutter="0">
        <el-col :span="24" class="banner">登入您的账户 </el-col>
      </el-row>

      <el-row :gutter="0" class = "warning_msg">
        <el-col :span="24">
          <el-alert v-show="error_msg!=='#'" :title="error_msg" type="error" center></el-alert>
        </el-col>
      </el-row>

      <el-form :model="input_msg" status-icon :rules="m_rules" ref="input_msg" label-width="100px">
      <el-row :gutter="0">
        <el-col :span="9" :offset="7">
          <el-form-item label="用户名" prop="username"><el-input type="text" v-model="input_msg.username" placeholder="字母,_,数字的组合" autocomplete="off"></el-input></el-form-item></el-col>
      </el-row>

      <el-row :gutter="0">
        <el-col :span="9" :offset="7">
          <el-form-item label="密码" prop="pass">
          <el-input type="password" v-model="input_msg.pass" autocomplete="off" placeholder="字母,_,数字的组合,长度大于5"></el-input>
          </el-form-item>
        </el-col>
      </el-row>

        <el-row :gutter="0">
          <div class="login-btn">
              <el-button type="success" @click="submitForm('input_msg')"><span class="form-btn">登录</span></el-button>
          </div>
        </el-row>
      </el-form>
      </div>

        <el-row :gutter="20">
          <el-col :span="24" class="banner2">您的账户适用于CCP的所有服务</el-col>
        </el-row>
        <el-row :gutter="20">
          <div class="login-icon">
            <img src="../../assets/img/login_service_intro.png" class="login_service_intro">
          </div>
        </el-row>

        <el-row :gutter="5">
          <div class="login-btn">
            <a href="/register" class="login_register" > 创建您的账户> </a>
          </div>
        </el-row>
    </el-main>
    </el-container>
  </div>
</template>

<script>
    import NavigationBar from '../../components/NavigationBar'
    import axios from 'axios'

    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.headers.common = {
      'X-CSRFToken':document.querySelector('#csrf-token input').value,
        'X-Requested-With': 'XMLHttpRequest'
    };

    export default {
        name: 'app',
        props:{
            error_msg:{
                default:'#',
                type:String
            }
        },
        data() {
            var validateUser = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('用户名不能为空!'));
                }
                callback();
            };
            var validatePass = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('密码不能为空!'));
                }
                callback();
            };

            return {
                input_msg: {
                    username: '',
                    pass:'',
                },
                m_rules: {
                    username: [
                        { validator: validateUser, trigger: 'blur' }
                    ],
                    pass: [
                        { validator: validatePass, trigger: 'blur' }
                    ],
                },
            };
        },
        components: {
            NavigationBar
        },
        methods:{
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        let vm = this;
                        axios.post('/api/user/login', {username:this.input_msg.username,password:this.input_msg.pass})
                            .then(response=>{
                                if (response.data.msg ==='') {
                                    //成功
                                    vm.$message({
                                        message: '登录成功!',
                                        type: 'success'
                                    });
                                    window.location.href = '/';
                                }
                                else{
                                  //失败
                                  vm.error_msg = response.data.msg;
                                }
                            });
                    } else {
                        //console.log('error submit!!');
                        return false;
                    }
                });
            },
        }
    }
</script>

<style>

  .form-btn{
    font-size:17px;
  }
  .banner{
    font-size:45px;
    text-align: center;
    font-family: "PingFang SC";
    padding: 70px 0px 0px 0px;
  }

  .banner2{
    font-size:40px;
    text-align: center;
    font-family: "PingFang SC";
    padding: 60px 0px 0px 0px;
  }

  .warning_msg{
    margin-bottom: 10px;
  }

  .login_main_page{
    background: url(../../assets/img/login_background.jpg);
    background-size: 100% 100%;
  }
  .el-col{
    margin-top: 15px;
    margin-bottom: 15px;
  }
  .login_service_intro{
    width: 20%;
    height: 20%;
  }
  .login_register{
    font-size: 18px;
    text-decoration: none;
    color: initial;
  }
  .login-icon{
    text-align: center;
  }

  .login_register:hover{
    font-size: 18px;
    text-decoration: none;
    color: dodgerblue;
  }
  .login-btn{
    text-align: center;
    margin-bottom: 40px;
    margin-top: 20px;
  }
</style>