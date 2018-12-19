<template>
    <div>
    <el-form :model="loadinfo" ref="loadinfo" label-width="100px" class="demo-dynamic">
        <el-form-item
                prop="name"
                label="作品名称"
                :rules="[
      { required: true, message: '请输入作品名称', trigger: 'blur' }
    ]"
        >
            <el-input v-model="loadinfo.name" style="width: 100px"></el-input>
        </el-form-item>
    </el-form>
    <UploadFile :contestid="contestid" v-bind:file_max_number="1" :fileList="fileList" :file_max_size="100" :uploadurl="'/api/contestant/submit'" accept="zip" :needname="true" :uploadinfo="loadinfo"></UploadFile>
    </div>
</template>

<script>
    import UploadFile from './UploadFile'
    import axios from 'axios'
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.headers.common = {
        'X-CSRFToken':document.querySelector('#csrf-token input').value,
        'X-Requested-With': 'XMLHttpRequest'
    };
    export default {
        name: "ParticipantUpload",
        components:{
            UploadFile,
        },
        props:{
           contestid:{
               Type:Number,
               default:-1
           }
        },
        data:function () {
            return{
                loadinfo:{
                    name:'',
                },
                fileList:[],
            }
        },
        created:function () {
            let self = this;
            self.fileList = [];
            axios.post('/api/competition/worksname',{
                contestid:self.contestid
            }).then(function (response) {
                if(response.data.msg!==''){
                    self.$message({
                        message:response.data.msg,
                        type:'error'
                    });
                    return
                }
                if(response.data.filename !== ''){
                    self.fileList.push({name:response.data.filename});
                    console.log(self.fileList)
                }
            }).catch(function (error) {
                self.$message({
                    message:'获取上一个提交的作品失败！',
                    type:'error'
                });
            })
        }
    }
</script>

<style scoped>

</style>