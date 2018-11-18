<template>
<div class="CompetitionListPage">
    <CompetitionList :finfo="info"
                     :current_page_num="current_page_num"
                     :total_page_num="total_page_num"
                     :array="array"></CompetitionList>
</div>
</template>

<script>
    import CompetitionList from './CompetitionList'    
    export default {
        components: {
            CompetitionList,
        },
        props: ['pagetotal'],
        data: function () {
            return {
                info: {
                    typename: '',
                    type: "比赛类型",
                    list: "比赛列表",
                },
                current_page_num: 1,
                total_page_num: this.pagetotal,
                array: [{
                    title: '',
                    intro: '',
                    contestId: 0,
                    img_url: ''
                }],
            }
        }
    }
</script>

<style>
</style>