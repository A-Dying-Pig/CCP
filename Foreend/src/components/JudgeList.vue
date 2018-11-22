<template>
    <div>
        <el-form :inline="true" :model="judgeinfo" ref="judgeinput">
            <el-form-item label="查询用户">
                <el-input v-model="judgeinfo.name" placeholder="输入评委的用户名" ></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="OnSubmit">添加</el-button>
            </el-form-item>
        </el-form>
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
        name: "JudgeList",
        props:['contestid'],
        data:function () {
            return {
                judgeinfo:{
                    name:''
                },
                rules:{

                }
            }
        },
        methods:{
            OnSubmit:function () {
                let self = this;
                if(self.judgeinfo.name===''){
                    self.$message({
                        message:'名称不可以为空!',
                        type:'error'
                    })
                }
                else {
                    console.log(self.judgeinfo.name);
                    axios.post('/api/admin/addJudge',{
                        username:self.judgeinfo.name,
                        contestid:self.contestid
                    }).then(function (response) {
                        if(response.data.msg==''){
                            self.$message({
                                message:'创建成功!',
                                type:'success'
                            })
                        }
                    })
                }
            },
        }
    }
</script>

<style scoped>

</style>