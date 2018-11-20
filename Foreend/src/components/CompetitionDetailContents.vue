<template>
    <el-row :gutter="20">
        <el-col :offset="5" :span="14">
<el-tabs type="border-card" value="details">
    <el-tab-pane label="比赛详情" name="details"><slot name="details"></slot></el-tab-pane>
    <el-tab-pane v-for="item in showlists" :key="item.key" :label="item.label" :name="item.value">
        <template v-if="item.value == 'gradework'">
            <GradeProject></GradeProject>
        </template>
        <template v-else-if="item.value == 'submitwork'">
            <UploadFile :file_max_number="5" :file_max_size="50"></UploadFile>
        </template>
        <template v-else-if="item.value == 'infochange'">

        </template>
        <template v-else-if="item.value == 'participantstable'">
            <ParticipantsTable :contestId="contestId"></ParticipantsTable>
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
    export default {
        components:{ParticipantsTable, GradeProject,UploadFile},
        props:['info','showlist','contestId'],
        data:function () {
            return{
                showlists:this.showlist
            }
        }
    }
</script>