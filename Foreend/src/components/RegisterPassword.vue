<template>
    <el-form :model="input_msg" status-icon :rules="m_rules" ref="input_msg" label-width="100px" class="register-input">
        <el-form-item label="密码" prop="pass">
            <el-input type="password" v-model="input_msg.pass" autocomplete="off" placeholder="字母,_,数字的组合,长度大于5">
            </el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="checkPass">
            <el-input type="password" v-model="input_msg.checkPass" autocomplete="off"></el-input>
        </el-form-item>
    </el-form>
</template>

<script>
    export default {
        name:'RegisterPassword',
        data() {
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
                } else if (value !== this.input_msg.pass) {
                    callback(new Error('两次输入密码不一致!'));
                } else {
                    callback();
                }
            };
            return {
                input_msg: {
                    pass: '',
                    checkPass: '',
                },
                m_rules: {
                    pass: [
                        { validator: validatePass, trigger: 'blur' }
                    ],
                    checkPass: [
                        { validator: validatePass2, trigger: 'blur' }
                    ],
                }
            };
        },
    }
</script>

<style src="./commonCSS/input.css"></style>