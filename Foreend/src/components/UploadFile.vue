<template>
    <div>
    <el-upload
            action=""
            ref="upload"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :before-remove="beforeRemove"
            :before-upload="beforeFileUpload"
            multiple
            :limit="file_max_number"
            :on-exceed="handleExceed"
            :file-list="fileList">
        <el-button slot="trigger" size="small" type="primary">选择文件</el-button>
        <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">上传到服务器</el-button>
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
            }
        },
        data() {
            return {
                is_wrong:false,
                fileList:[],
                fileobjs:[]
            };
        },
        methods: {
            handleRemove(file, fileList) {
                for(let idx in this.fileobjs){
                    if(this.fileobjs[idx].name===file.name){
                        console.log(this.fileobjs[idx].name+' deleted');
                        this.fileobjs.splice(idx,1);
                        break;
                    }
                }
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
            submitUpload(){
                let self = this;
                let failnum = 0;
                if(self.fileobjs.length === 0){
                    self.$message({
                        message:'没有文件可上传！',
                        type:'error'
                    })
                    return;
                }
                for(let fileobj of self.fileobjs){
                    let fd = new FormData();
                    fd.append('file',fileobj);
                    fd.append('contestid',this.contestid);
                    axios.post(self.uploadurl,fd,{

                    }).then(function (response) {
                        let msg = response.data.msg;
                        if(msg!==''){
                            self.$message({
                                message:'上传'+fileobj.name+'失败！',
                                type:'error'
                            });
                            failnum = failnum + 1;
                        }
                    }).catch(function (error) {
                        self.$message({
                            message:'上传'+fileobj.name+'失败！',
                            type:'error'
                        });
                        failnum = failnum + 1;
                    });
                }
                if(!failnum){
                    self.$message({
                        message:'上传成功！',
                        type:'success'
                    })
                }
                self.fileobjs = [];
                self.fileList = [];
            },
            beforeFileUpload(file){
                let self = this;
                const isLt = file.size / 1024 / 1024 <= this.file_max_size;
                if(!isLt){
                    this.$message.error(`上传文件大小不能超过 ${this.file_max_size} MB!`);
                    this.is_wrong = true;
                    return;
                }
                self.fileobjs.push(file);
                return isLt;
            }
        }
    }


</script>