import assert from 'node:assert/strict';
import { test } from 'node:test';
import { build } from 'esbuild';
import { fileURLToPath } from 'node:url';

const result = await build({ entryPoints: [fileURLToPath(new URL('../src/konva_editor/answerReview.ts', import.meta.url))], bundle: true, write: false, format: 'esm' });
const { answerChoicesFromArtifacts, reviewSettings, normalizedAnswer } = await import(`data:text/javascript;base64,${Buffer.from(result.outputFiles[0].text).toString('base64')}`);

test('numbered choice answers use displayed numbers, not slot order', () => {
  const semantic = { answer: { target: { type: 'choice_number' }, choices: [
    { id: 'b', text: '② B' }, { id: 'a', text: '① A' },
  ] } };
  const choices = answerChoicesFromArtifacts(semantic, null, [{ value: '2', ref: 'answer.value' }]);
  assert.deepEqual(choices.map(({label,text,correct}) => ({label,text,correct})), [{label:'①',text:'A',correct:false},{label:'②',text:'B',correct:true}]);
});
test('a known answer ID wins when two choices have identical text', () => {
  const choices = answerChoicesFromArtifacts({answer:{choices:[{id:'a',text:'same'},{id:'b',text:'same'}]}}, null, [{ref:'b',value:'same'}]);
  assert.deepEqual(choices.map((c)=>c.correct), [false,true]);
});
test('legacy marker and value do not become separate choices', () => {
  const choices = answerChoicesFromArtifacts({answer:{choices:[{id:'slot.c.marker',text:'①'},{id:'c1',slot_id:'slot.c.value',label:'①',text:'21'}]}}, null, [{ref:'c1',value:'21'}]);
  assert.equal(choices.length,1);
  assert.equal(choices[0].text,'21');
});
test('OX answers become three independent inputs', () => {
  const settings = reviewSettings(null,[{value:'○, ×, ○'}],[], 'panel_input');
  assert.equal(settings.mode,'ox');
  assert.deepEqual(settings.answers.map((a)=>a.value),['O','X','O']);
});
test('multiple subquestions retain repeated answers and separate groups', () => {
  const settings = reviewSettings({answer:{choice_groups:[{label:'(1)',choices:['A','B']},{label:'(2)',choices:['A','B']}]}},[{value:'B'},{value:'B'}],[], 'choice');
  assert.equal(settings.mode,'grouped_choice');
  assert.deepEqual(settings.groups.map((g)=>g.correct_index),[1,1]);
});
test('decimal punctuation is significant for grading', () => {
  assert.notEqual(normalizedAnswer('1.2'), normalizedAnswer('12'));
  assert.equal(normalizedAnswer('○'), normalizedAnswer('O'));
  assert.equal(normalizedAnswer('×'), normalizedAnswer('x'));
});
test('person selection without choices requests review instead of guessing a name', () => {
  const settings = reviewSettings({answer:{target:{type:'person_selection'},value:1}},[{value:'1'}],[], 'panel_input');
  assert.equal(settings.mode,'choice');
  assert.equal(settings.status,'needs_changes');
  assert.deepEqual(settings.choices,[]);
});
