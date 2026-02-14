const fs = require('fs');
const path = require('path');

const WORDS = [
  'able','arch','bark','base','beam','bell','bird','bite','blue','boat',
  'bold','bone','book','bowl','burn','bush','cafe','cage','cake','calm',
  'cape','cave','clay','clip','code','coin','cold','cook','cool','cope',
  'cord','cork','cove','crow','cube','curl','dale','dame','dark','dawn',
  'days','deer','deli','demo','dew','dice','dine','dock','dome','door',
  'dove','down','draw','drum','dune','dusk','dust','earl','ease','east',
  'echo','edge','fawn','fern','fire','fish','flag','flat','flip','flow',
  'foam','fold','folk','font','food','ford','form','fort','frog','fuel',
  'full','fuse','gale','game','gate','gave','gaze','gems','gift','glad',
  'glen','glow','goat','gold','golf','good','gust','hail','hale','half',
  'hall','hare','harp','haze','heat','helm','herb','hero','hide','high',
  'hill','hint','hive','hold','home','hood','hook','hope','hour','hush',
  'iris','iron','isle','jade','jazz','join','jolt','jump','june','jury',
  'keen','kelp','kept','kind','kite','knob','knot','lace','lake','lamb',
  'lamp','lane','lark','late','lava','lawn','leaf','lean','lime','line',
  'link','lion','live','loft','loom','loop','lore','lush','lynx','malt',
  'mane','maps','mare','mark','mast','maze','mead','mesa','mild','mill',
  'mint','mist','mode','moon','moor','moss','moth','muse','nail','name',
  'navy','nest','noon','note','nova','oaks','opal','orca','oval','owls',
  'pace','pack','palm','park','pass','path','peak','pear','pier','pine',
  'plan','plum','poem','polo','pond','port','pour','prow','puff','pure',
  'quay','raft','rail','rain','reed','reef','rest','ride','rift','ring',
  'rise','road','robe','rock','rode','roll','roof','room','root','rope',
  'rose','ruby','rush','rust','sage','sail','salt','sand','seal','seed',
  'silk','skip','snow','soar','sole','song','soul','star','stem','surf',
  'swan','tale','tall','tame','tang','tape','tarn','teal','tent','thaw',
  'tide','tile','time','tint','tone','tour','tree','true','tune','turn',
  'vale','vane','vary','veil','vent','vest','view','vine','volt','wade',
  'wage','wake','walk','wall','wand','warm','wasp','wave','weed','well',
  'west','wick','wild','will','wind','wine','wing','wink','wish','wisp',
  'wold','wolf','wood','wool','word','wren','yarn','yawn','year','yell',
  'yoga','yoke','yore','zeal','zero','zinc','zone','zoom'
];

function generateSlug(repoRoot) {
  const iDir = path.join(repoRoot || path.resolve(__dirname, '..'), 'i');
  const maxAttempts = 500;

  for (let i = 0; i < maxAttempts; i++) {
    const a = WORDS[Math.floor(Math.random() * WORDS.length)];
    const b = WORDS[Math.floor(Math.random() * WORDS.length)];
    if (a === b) continue;
    const slug = `${a}-${b}`;
    if (!fs.existsSync(path.join(iDir, slug))) {
      return slug;
    }
  }
  throw new Error('Could not generate unique slug after ' + maxAttempts + ' attempts');
}

module.exports = generateSlug;
