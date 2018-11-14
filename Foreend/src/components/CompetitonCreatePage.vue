<template><div class="CompetitionCreatePage">
<CompetitionInfo typeid="1">比赛基本信息</CompetitionInfo>
</div></template>
<script>
    import CompetitionInfo from './CompetitionInfo'
    export default {
        components:{CompetitionInfo},
        data:function () {
            return {
                allinfo:{
                  basicinfo:{},
                  signupinfo:{},
                  //TODO stages
                },
            }
        }
    }
</script>
<style></style>