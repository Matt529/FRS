var webpack = require('webpack');

module.exports = {
    entry: './static/global/ts/main.ts',
    output: {
        filename: 'bundle.js',
        path: '/dist',
        libraryTarget: 'var',
        library: 'FRS'
    },
    resolve: {
        modulesDirectories: ["node_modules", "static/bower_components"],
        extensions: ['', '.webpack.js', '.web.js', '.ts', '.js']
    },
    module: {
        loaders: [
            {
                test: /\.ts$/,
                loader: 'ts-loader'
            }
        ]
    },
    plugins: [
        new webpack.ResolverPlugin(
            new webpack.ResolverPlugin.DirectoryDescriptionFilePlugin(".bower.json", ["main"])
        )
    ]
};
