import { defineConfig } from 'vite';
import reactRefresh from '@vitejs/plugin-react';
import tsconfigPaths from 'vite-tsconfig-paths';
import checker from 'vite-plugin-checker';
import packageInfo from './package.json';

// https://vitejs.dev/config/
export default defineConfig({
    build: {
        outDir: 'build',
        assetsDir: 'static/bundle',
        cssCodeSplit: true,
        sourcemap: false,
        manifest: 'assetsManifest',
        target: 'es2022',
        rollupOptions: {
            output: {
                assetFileNames: 'static/bundle/[name].[hash].[ext]',
            },
        },
    },
    server: {
        open: true,
        port: 3000,
    },
    css: {
        modules: {
            generateScopedName: '[name]_[local]__[hash:base64:5]',
        },
    },
    base: `/${packageInfo.homepage}`,
    plugins: [
        reactRefresh(),
        tsconfigPaths(),
        checker({
            typescript: true,
        }),
    ],
});