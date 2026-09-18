import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import fs from 'node:fs'
import path from 'node:path'
import { spawnSync } from 'node:child_process'

function imaRuntimePlugin() {
  return {
    name: 'ima-runtime-state',
    configureServer(server) {
      const root = path.resolve(process.cwd(), '..')
      const readJson = (file) => {
        try {
          const value = JSON.parse(fs.readFileSync(path.join(root, file), 'utf8'))
          return Array.isArray(value) ? value.length : Object.keys(value).length
        } catch { return 0 }
      }

      server.middlewares.use('/ima-api/runtime', (_req, res) => {
        const body = JSON.stringify({
          source: 'Ima-kernel runtime', updatedAt: new Date().toISOString(),
          memory: { available: fs.existsSync(path.join(root, 'founder/data/ima_memory.json')), records: readJson('founder/data/ima_memory.json') },
          learning: { available: fs.existsSync(path.join(root, 'learning/learning_memory.json')), records: readJson('learning/learning_memory.json') },
          agents: ['ChatGPT', 'Claude', 'Gemini'],
        })
        res.statusCode = 200
        res.setHeader('Content-Type', 'application/json')
        res.setHeader('Cache-Control', 'no-store')
        res.end(body)
      })

      server.middlewares.use('/ima-api/chat', (req, res) => {
        if (req.method !== 'POST') { res.statusCode = 405; return res.end() }
        let raw = ''
        req.on('data', chunk => { raw += chunk })
        req.on('end', () => {
          try {
            const { message } = JSON.parse(raw || '{}')
            if (typeof message !== 'string' || !message.trim()) throw new Error('message is required')
            const script = "import sys,json; from ima_master_runtime import ask; print(json.dumps(ask(sys.argv[1]), ensure_ascii=False))"
            const result = spawnSync('python3', ['-c', script, message], { cwd: root, encoding: 'utf8', timeout: 120000 })
            if (result.error) throw result.error
            if (result.status !== 0) throw new Error((result.stderr || result.stdout || 'IMA runtime failed').trim())
            const payload = JSON.parse(result.stdout.trim())
            const response = JSON.stringify({ response: payload.response || '', provider: 'IMA MASTER', runtime: payload.connections || {} })
            res.statusCode = 200
            res.setHeader('Content-Type', 'application/json; charset=utf-8')
            res.end(response)
          } catch (error) {
            res.statusCode = 500
            res.setHeader('Content-Type', 'application/json; charset=utf-8')
            res.end(JSON.stringify({ error: error.message }))
          }
        })
      })
    },
  }
}

export default defineConfig({
  base: '/Ima-kernel/',
  plugins: [react(), imaRuntimePlugin()],
  server: { proxy: { '/ima-api': { target: 'http://127.0.0.1:8081', changeOrigin: true, rewrite: path => path.replace(/^\/ima-api/, '') } } }
})
