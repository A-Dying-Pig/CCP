<template>
    <el-form :model="input_msg" status-icon :rules="m_rules" ref="input_msg" label-width="100px" class="register-input">
        <el-form-item label="邮箱" prop="email">
            <el-input type="text" v-model="input_msg.email" autocomplete="off">
            </el-input>
        </el-form-item>
    </el-form>
</template>

<script>
    export default {
        name:'RegisterPassword',
        data() {
            var validateEmail = (rule, value, callback) => {
                this.$emit('new_email','');
                if (value === '') {
                    callback(new Error('请输入邮箱地址'));
                } else {
                    if (/^[a-zA-Z0-9_]+@[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+/.test(value) === false) {
                        callback(new Error("请输入合法的邮箱地址"));
                    }
                    else{
                        this.$emit('new_email',value)
                    }
                    callback();
                }
            };
            return {
                input_msg: {
                    email: '',
                },
                m_rules: {
                    email: [
                        { validator: validateEmail, trigger: 'blur' }
                    ],
                }
            };
        },
    }
</script>
