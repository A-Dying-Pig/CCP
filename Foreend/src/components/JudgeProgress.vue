<template>
    <el-row type="flex" justify="center">
        <el-col>
            <el-table :data="judges" style="width: 100%">
                <el-table-column prop="name" label="评委名称" width="180"></el-table-column>
                <el-table-column prop="sum" label="总评测数" width="180"></el-table-column>
                <el-table-column prop="finish" label="已评测数" width="180"></el-table-column>
                <el-table-column label="评测进度" width="180">
                    <template slot-scope="scope">
                        <div>
                            <el-progress v-if="scope.row.finish/scope.row.sum*100<50" :text-inside="true" :stroke-width="18" :percentage="scope.row.finish/scope.row.sum*100" status="exception"></el-progress>
                            <el-progress v-else-if="scope.row.finish/scope.row.sum*100===100" :text-inside="true" :stroke-width="18" :percentage="scope.row.finish/scope.row.sum*100" status="success"></el-progress>
                            <el-progress v-else :text-inside="true" :stroke-width="18" :percentage="scope.row.finish/scope.row.sum*100"></el-progress>
                        </div>
                    </template>
                </el-table-column>
            </el-table>
        </el-col>
    </el-row>
</template>

<script>
    import axios from 'axios'
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.headers.common = {
        //'X-CSRFToken':document.querySelector('#csrf-token input').value,
        'X-Requested-With': 'XMLHttpRequest'
    };
    export default {
        name: "JudgeProgress",
        props:['contestid'],
        data:function () {
            return{
                judges:[]
            }
        },
        created:function () {
            let self = this;
            self.judges.push({
                name:'评委1',
                sum:100,
                finish:75
            },{
                name:'评委2',
                sum:100,
                finish:100
            },{
                name:'评委3',
                sum:100,
                finish:30
            });
            axios.post('/api/admin/judgeprogress',{
                contestid:self.contestid
            }).then(function (response) {
                self.judges = [];
                if(response.data.msg!==''){
                    self.$message({
                        message:response.data.msg,
                        type:'error'
                    });
                    return;
                }
                self.judges = response.data.judges;
            }).catch(function (error) {
                self.$message({
                    message:'获取评委进度失败！',
                    type:'error'
                });
            })
        }
    }
</script>

<style scoped>

</style>