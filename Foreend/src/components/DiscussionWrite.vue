<template>
    <el-row type="flex" justify="center">
        <el-col :span="15">
            <el-form :model="writedata" :rules="rules" ref="writeform" label-width="100px" label-position="top">
                <el-form-item label="标题" prop="title">
                    <el-input v-model="writedata.title"></el-input>
                </el-form-item>
                <el-form-item label="内容" prop="content" label-width="100">
                    <el-input type="textarea" :rows="10" v-model="writedata.content">
                    </el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submit">立即发表</el-button>
                    <el-button @click="back">取消</el-button>
                </el-form-item>
            </el-form>
        </el-col>
    </el-row>

</template>

<script>
    //import axios from 'axios'
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.headers.common = {
        'X-CSRFToken':document.querySelector('#csrf-token input').value,
        'X-Requested-With': 'XMLHttpRequest'
    };
    export default {
        name: "DiscussionWrite",
        props:{
            contestid:{
                Type:Number,
                default:-1
            },
            showtype:{
                Type:Object,
                default:{show:0}
            },
        },
        data:function(){
            return{
                isshowList:this.showtype,
                rules:{
                    title: [
                        { required: true, message: '请输入标题', trigger: 'blur' },
                        { min: 1, max: 30, message: '长度在 1 到 30 个字符', trigger: 'blur' }
                    ],
                    content: [
                        { required: true, message: '请输入内容', trigger: 'blur' },
                        { min: 1, max: 1000, message: '长度在 1 到 1000 个字符', trigger: 'blur' }
                    ],
                },
                writedata:{
                    title:'',
                    content:''
                }
            }
        },
        methods:{
            submit:function () {
                let self = this;
                this.$refs['writeform'].validate((valid) => {
                    if (valid) {

                        axios.post('/api/competition/adddiscussion',{
                            contestid:self.contestid,
                            title:self.writedata.title,
                            content:self.writedata.content
                        }).then(function (response) {
                            if(response.data.msg!==''){
                                self.$message({
                                    message:'发送失败！'+response.data.msg,
                                    type:'error'
                                });
                                return;
                            }
                            self.$message({
                                message:'发送成功！',
                                type:'success'
                            });
                            self.back();
                        }).catch(function (error) {
                            console.log(self.writedata.title,self.writedata.content)
                            self.$message({
                                message:'发送失败！',
                                type:'error'
                            });
                        });
                        return true;
                    } else {
                        return false;
                    }
                });
            },
            back:function () {
                this.writedata.title = '';
                this.writedata.content = '';
                this.isshowList.show = 0;
            }
        }
    }
</script>

<style scoped>

</style>