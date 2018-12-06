<template>
    <el-row>
        <el-col :offset="3" :span="18">
<el-tabs type="border-card" value="details">
    <el-tab-pane label="比赛详情" name="details"><slot name="details"></slot></el-tab-pane>
    <el-tab-pane v-for="item in showlist" :key="item.key" :label="item.label" :name="item.value">
        <template v-if="item.value == 'gradework'">
            <GradeProject :contestid="contestid" :stageinfo="info.stageinfo" :readonly="false"></GradeProject>
        </template>
        <template v-else-if="item.value === 'submitwork'">
            <UploadFile :file_max_number="1" :file_max_size="100" :uploadurl="'/api/contestant/submit'"></UploadFile>
        </template>
        <template v-else-if="item.value === 'infochange'">
            <CompetitionCreatePage :contestid="contestid" :info="info" :change="true"></CompetitionCreatePage>
        </template>
        <template v-else-if="item.value === 'participantstable'">
            <ParticipantsTable :contestid="contestid"></ParticipantsTable>
        </template>
        <template v-else-if="item.value === 'judgelist'">
            <JudgeList :contestid="contestid"></JudgeList>
        </template>
        <template v-else-if="item.value === 'advancedparticipants'">
            <AdvancedParticipants :contestid="contestid"> </AdvancedParticipants>
        </template>
        <template v-else-if="item.value == 'judgefinish'">
            <JudgeFinish :contestid="contestid"></JudgeFinish>
        </template>
        <template v-else-if="item.value == 'competitionfiles'">
            <CompetitionFiles :contestid="contestid" :type="type"></CompetitionFiles>
        </template>
        <template v-else-if="item.value == 'judgeprogress'">
            <JudgeProgress :contestid="contestid" :type="type"></JudgeProgress>
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
    import AdvancedParticipants from './AdvancedParticipants'
    import JudgeFinish from './JudgeFinish'
    import CompetitionFiles from './CompetitionFiles'
    import JudgeProgress from './JudgeProgress'
    export default {
        components:{JudgeList, ParticipantsTable, GradeProject,UploadFile,CompetitionCreatePage,JudgeFinish,CompetitionFiles,AdvancedParticipants,JudgeProgress},
        props:['info','showlist','contestid','type'],
        data:function () {
            return{
                showlists:this.showlist
            }
        },
    }
</script>