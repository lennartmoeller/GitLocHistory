const path = require('path')

const FileManagerPlugin = require('filemanager-webpack-plugin');
const ForkTsCheckerWebpackPlugin = require('fork-ts-checker-webpack-plugin')
const sveltePreprocess = require('svelte-preprocess')

const mode = process.env.NODE_ENV || 'development'
const prod = mode === 'production'

module.exports = {
	entry: path.resolve(__dirname, "src/main.ts"),
	resolve: {
		alias: {
			svelte: path.dirname(require.resolve('svelte/package.json'))
		},
		extensions: ['.mjs', '.js', '.ts', '.svelte'],
		mainFields: ['svelte', 'browser', 'module', 'main'],
		conditionNames: ['svelte', 'module', 'import', 'require']
	},
	output: {
		filename: "[name].js",
		path: path.resolve(__dirname, 'dist')
	},
	module: {
		rules: [
			// TYPESCRIPT
			{
				test: /\.ts$/,
				loader: 'ts-loader',
				exclude: /node_modules/
			},
			// BABEL
			{
				test: /\.(js|ts|svelte)$/,
				exclude: /node_modules/,
				use: {
					loader: 'babel-loader',
					options: {
						presets: [
							'@babel/typescript',
							'@babel/preset-env'
						]
					}
				}
			},
			// SVELTE FILES
			{
				test: /\.svelte$/,
				use: {
					loader: 'svelte-loader',
					options: {
						compilerOptions: {
							dev: !prod
						},
						emitCss: false,
						hotReload: !prod,
						preprocess: sveltePreprocess({
							scss: {
								renderSync: true
							}
						})
					}
				}
			},
			// SVELTE BUG FIX
			{
				test: /node_modules\/svelte\/.*\.mjs$/,
				resolve: {
					fullySpecified: false
				}
			},
			// EXTERNAL STYLESHEET FILES
			{
				test: /\.s[ac]ss$/i,
				use: [
					"style-loader",
					"css-loader",
					"sass-loader",
				],
			}
		]
	},
	mode,
	plugins: [
		new ForkTsCheckerWebpackPlugin(),
		new FileManagerPlugin({
			events: {
				onEnd: {
					mkdir: ['./release', './release/dist'],
					copy: [
						{
							source: './internals',
							destination: './release/internals',
						},
						{
							source: './config.json',
							destination: './release/config.json',
						},
						{
							source: './glh.py',
							destination: './release/glh.py',
						},
						{
							source: './requirements.txt',
							destination: './release/requirements.txt',
						},
						{
							source: './viewer.html',
							destination: './release/viewer.html',
						},
						{
							source: './dist/main.js',
							destination: './release/dist/main.js',
						},
						{
							source: './dist/main.js.LICENSE.txt',
							destination: './release/dist/main.js.LICENSE.txt'
						},
					],
				},
			},
		})
	]
}
