<template>
<div class="CompetitionListPage">
    <CompetitionList v-bind:finfo="info" ></CompetitionList>    
</div>
</template>

<script>
    import CompetitionList from './CompetitionList'    
    export default {
        components:{
            CompetitionList,            
        },
        data:function () {
            return {
                info:{
                typename:'',
                type:"比赛类型",
                list:"比赛列表",
                },
            }             
            },
        }
</script>

<style>
</style>