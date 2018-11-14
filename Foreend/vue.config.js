module.exports = {
  pages: {
	  index: {
          entry: 'src/pages/index/main.js',
          template: 'src/pages/index/index.html',
          filename: 'indexm.html',
      },
      CompetitionCreate:{
          entry: 'src/pages/CompetitonCreate/main.js',
          template: 'src/pages/CompetitonCreate/index.html',
          //filename: 'CompetitonCreate.html',
          filename: 'index.html',
      }
  },
    baseUrl:'',
  outputDir:'static',
  //indexPath:'./../templates/index.html',
}