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
        props:['pagetotal'],
        data:function () {
            return {
                info:{
                    typename:'',
                    type:"比赛类型",
                    list:"比赛列表",
                },
                page:{
                    total:14,
                    //this.pagetotal,
                    pagenumber:1,
                }
            }             
            }
        }
</script>

<style>
</style>