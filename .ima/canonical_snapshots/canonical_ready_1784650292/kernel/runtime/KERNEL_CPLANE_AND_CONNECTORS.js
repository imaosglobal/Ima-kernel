const fs = require('fs');
const { execSync } = require('child_process');

/* =========================
   CONTROL PLANE (2)
   ========================= */

const STATE_FILE = './runtime/kernel_state.json';

function load() {
  try { return JSON.parse(fs.readFileSync(STATE_FILE,'utf8')); }
  catch { return {}; }
}

function save(s) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(s,null,2));
}

const CONTROL_PLANE = {

  policy(event) {
    if (!event) return { ok:false, reason:'no_event' };
    if (event.type === 'WRITE_FILE' && !event.payload?.file) {
      return { ok:false, reason:'missing_file' };
    }
    return { ok:true };
  },

  mutate(stateUpdate) {
    const s = load();
    Object.assign(s, stateUpdate);
    save(s);
    return s;
  },

  audit() {
    const s = load();
    return {
      version: s.version,
      stable: s.stability,
      locked: s.e2e_locked
    };
  }
};


/* =========================
   EXTERNAL CONNECTORS (3)
   ========================= */

const CONNECTORS = {

  git: {

    status() {
      return execSync('git status --porcelain').toString().trim();
    },

    commit(msg) {
      execSync(`git add . && git commit -m "${msg}"`);
      return true;
    },

    push() {
      execSync('git push');
      return true;
    }
  },

  npm: {

    version() {
      const p = JSON.parse(fs.readFileSync('./package.json','utf8'));
      return p.version;
    },

    bump() {
      const p = JSON.parse(fs.readFileSync('./package.json','utf8'));
      const parts = p.version.split('.').map(Number);
      parts[2] += 1;
      p.version = parts.join('.');
      fs.writeFileSync('./package.json', JSON.stringify(p,null,2));
      return p.version;
    }
  },

  runtime: {

    scanRuntime() {
      const dir = './runtime';
      const files = fs.readdirSync(dir);
      return {
        files: files.length,
        js: files.filter(f=>f.endsWith('.js')).length,
        json: files.filter(f=>f.endsWith('.json')).length
      };
    }
  }
};


/* =========================
   UNIFIED API
   ========================= */

function syncCycle() {

  const gitStatus = CONNECTORS.git.status();

  const dirty = gitStatus.length > 0;

  if (dirty) {
    CONTROL_PLANE.mutate({
      git: 'dirty',
      last_sync: Date.now()
    });

    return {
      status: 'blocked',
      reason: 'git_dirty'
    };
  }

  const newVersion = CONNECTORS.npm.bump();

  CONNECTORS.git.commit(`auto sync ${newVersion}`);

  CONTROL_PLANE.mutate({
    version: newVersion,
    last_sync: Date.now(),
    git: 'clean'
  });

  return {
    status: 'synced',
    version: newVersion
  };
}

module.exports = {
  CONTROL_PLANE,
  CONNECTORS,
  syncCycle
};
