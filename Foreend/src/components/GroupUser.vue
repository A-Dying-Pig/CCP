<template>
    <div>
        <div class="group-user-title">添加组员(组队人数{{ group_min_number}} ~ {{ group_max_number}}人)</div>
    <el-form :inline="true" :model="ruleForm" :rules="rules" ref="ruleForm">
        <el-form-item label="查询用户" prop="curr_user" :error="input_error">
            <el-input v-model="ruleForm.curr_user" placeholder="输入队友的用户名" ></el-input>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="OnSubmit" class="group_user_add_btn">添加</el-button>
        </el-form-item>
    </el-form>

    <el-table :data="group_user" style="width: 100%">
        <el-table-column prop="name" label="组员" min-width="5"></el-table-column>
        <el-table-column label="删除" width="180" min-width="1">
            <template slot-scope="scope">
                <el-button
                        size="mini"
                        type="danger"
                        @click="handleDelete(scope.$index, scope.row)">删除</el-button>
            </template>
        </el-table-column>
    </el-table>
    </div>

</template>


<script>
    import axios from 'axios'

    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.headers.common = {
        'X-CSRFToken':document.querySelector('#csrf-token input').value,
        'X-Requested-With': 'XMLHttpRequest'
    };

    export default {
        props:{
            group_min_number:{
                default:1
            },
            competition_id:{
                default:-1,
            },
            group_max_number:{
                default:1,
            },
        },
        data:function () {
            var validateUser = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('查询用户不能为空!'));
                } else if (/^[a-zA-Z0-9_]+$/.test(value) === false){
                    callback(new Error("请输入合法的用户名!"));
                }
                    callback();
            };

            var validateNumber = (rule, value, callback) => {
                if (this.group_user.length < this.group_min_number - 1){
                    callback(new Error(`至少需要${this.group_min_number - 1}名队友组队!`));
                }
                callback();
            };
            return{
                input_error:'',
                group_user:[],
                member_number:0,

                ruleForm: {
                        curr_user: '',
                    },
                rules:{
                    curr_user: [
                        { validator:validateNumber, trigger: 'blur' },
                    ]
                }

            }
        },
        methods:{
            handleDelete(index, row) {
                this.member_number -= 1;
                //this.$set(this.group_user,index,null);
                this.group_user.splice(index,1);
                let temp = [];
                for (let i = 0 ; i < this.group_user.length; i++){
                    temp.push(this.group_user[i].name);
                }
                this.$emit('new-group',{number:this.member_number,value:temp});

            },
            OnSubmit() {
                this.input_error='';
                for (let i = 0; i < this.member_number; i++){
                    if (this.group_user[i].name === this.ruleForm.curr_user){
                        this.input_error=`${this.ruleForm.curr_user} 已经选为您的队友!`;
                        return;
                    }
                }

                if (this.group_user.length === this.group_max_number - 1){
                    this.input_error = `至多与${this.group_max_number - 1}名队友组队!`;
                    return;
                }

                if (this.ruleForm.curr_user === '') {
                    this.input_error='请输入查询用户名!';
                    return;
                }
                if (/^[a-zA-Z0-9_]+$/.test(this.ruleForm.curr_user) === false){
                    this.input_error='请输入合法的用户名!';
                    return;
                }
                if (this.group_user.length < this.group_min_number - 1){
                    this.input_error = `至少需要${this.group_min_number - 1}名队友组队!`;
                }

                let vm = this;
                axios.post('/api/user/check',{username:this.ruleForm.curr_user,contestid:this.competition_id})
                    .then((response)=>{
                            if(response.data.msg !== ''){
                                vm.input_error = response.data.msg;
                            }
                            else{
                                vm.$set(vm.group_user,vm.member_number,{name:vm.ruleForm.curr_user});
                                vm.member_number += 1;
                                let temp = [];
                                for (let i = 0 ; i < vm.group_user.length; i++){
                                    temp.push(vm.group_user[i].name);
                                }
                                vm.$emit('new-group',{number:vm.member_number,value:temp});
                             }
                        }
                    )
            },
        }

    }

</script>


<style>
    .group_user_add_btn{
        position: absolute;
    }
    .group-user-title{
        margin-top: 20px;
        margin-bottom: 20px;
    }

</style>