import fs from 'node:fs'
import path from 'node:path'
import { pathToFileURL } from 'node:url'

import { command } from 'execa'

import { LogHelper } from '@/helpers/log-helper'

import buildAurora from './build-aurora'
import train from './train/train'

const MOVE_FALLBACK_ERROR_CODES = new Set(['EXDEV', 'EPERM', 'EBUSY', 'EACCES'])
const SERVER_DIST_PATH = path.join(process.cwd(), 'server', 'dist')
const SERVER_DIST_SRC_PATH = path.join(SERVER_DIST_PATH, 'server', 'src')
const SERVER_DIST_SERVER_PATH = path.join(SERVER_DIST_PATH, 'server')
const SERVER_MEMORY_SQL_SOURCE_PATH = path.join(
  process.cwd(),
  'server',
  'src',
  'core',
  'memory-manager',
  'sql'
)
const SERVER_MEMORY_SQL_DESTINATION_PATH = path.join(
  SERVER_DIST_PATH,
  'core',
  'memory-manager',
  'sql'
)

function isMoveFallbackError(error) {
  return (
    error instanceof Error &&
    'code' in error &&
    MOVE_FALLBACK_ERROR_CODES.has(error.code)
  )
}

async function movePath(sourcePath, destinationPath) {
  try {
    await fs.promises.rename(sourcePath, destinationPath)
  } catch (error) {
    if (!isMoveFallbackError(error)) {
      throw error
    }

    await fs.promises.cp(sourcePath, destinationPath, {
      recursive: true,
      force: true
    })
    await fs.promises.rm(sourcePath, { recursive: true, force: true })
  }
}

async function reshapeServerDist() {
  await Promise.all([
    fs.promises.rm(path.join(SERVER_DIST_PATH, 'core'), {
      recursive: true,
      force: true
    }),
    fs.promises.rm(path.join(SERVER_DIST_PATH, 'package.json'), {
      force: true
    })
  ])

  const entries = await fs.promises.readdir(SERVER_DIST_SRC_PATH, {
    withFileTypes: true
  })

  await Promise.all(
    entries.map((entry) =>
      movePath(
        path.join(SERVER_DIST_SRC_PATH, entry.name),
        path.join(SERVER_DIST_PATH, entry.name)
      )
    )
  )

  await fs.promises.rm(SERVER_DIST_SERVER_PATH, {
    recursive: true,
    force: true
  })
}

async function copyRuntimeAssets() {
  await fs.promises.mkdir(path.join(SERVER_DIST_PATH, 'tmp'), {
    recursive: true
  })
  await fs.promises.mkdir(SERVER_MEMORY_SQL_DESTINATION_PATH, {
    recursive: true
  })
  await fs.promises.cp(
    SERVER_MEMORY_SQL_SOURCE_PATH,
    SERVER_MEMORY_SQL_DESTINATION_PATH,
    {
      recursive: true,
      force: true
    }
  )
}

async function runBuildStep(stepName, step, quiet) {
  if (!quiet) {
    LogHelper.info(stepName)
  }

  await step()
}

/**
 * Build the production server output and copy runtime assets that TypeScript
 * does not emit by itself.
 */
export default async function buildServer(options = {}) {
  const { quiet = false } = options

  await runBuildStep(
    'Deleting server dist...',
    () =>
      fs.promises.rm(SERVER_DIST_PATH, {
        recursive: true,
        force: true
      }),
    quiet
  )
  await runBuildStep(
    'Training skill router duty...',
    () => train({ quiet }),
    quiet
  )
  await runBuildStep(
    'Building Aurora declarations...',
    () => buildAurora({ quiet }),
    quiet
  )
  await runBuildStep(
    'Compiling TypeScript...',
    () => command('tsc --project tsconfig.json', { stdio: quiet ? 'ignore' : 'inherit' }),
    quiet
  )
  await runBuildStep(
    'Resolving TS paths...',
    () => command('resolve-tspaths', { stdio: quiet ? 'ignore' : 'inherit' }),
    quiet
  )
  await runBuildStep('Reshaping server dist...', () => reshapeServerDist(), quiet)
  await runBuildStep('Copying runtime assets...', () => copyRuntimeAssets(), quiet)
}

const isMainModule =
  process.argv[1] &&
  import.meta.url === pathToFileURL(process.argv[1]).href

if (isMainModule) {
  ;(async () => {
    try {
      await buildServer()
    } catch (e) {
      LogHelper.error(`Failed to build server: ${e}`)
      process.exit(1)
    }
  })()
}
