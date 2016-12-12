module.exports = {
    entry: './static/global/ts/main.ts',
    output: {
        filename: 'bundle.js',
        path: '/dist'
    },
    resolve: {
        extensions: ['', '.webpack.js', '.web.js', '.ts', '.js']
    },
    module: {
        loaders: [
            {
                test: /\.ts$/,
                loader: 'ts-loader'
            }
        ]
    }
};
