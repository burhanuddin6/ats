define a scr/index.js file
>>> npm init -y # this will create a package.json
>>> npm install react react-dom babel 
>>> npm install --save-dev webpack webpack-cli
>>> npm install -D babel-loader @babel/core @babel/preset-env @babel/preset-react webpack

create a webpack.config.js file and add these lines for the babel-loader

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
    }
  ]
}


open the package.json file and add
"scripts": {
	"build": "webpack"
	},
	

create a .babelrc file and add the following lines

{
    "presets": [
        "@babel/preset-env", 
        ["@babel/preset-react", {"runtime": "automatic"}]
    ]
}

# note that @babel/preset-react is also install (I have included it in above command but usually its not there)
# the automatic thing helps in including everything at runtime? Not sure but important
https://stackoverflow.com/questions/32070303/uncaught-referenceerror-react-is-not-defined

For CSS:
We need to use the css-loader
>>> npm install --save-dev css-loader style-loader

module.exports = {
  module: {
    rules: [
      {
        test: /\.css$/i,
        use: ["style-loader", "css-loader"],
      },npm
    ],
  },
};


For better scripts:
>>> npm install react-scripts # not used yet

This will display some warning of bad code. Refer to this
https://stackoverflow.com/questions/71282206/github-dependabot-alert-inefficient-regular-expression-complexity-in-nth-check
it says to add react-scripts to devDependencies in package.json




