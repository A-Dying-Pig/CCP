<template>
    <el-row>
        <el-col :offset="3" :span="18">
<el-tabs type="border-card" value="details">
    <el-tab-pane label="比赛详情" name="details"><slot name="details"></slot></el-tab-pane>
    <el-tab-pane v-for="item in showlist" :key="item.key" :label="item.label" :name="item.value">
        <template v-if="item.value === 'gradework'">
            <GradeProject :contestid="contestid" :stageinfo="info.stageinfo" :readonly="false"></GradeProject>
        </template>
        <template v-else-if="item.value === 'submitwork'">
            <ParticipantUpload :contestid="contestid"></ParticipantUpload>
        </template>
        <template v-else-if="item.value === 'infochange'">
            <CompetitionCreatePage :contestid="contestid" :info="info" :change="true"></CompetitionCreatePage>
        </template>
        <template v-else-if="item.value === 'participantstable'">
            <ParticipantsTable :contestid="contestid"></ParticipantsTable>
        </template>
        <template v-else-if="item.value === 'judgelist'">
            <JudgeList :contestid="contestid" :judgebeginbutton="info.basicinfo.beginjudgebutton"></JudgeList>
        </template>
        <template v-else-if="item.value === 'advancedparticipants'">
            <AdvancedParticipants :contestid="contestid"> </AdvancedParticipants>
        </template>
        <template v-else-if="item.value === 'judgefinish'">
            <JudgeFinish :contestid="contestid"></JudgeFinish>
        </template>
        <template v-else-if="item.value === 'competitionfiles'">
            <CompetitionFiles :contestid="contestid" :type="type"></CompetitionFiles>
        </template>
        <template v-else-if="item.value === 'judgeprogress'">
            <JudgeProgress :contestid="contestid" :type="type"></JudgeProgress>
        </template>
        <template v-else-if="item.value === 'discussion'">
            <DiscussionMain :contestid="contestid" :width="width"></DiscussionMain>
        </template>
    </el-tab-pane>
</el-tabs>
        </el-col>
    </el-row>
</template>

<script>
    import GradeProject from './GradeProject.vue'
    import ParticipantsTable from  './ParticipantsTable.vue'
    import CompetitionCreatePage from './CompetitionCreatePage.vue'
    import JudgeList from './JudgeList.vue'
    import AdvancedParticipants from './AdvancedParticipants.vue'
    import JudgeFinish from './JudgeFinish.vue'
    import CompetitionFiles from './CompetitionFiles.vue'
    import JudgeProgress from './JudgeProgress.vue'
    import DiscussionMain from './DiscussionMain.vue'
    import ParticipantUpload from './ParticipantUpload.vue'
    export default {
        components:{
            ParticipantUpload,
            JudgeList, ParticipantsTable, GradeProject,CompetitionCreatePage,JudgeFinish,CompetitionFiles,AdvancedParticipants,JudgeProgress,DiscussionMain},
        props:['info','showlist','contestid','type'],
        data:function () {
            return{
                showlists:this.showlist,
                width:window.innerWidth*0.7,
            }
        },
        mounted:function () {
            let self = this;
            console.log(self.showlist)
            window.onresize = function resize(){
                self.width = window.innerWidth*0.7;
            }
        }
    }
</script>