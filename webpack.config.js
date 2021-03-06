/**
  * Webpack configuration
  *
  * Author: Luca Vizzarro <2252593v@student.gla.ac.uk>
  * Dev Team: WAD2 Lab 9 Team A
  */

const path = require('path');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const { EnvironmentPlugin } = require("webpack");

function inProduction() { return process.env.NODE_ENV == "production"; }
function inDevelopment() { return process.env.NODE_ENV == "development"; }

var config = {
  entry: './resources/js/index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'static/js')
  },
  plugins: [
    new ExtractTextPlugin("../css/bundle.css"),
    new EnvironmentPlugin(['NODE_ENV'])
  ],
  module: {
    rules: [{
      test: /\.scss$/,
      use: ExtractTextPlugin.extract({
        fallback: "style-loader",
        use: [
          {
            loader: 'css-loader',
            options: {
              sourceMap: inDevelopment() ? true : false,
              minimize: true
            }
          },
          {
            loader: 'postcss-loader',
            options: {
              plugins: function () {
                return [
                  require('precss'),
                  require('autoprefixer')
                ];
              },
              sourceMap: inDevelopment() ? true : false
            }
          },
          {
            loader: 'sass-loader',
            options: {
              sourceMap: inDevelopment() ? true : false
            }
          }]
      })
    }, {
      test: /\.(gif|png|jpe?g|svg)$/i,
      use: [
        'url-loader',
        'img-loader'
      ]
    }]
  }
};

if(inDevelopment()) {
  config.devtool = 'inline-source-map';
  config.optimization = {
     minimize: false
   }
}

module.exports = config;
