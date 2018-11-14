<template>
    <el-form :model="input_msg" status-icon :rules="m_rules" ref="input_msg" label-width="100px" class="register-input">
        <el-form-item label="用户名" prop="username">
            <el-input type="text" v-model="input_msg.username" placeholder="字母,_,数字的组合" autocomplete="off">
            </el-input>
        </el-form-item>
    </el-form>
</template>

<script>
    export default {
        name:'RegisterUsername',
        data() {
            var validateUser = (rule, value, callback) => {
                this.$emit('new_username','');
                if (value === '') {
                    callback(new Error('请输入用户名'));
                } else {
                    if (/^[a-zA-Z0-9_]+$/.test(value) === false){
                        callback(new Error("请输入合法的用户名"));
                    }
                    else{
                        this.$emit('new_username',value)
                    }
                    callback();
                }
            };
            return {
                input_msg: {
                    username: '',
                },
                m_rules: {
                    username: [
                        { validator: validateUser, trigger: 'blur' }
                    ],
                }
            };
        },
    }
</script>
