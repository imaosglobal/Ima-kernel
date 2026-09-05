import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins:[react()],
  server:{
    host: true,
    allowedHosts: true,
    proxy:{
      '/ima-api':{
        target: process.env.API_TARGET || 'http://127.0.0.1:8080',
        changeOrigin:true,
        rewrite:(path)=>path.replace(/^\/ima-api/,'')
      },
      '/bridge-api':{
        target: process.env.BRIDGE_URL || 'https://bedding-compute-denied-method.trycloudflare.com',
        changeOrigin:true,
        secure:true,
        rewrite:(path)=>path.replace(/^\/bridge-api/,'')
      }
    }
  }
})
