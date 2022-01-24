// Webpack configuration for sphinx-book-theme
const { resolve } = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const OptimizeCssAssetsPlugin = require("optimize-css-assets-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");
const dedent = require("dedent");

// Paths for various assets (sources and destinations)
const staticPath = resolve(
  __dirname,
  "src/sphinx_book_theme/theme/sphinx_book_theme/static"
);

//
// Cache-busting Jinja2 macros (`webpack-macros.html`) used in `layout.html`
//
function macroTemplate({ compilation }) {
  const hash = compilation.hash;
  const css_files = ["styles/sphinx-book-theme.css"];
  const js_files = ["scripts/sphinx-book-theme.js"];

  function stylesheet(css) {
    return `<link href="{{ pathto('_static/${css}', 1) }}?digest=${hash}" rel="stylesheet">`;
  }

  function script(js) {
    return `<script src="{{ pathto('_static/${js}', 1) }}?digest=${hash}"></script>`;
  }
  return dedent(`\
    <!--
      All these macros are auto-generated and must **NOT** be edited by hand.
      See the webpack.config.js file, to learn more about how this is generated.
    -->
    {% macro head_pre_bootstrap() %}
      ${css_files.map(stylesheet).join("\n  ")}
    {% endmacro %}

    {% macro body_post() %}
      ${js_files.map(script).join("\n  ")}
    {% endmacro %}
  `)
}

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
    minimize: true,
    minimizer: [new TerserPlugin({sourceMap: true}), new OptimizeCssAssetsPlugin({})],
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
  plugins: [
    new HtmlWebpackPlugin({
      filename: resolve(staticPath, "sbt-webpack-macros.html"),
      inject: false,
      minify: false,
      css: true,
      templateContent: macroTemplate,
    })
  ]
};
