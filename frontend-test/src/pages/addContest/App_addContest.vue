<template><div id="app">
    <el-container>
        <el-header>
            <NavigationBar :username="musername"></NavigationBar>
        </el-header>
        <el-main>
            <CompetitionCreatePage></CompetitionCreatePage>
        </el-main>
    </el-container>
    </div>
</template>
<script>
    import CompetitionCreatePage from '../../components/CompetitionCreatePage';
    import NavigationBar from "../../components/NavigationBar";
    export default {
        props:{
            'musername':{
                type:String,
                default:''
            }
        },
        components: {NavigationBar,CompetitionCreatePage}
    }
</script>
<style></style>