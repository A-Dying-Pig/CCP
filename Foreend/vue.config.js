module.exports = {
  pages: {
	  index: {
          entry: 'src/pages/index/main.js',
          template: 'src/pages/index/index.html',
          filename: 'index.html',
      },
      CompetitionCreate:{
          entry: 'src/pages/CompetitonCreate/main.js',
          template: 'src/pages/CompetitonCreate/index.html',
          filename: 'CompetitonCreate.html',
      }
  },
    devServer:{
      index:'static/CompetitonCreate.html'
    },
  outputDir:'static',
  //indexPath:'./../templates/index.html',
}