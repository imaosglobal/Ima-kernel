const express = require('express');
const app = express();

const PORT = process.env.PORT || 4000;

app.get('/', (req,res)=>res.send('OK'));

if(process.env.IMA_SAFE_MODE === '1'){
  console.log('[SAFE MODE] boot skipped');
  process.exit(0);
} else {
  app.listen(PORT, () => {
    console.log('[BOOT] running on', PORT);
  });
}