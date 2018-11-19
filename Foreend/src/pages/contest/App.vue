<template><div id="app">
    <el-container>
        <el-header>
            <NavigationBar :username="username"></NavigationBar>
        </el-header>

        <el-main>
            <CompetitionListPage></CompetitionListPage>
        </el-main>
    </el-container>
    </div>
</template>

<script>
    import Vue from 'vue'
    import 'element-ui/lib/theme-chalk/index.css'
    import ElementUI from 'element-ui'
    Vue.use(ElementUI);    

    import NavigationBar from "../../components/NavigationBar";
    import CompetitionListPage from '../../components/CompetitionListPage'
    export default {
        props:['username','pageTotal'],
        components: {NavigationBar,CompetitionListPage}
    }
</script>

<style>
</style>