var path = require('path')
var webpack = require('webpack')
const VueLoaderPlugin = require('vue-loader/lib/plugin')

module.exports = {
  entry: './src/main.js',
  output: {
    path: path.resolve(__dirname, './dist'),
    publicPath: '/dist/',
    filename: 'build.js'
  },
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js',
      '@': path.resolve(__dirname, 'src'),
        'pdf': 'react-pdf/build/entry.noworker'
    }
  },
  mode:'development',
  plugins:[
	new VueLoaderPlugin()
  ],
  module: {
    rules: [
        // {
        //     test: /\.vue$/,
        //     //loader: 'vue-loader'
        //     loader: 'remove-hashbag-loader',
        //     include: [ path.resolve(__dirname, '') ],
        // },
      {
        test: /\.vue$/,
        loader:'vue-loader',
          exclude: /node_modules/,
          include: [ path.resolve(__dirname, '') ],
      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/
      },
      {
        test: /\.(png|jpg|gif|svg)$/,
        loader: 'file-loader',
        options: {
          name: '[name].[ext]?[hash]'
        },
      },
        {
            test: /\.ts$/,
            exclude: /(node_modules|bower_components)/,
            loader: 'ts-loader'
        },
        { test: /\.(s)?css$/, loader: 'null-loader'}
    ]
  },
    resolveLoader: {
        alias: {
            "remove-hashbag-loader": path.join(__dirname, "remove-hashbag-loader")
        }
    },
  devServer: {
    historyApiFallback: true,
    noInfo: true
  },
  performance: {
    hints: false
  },
  devtool: '#eval-source-map'
}

if (process.env.NODE_ENV === 'production') {
  module.exports.devtool = '#source-map'
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"production"'
      }
    }),
    new webpack.optimize.UglifyJsPlugin({
      sourceMap: true,
      compress: {
        warnings: false
      }
    }),
    new webpack.LoaderOptionsPlugin({
      minimize: true
    })
  ])
}

// test specific setups
if (process.env.NODE_ENV === 'test') {
  module.exports.externals = [require('webpack-node-externals')()]
  module.exports.devtool = 'eval'
}