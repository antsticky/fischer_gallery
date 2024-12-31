const HtmlWebpackPlugin = require("html-webpack-plugin");
const path = require("path");
const args = process.argv.slice(2);
const portArg = args.find(arg => arg.includes('--port='));
const PORT = portArg ? parseInt(portArg.split('=')[1], 10) : 3000;

module.exports = {
  entry: `./src/index.tsx`,
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "bundle.js",
    publicPath: "/", // Ensure this is set to the root path
  },
  devServer: {
    host: '0.0.0.0',
    port: PORT,
    static: {
      directory: path.join(__dirname, 'src/public'),
    },
    historyApiFallback: true,
    hot: true,
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: path.join(__dirname, `src/public/index.html`),
      filename: "index.html",
    }),
  ],
  module: {
    rules: [
      {
        test: /\.(ts|js)x?$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            presets: [
              "@babel/preset-env",
              "@babel/preset-react",
              "@babel/preset-typescript",
            ],
          },
        },
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"],
      },
      {
        test: /\.svg$/,
        issuer: /\.[jt]sx?$/,
        use: ["@svgr/webpack"], // Use SVGR to handle SVG as React components
      },
      {
        test: /\.scss$/,
        use: [
          "style-loader", // Injects styles into DOM
          "css-loader", // Turns CSS into JS
          "sass-loader", // Compiles Sass to CSS
        ],
      },
    ],
  },
  resolve: {
    extensions: [".js", ".jsx", ".ts", ".tsx"],
  },
};
