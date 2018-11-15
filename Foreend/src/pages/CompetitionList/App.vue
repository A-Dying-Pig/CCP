<template><div id="app">
    <el-container>
        <el-header>
            <NavigationBar></NavigationBar>
        </el-header>

        <el-main>
            <el-row>
            <el-col :span="24" class="banner">比赛分类</el-col>
            </el-row>

            <el-row>
            <competitionList title="比赛列表"></competitionList>
            </el-row>            
        </el-main>
    </el-container>
    </div>
</template>

<script>    
    import NavigationBar from "../../components/NavigationBar";
    import CompetitionList from '../../components/CompetitionList'
    export default {
        components: {NavigationBar,CompetitionList}
    }
</script>

<style>
.banner{
    font-size:20px;
    text-align: left;
    font-family: "PingFang SC";
    padding: 70px 0px 0px 0px;
    text-weight:bold;
  }
</style>