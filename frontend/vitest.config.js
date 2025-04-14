import path from 'path'
import vue from '@vitejs/plugin-vue'

export default {
    test: {
      globals: true,
      environment: 'jsdom',
      transformMode: {
        web: [/\.vue$/],
      },
    },      
    plugins: [vue()],
    resolve: {
    alias: {
        '@': path.resolve(__dirname, './src'),
    },
  }
}
  