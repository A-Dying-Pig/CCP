<template>
    <el-table :data="grades.filter(data => !search || (data.grade==search))" style="width: 100%">
        <el-table-column type="expand" >
            <template slot-scope="props">
                <GradeProject :contestid="contestid" :readonly="true" :participantid="props.row.participantid" :participantgrade="props.row.grade"></GradeProject>
            </template>
        </el-table-column>
        <el-table-column type="index" width="180">

        </el-table-column>
        <el-table-column prop="grade" label="分数" sortable width="180">

        </el-table-column>
        <el-table-column>
            <template slot="header"  slot-scope="scope">
                <el-input
                        v-model="search"
                        size="mini"
                        placeholder="输入分数"/>
            </template>
        </el-table-column>
    </el-table>
</template>

<script>
    import GradeProject from './GradeProject'
    import axios from 'axios'
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.headers.common = {
        'X-CSRFToken':document.querySelector('#csrf-token input').value,
        'X-Requested-With': 'XMLHttpRequest'
    };
    export default {
        name: "JudgeFinish",
        props:['contestid'],
        components:{GradeProject},
        data:function () {
            return{
                grades:[{participantid:1,grade:80},{participantid:2,grade:60},{participantid:3,grade:100}],
                search:'',
            }
        },
        created:function () {
            this.grades = [];
            axios.post('/api/judge/finished',{
                contestid:this.contestid
            }).then(function (response) {
                this.grades = response.data.grades;
            })
        }
    }
</script>

<style scoped>

</style>