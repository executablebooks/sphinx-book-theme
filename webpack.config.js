// Webpack configuration for sphinx-book-theme
const { resolve } = require("path");
const OptimizeCssAssetsPlugin = require("optimize-css-assets-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");

// Paths for various assets (sources and destinations)
const staticPath = resolve(
  __dirname,
  "src/sphinx_book_theme/theme/sphinx_book_theme/static"
);

module.exports = {
  mode: "production",
  devtool: "source-map",
  entry: {
    "sphinx-book-theme": ["./src/sphinx_book_theme/assets/scripts/index.js"],
  },
  output: {
    filename: "scripts/[name].js",
    path: staticPath,
  },
  optimization: {
    minimizer: [new TerserPlugin(), new OptimizeCssAssetsPlugin({})],
  },
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: [
          {
            loader: "file-loader",
            options: {
              name: "styles/sphinx-book-theme.css",
            },
          },
          {
            loader: "extract-loader",
          },
          {
            // Use the css-loader with url()-inlining turned off.
            loader: "css-loader?-url",
          },
          {
            loader: "sass-loader",
          },
        ],
      },
    ],
  },
};
