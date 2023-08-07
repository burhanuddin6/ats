module.exports = {
    mode: 'development',
    entry: './src/index.js', 
    module: {
        rules: [
          {
            test: /\.(?:js|mjs|cjs)$/,
            exclude: /node_modules/,
            use: {
              loader: 'babel-loader',
              options: {
                presets: [
                  ['@babel/preset-env', { targets: "defaults" }]
                ]
              }
            }
          },
          {
            test: /\.css$/i,
            use: ["style-loader", "css-loader"],
          },
        ]
    },
    
    output: {
        filename: 'main.js',
        path: __dirname + '/dist',
    },
}