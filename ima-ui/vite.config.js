import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  base: '/Ima-kernel/',
  plugins:[react()],
  server:{
    proxy:{
      '/ima-api':{
        target:'http://127.0.0.1:8081',
        changeOrigin:true,
        rewrite:(path)=>path.replace(/^\/ima-api/,'')
      }
    }
  }
})
