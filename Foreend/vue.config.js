module.exports = {
  pages: {
      test:{
          entry: 'src/pages/test/main.js',
          template:'src/pages/test/test.html',
          filename:'test.html',
      },
      index: {
          entry: 'src/pages/index/main.js',
          template: 'src/pages/index/index.html',
          filename: 'index.html',
      }
  },
  outputDir:'static',
  indexPath:'./../templates/index.html',
}