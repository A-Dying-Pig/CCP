<template>
    <div>
    <el-table :data="files" style="width: 100%;">
        <el-table-column label="文件名" prop="name"></el-table-column>
        <el-table-column label="文件大小" prop="size"></el-table-column>
        <el-table-column>
            <template slot-scope="scope">
                <a :download="scope.row.name" :href="scope.row.url"><el-button size="mini">下载</el-button></a>
            </template>
        </el-table-column>

    </el-table>
        <UploadFile :contestid="contestid" :uploadurl="'/api/admin/upload'" v-if="type === 3" :uploaddata="{contestid:contestid}"></UploadFile>
    </div>
</template>

<script>
    import axios from 'axios'
    import UploadFile from './UploadFile.vue'
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.headers.common = {
        'X-CSRFToken':document.querySelector('#csrf-token input').value,
        'X-Requested-With': 'XMLHttpRequest'
    };
    export default {
        name: "CompetitionFiles",
        props:['contestid','type'],
        components:{UploadFile},
        data:function () {
            return{
                files:[
                ],
                fileList:[],
            }
        },
        methods:{
            handleDownload:function (idx, row) {
                console.log(row);
                //window.open(row.url);
            },
            submitUpload() {
                    this.$refs.upload.submit();
                },
            handleRemove(file, fileList) {
                    console.log(file, fileList);
                },
            handlePreview(file) {
                    console.log(file);
                },
            loadok(response, file, fileList){
                this.getfile();
                console.log('loadok')
            },
            getfile(){
                let self = this;
                axios.post('/api/competition/filelist',{
                    contestid:self.contestid,
                }).then(function (response) {
                    self.files = [];
                    self.files = response.data.files;
                    console.log(self.files);
                }).catch(function (error) {
                    console.log(error);
                })
            }
        },
        created:function () {
            this.getfile();
        }
    }
</script>

<style scoped>

</style>