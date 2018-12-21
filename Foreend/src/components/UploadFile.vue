<template>
    <div>
    <el-upload
            :action="uploadurl"
            ref="upload"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :before-remove="beforeRemove"
            :before-upload="beforeFileUpload"
            multiple
            :limit="file_max_number"
            :on-exceed="handleExceed"
            :auto-upload="true"
            :http-request="submitUpload"
            :file-list="fileList">
        <el-button slot="trigger" size="small" type="primary">上传文件</el-button>
        <!--<el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">上传到服务器</el-button>-->
        <div slot="tip" class="el-upload__tip"></div>
    </el-upload>
    </div>
</template>
<script>
    import axios from 'axios'
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.headers.common = {
        'X-CSRFToken':document.querySelector('#csrf-token input').value,
        'X-Requested-With': 'XMLHttpRequest'
    };
    //before upload 用来限制文件的大小和格式
    export default {
        props:{
            file_max_number:{
                type:Number,
                default:10
            },
            file_max_size:{
                type:Number,
                default:100 //unit:M
            },
            contestid:{
                type:Number,
                default:-1
            },
            uploadurl:{
                type:String,
                default:''
            },
            accept:{
                type:String,
                default:'all'
            },
            needname:{
                type:Boolean,
                default:true
            },
            uploadinfo:{
                type:Object,
                default:function () {
                    return {}
                }
            },
            fileList:{
                type:Array,
            }
        },
        data() {
            return {
                is_wrong:false,
            };
        },
        methods: {
            handleRemove(file, fileList) {
            },
            handlePreview(file) {
                console.log(file);
            },
            handleExceed(files, fileList) {
                this.$message.warning(`当前限制选择 ${this.file_max_number} 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`);
            },
            beforeRemove(file, fileList) {
                if(this.is_wrong === false){
                    return this.$confirm(`确定移除 ${ file.name }？`);
                }
                else{
                    this.is_wrong = false;
                }

            },
            submitUpload(param){
                let fileobj = param.file;
                let self = this;
                let failnum = 0;
                console.log(fileobj);
                if(self.needname === true){
                    if(self.uploadinfo.name===''){
                        self.$message({
                            message:'请输入名称！',
                            type:'error'
                        });
                        return false;
                    }
                }

                let fd = new FormData();
                fd.append('file',fileobj);
                fd.append('contestid',self.contestid);
                if(self.needname === true){
                    fd.append('name',self.uploadinfo.name)
                }
                axios.post(self.uploadurl,fd,{
                }).then(function (response) {
                    let msg = response.data.msg;
                    if(msg!==''){
                        self.$message({
                            message:'上传'+fileobj.name+'失败！',
                            type:'error'
                        });
                    }
                    else {
                        self.$message({
                            message:'上传'+fileobj.name+'成功！',
                            type:'success'
                        });
                    }
                }).catch(function (error) {
                    self.$message({
                        message:'上传'+fileobj.name+'失败！',
                        type:'error'
                    });
                });
            },
            beforeFileUpload(file){
                let self = this;
                const isLt = file.size / 1024 / 1024 <= this.file_max_size;
                if(!isLt){
                    this.$message.error(`上传文件大小不能超过 ${this.file_max_size} MB!`);
                    this.is_wrong = true;
                    return;
                }
                if(self.accept === 'zip'){
                    if((!file.name.endsWith('zip'))&&(!file.name.endsWith('rar'))){
                        this.$message.error(`只支持rar或者zip格式文件的上传!`);
                        this.is_wrong = true;
                        return;
                    }
                }
                return isLt;
            }
        },
        created:function () {
            console.log(this.fileList)
        }
    }


</script>