<template>
    <div class="person-center-photo-div">
        <div class="person-center-photo-title">个人头像</div>
        <div class="person-center-photo-image">
            <img :src="img_url" class = 'person-center-photo'>
        </div>
        <div class="person-center-photo-btn">
            <el-upload
                    action=""
                    :show-file-list="false"
                    :before-upload="BeforeUpload"
                    :http-request="SubmitUpload">
                <el-button size="small" type="primary">点击上传头像</el-button>
            </el-upload>
        </div>
    </div>
</template>


<script>
    import axios from 'axios'
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    //axios.defaults.headers.common = {
    //    'X-CSRFToken':document.querySelector('#csrf-token input').value,
    //    'X-Requested-With': 'XMLHttpRequest'
    //};

    export default {
        props:{
            img_url:{
                type:String,
                default:'',
            },
            max_size:{
                default:2,
            },
        },
        data:function(){
            return{
            }
        },
        methods:{
            BeforeUpload:function (file) {
                const isTYPE = /\.(jpg|jpeg|png|JPG|PNG)$/.test(file.name);
                const isLtM = file.size / 1024 / 1024 < this.max_size;

                if(!isTYPE) {
                    this.$message({
                        message: '上传头像图片只能是 jpg,jpeg,png 格式!',
                        type: 'error'
                    });
                }
                if (!isLtM){
                    this.$message({
                        message: `上传头像图片大小不能超过 ${this.max_size} MB!`,
                        type: 'error'
                    });
                }
                return isTYPE && isLtM;
            },
            SubmitUpload:function (param) {
                let fileobj = param.file;
                let self = this;
                let fd = new FormData();
                fd.append('file',fileobj);
                axios.post('/api/user/uploadimg',fd,{
                }).then(function (response) {
                    let msg = response.data.msg;
                    if(msg !== ''){
                        self.$message({
                            message:'上传'+fileobj.name+'失败！',
                            type:'error'
                        });
                    }
                    else{
                        self.$message({
                            message: '上传图片成功',
                            type: 'success'
                        });
                        self.img_url = response.data.url;
                    }
                }).catch(function (error) {
                    self.$message({
                        message:'上传'+fileobj.name+'失败！',
                        type:'error'
                    });
                });
            }

        }
    }
</script>

<style>
    .person-center-photo-title{
        padding-top: 30px;
        font-size: 16px;
        font-family: PingFang SC;
        text-align: center;
    }

    .person-center-photo{
        width: 80%;
        border: 1px solid lightgray;
        margin-left: 10%;
        margin-top: 20px;
        margin-bottom: 60px;
        height: 200px;

    }
    .person-center-photo-div{
        width: 99.5%;
        border-right: 1px solid lightgray;
    }
    .person-center-photo-btn{
        text-align: center;
    }

</style>