import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';

const path = new URL('../public/mother_character.glb', import.meta.url);
const bytes = await readFile(path);
const gitBlobSha1 = createHash('sha1')
  .update(`blob ${bytes.length}\0`)
  .update(bytes)
  .digest('hex');

const expected = '217170d2bd67051270be974292dc3b834eefe206';
if (gitBlobSha1 !== expected) {
  console.error(`IMA_GL B_VERIFY=FAIL expected=${expected} actual=${gitBlobSha1}`);
  process.exit(1);
}
console.log(`IMA_GLB_VERIFY=PASS sha=${gitBlobSha1} bytes=${bytes.length}`);
