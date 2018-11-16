<template>
<div class="CompetitionListPage">
    <CompetitionList :finfo="info"
                     :fpage="page"></CompetitionList>
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
                page:{
                    pagetotal:100,
                    pagenumber:1
                }
            }             
            },
        }
</script>

<style>
</style>