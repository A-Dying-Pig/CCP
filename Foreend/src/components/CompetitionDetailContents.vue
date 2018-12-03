<template>
    <el-row :gutter="20">
        <el-col :offset="5" :span="14">
<el-tabs type="border-card" value="details">
    <el-tab-pane label="比赛详情" name="details"><slot name="details"></slot></el-tab-pane>
    <el-tab-pane v-for="item in showlist" :key="item.key" :label="item.label" :name="item.value">
        <template v-if="item.value == 'gradework'">
            <GradeProject :contestid="contestid" :stageinfo="info.stageinfo" :readonly="false"></GradeProject>
        </template>
        <template v-else-if="item.value == 'submitwork'">
            <UploadFile :file_max_number="5" :file_max_size="50"></UploadFile>
        </template>
        <template v-else-if="item.value == 'infochange'">
            <CompetitionCreatePage :contestid="contestid" :info="info" :change="true"></CompetitionCreatePage>
        </template>
        <template v-else-if="item.value == 'participantstable'">
            <ParticipantsTable :contestid="contestid"></ParticipantsTable>
        </template>
        <template v-else-if="item.value == 'judgelist'">
            <JudgeList :contestid="contestid"></JudgeList>
        </template>
        <template v-else-if="item.value == 'judgefinish'">
            <JudgeFinish :contestid="contestid"></JudgeFinish>
        </template>
    </el-tab-pane>
</el-tabs>
        </el-col>
    </el-row>
</template>

<script>
    import GradeProject from './GradeProject'
    import UploadFile from './UploadFile'
    import ParticipantsTable from  './ParticipantsTable'
    import CompetitionCreatePage from './CompetitionCreatePage'
    import JudgeList from './JudgeList'
    import JudgeFinish from './JudgeFinish'
    export default {
        components:{JudgeList, ParticipantsTable, GradeProject,UploadFile,CompetitionCreatePage,JudgeFinish},
        props:['info','showlist','contestid'],
        data:function () {
            return{
                showlists:this.showlist
            }
        },
    }
</script>