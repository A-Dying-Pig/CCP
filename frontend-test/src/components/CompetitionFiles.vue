<template>
    <div>
    <el-table :data="files" style="width: 100%;">
        <el-table-column label="文件名" prop="name"></el-table-column>
        <el-table-column label="文件大小" prop="size"></el-table-column>
        <el-table-column>
            <template slot-scope="scope">
                <a download="file.txt" :href="scope.row.url"><el-button size="mini">下载</el-button></a>
            </template>
        </el-table-column>

    </el-table>
        <UploadFile :contestid="contestid" :uploadurl="'/api/admin/upload'" v-if="type === 3"></UploadFile>
    </div>
</template>

<script>
    import axios from 'axios'
    import UploadFile from './UploadFile'
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
                    {
                        name:'1.pdf',
                        url:'http://math.sjtu.edu.cn/faculty/chengwang/files/2015fall/ch1.pdf',
                        size:'1b',
                    },
                    {
                        name:'2.jpg',
                        url:'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1543949343531&di=b7cc03cd964bb52e6ce10ea1aed433c8&imgtype=0&src=http%3A%2F%2Fimgsrc.baidu.com%2Fimage%2Fc0%253Dshijue1%252C0%252C0%252C294%252C40%2Fsign%3D8a953b1817950a7b6138468762b808ac%2F03087bf40ad162d9344e02321bdfa9ec8a13cd78.jpg',
                        size:'2b'
                    }
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
                }
        },
        created:function () {
            let self = this;
            axios.post('/api/competition/filelist',{
                contestid:self.contestid,
            }).then(function (response) {
                self.files = response.data.files;
                console.log(self.files);
            }).catch(function (error) {
                console.log(error);
            })
        }
    }
</script>

<style scoped>

</style>