<template>
    <div id="app"><NavigationBar></NavigationBar><CompetitionCreatePage></CompetitionCreatePage></div>
</template>
<script>
    import CompetitionCreatePage from '../../components/CompetitonCreatePage';
    import NavigationBar from "../../components/NavigationBar";
    export default {
        components: {NavigationBar,CompetitionCreatePage}
    }
</script>
<style></style>