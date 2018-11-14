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

      <el-form :model="input_msg" status-icon :rules="m_rules" ref="input_msg" label-width="100px">
      <el-row :gutter="20">
        <el-col :span="9" :offset="7">
          <el-form-item label="邮箱" prop="email"><el-input type="text" v-model="input_msg.email" autocomplete="off"></el-input></el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="9" :offset="7">
          <el-form-item label="用户名" prop="username"><el-input type="text" v-model="input_msg.username" placeholder="字母,_,数字的组合" autocomplete="off"></el-input></el-form-item></el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="9" :offset="7">
          <el-form-item label="密码" prop="pass">
          <el-input type="password" v-model="input_msg.pass" autocomplete="off" placeholder="字母,_,数字的组合,长度大于5"></el-input>
          </el-form-item>
        </el-col>
      </el-row>

        <el-row :gutter="20">
          <el-col :span="9" :offset="7">
            <el-form-item label="确认密码" prop="checkPass">
              <el-input type="password" v-model="input_msg.checkPass" autocomplete="off"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="1" :offset="9">
            <el-form-item>
              <el-button type="text" @click="submitForm('input_msg')"><span class="form-btn">继续</span></el-button>
            </el-form-item>
          </el-col>

          <el-col :span="1" :offset="1">
            <el-form-item>
              <el-button type='text' @click="resetForm('input_msg')"><span class="form-btn">重置</span></el-button>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-main>
    </el-container>
  </div>
</template>

<script>
    import NavigationBar from '../../components/NavigationBar'
    import axios from 'axios'

    export default {
        name: 'app',
        data() {
            var validateEmail = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请输入邮箱地址'));
                }
                else if (/^[a-zA-Z0-9_]+@[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+/.test(value) === false) {
                    callback(new Error("请输入合法的邮箱地址"));
                }
                callback();
            };

            var validateUser = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请输入用户名'));
                }
                else if (/^[a-zA-Z0-9_]+$/.test(value) === false){
                    callback(new Error("请输入合法的用户名"));
                }
                callback();
            };
            var validatePass = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请输入密码'));
                } else {
                    if (value.length < 6){
                        callback(new Error("密码必须长度大于5"));
                    }
                    else if(/^[a-zA-Z0-9_]+$/.test(value) === false) {
                        callback(new Error("密码必须是字母,_,数字的组合!"));
                    }
                    else if (this.input_msg.checkPass !== '') {
                        this.$refs.input_msg.validateField('checkPass');
                    }
                    callback();
                }
            };
            var validatePass2 = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请再次输入密码'));
                }
                else if (value !== this.input_msg.pass) {
                    callback(new Error('两次输入密码不一致!'));
                }
                else {
                    callback();
                }
            };

            return {
                input_error:false,
                error_msg:"",
                input_msg: {
                    email: '',
                    username: '',
                    pass:'',
                    checkPass:'',
                },
                m_rules: {
                    email: [
                        { validator: validateEmail, trigger: 'blur' }
                    ],
                    username: [
                        { validator: validateUser, trigger: 'blur' }
                    ],
                    pass: [
                        { validator: validatePass, trigger: 'blur' }
                    ],
                    checkPass: [
                        { validator: validatePass2, trigger: 'blur' }
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
                        axios.post('/register', {username:this.input_msg.username,password:this.input_msg.pass,email:this.input_msg.email})
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            resetForm(formName) {
                this.$refs[formName].resetFields();
            }
        }
    }
</script>

<style>

  .form-btn{
    font-size:18px;
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