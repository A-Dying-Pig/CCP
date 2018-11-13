<template>
    <el-upload
            class="upload-file"
            action="https://jsonplaceholder.typicode.com/posts/"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :before-remove="beforeRemove"
            :before-upload="beforeFileUpload"
            multiple
            :limit="file_max_number"
            :on-exceed="handleExceed"
            :file-list="fileList">
        <el-button size="small" type="primary">点击上传</el-button>
        <div slot="tip" class="el-upload__tip"></div>
    </el-upload>
</template>


<script>

    //before upload 用来限制文件的大小和格式
    export default {
        props:{
            file_max_number:{
                type:Number,
                default:2
            },
            file_max_size:{
                type:Number,
                default:1 //unit:M
            }
        },
        data() {
            return {
                is_wrong:false,
                fileList:[]
            };
        },
        methods: {
            handleRemove(file, fileList) {
                console.log(file, fileList);
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
            beforeFileUpload(file){
                const isLt = file.size / 1024 / 1024 <= this.file_max_size;
                if(!isLt){
                    this.$message.error(`上传文件大小不能超过 ${this.file_max_size} MB!`);
                    this.is_wrong = true;
                }
                return isLt;
            }
        }
    }


</script>