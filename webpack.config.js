// Webpack configuration for sphinx-book-theme
const { resolve } = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin"); // Compile our translation files
const { exec } = require("child_process");
exec("python src/sphinx_book_theme/_compile_translations.py");

// Paths for various assets (sources and destinations)
const staticPath = resolve(
  __dirname,
  "src/sphinx_book_theme/theme/sphinx_book_theme/static",
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
  optimization: { minimizer: ["...", new CssMinimizerPlugin()] },
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: [
          { loader: MiniCssExtractPlugin.loader },
          // Interprets `@import` and `url()` like `import/require()` and will resolve them
          {
            loader: "css-loader",
            options: {
              sourceMap: true,
              url: false,
            },
          },
          {
            // Loads a SASS/SCSS file and compiles it to CSS
            loader: "sass-loader",
            options: {
              sourceMap: true,
              sassOptions: { outputStyle: "expanded" },
            },
          },
        ],
      },
    ],
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: "styles/[name].css",
    }),
  ],
};
