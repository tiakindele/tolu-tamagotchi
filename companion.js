(function (global) {
  'use strict';
  const states = Object.freeze({idle: 2.4, coding: 0.8, thinking: 1.8, celebrating: 0.85, recharging: 1.8, sleeping: 2.4});
  const scriptBase = document.currentScript?.src || document.baseURI;
  const clamp = v => { const n = Number(v); if (!Number.isFinite(n)) throw new TypeError('Stat must be a finite number'); return Math.round(Math.max(0, Math.min(100, n))); };
  function mount(options = {}) {
    const target = options.target || document.body;
    const assetBase = options.assetBase || new URL('./sprites/', scriptBase).href;
    const base = new URL(assetBase.endsWith('/') ? assetBase : assetBase + '/', document.baseURI);
    const assets = Object.fromEntries(Object.keys(states).map(mood => [mood, options.sprites?.[mood] || new URL(mood + '.png', base).href]));
    const name = options.name ?? 'Tolu';
    const root = document.createElement('aside'); root.className = 'tolu-companion'; root.setAttribute('aria-label', name + ' companion');
    root.innerHTML = `<button type="button" class="tolu-companion__sprite"></button><div class="tolu-companion__panel"><div class="tolu-companion__heading"><span class="tolu-companion__name"></span><span class="tolu-companion__mood" aria-live="polite"></span></div>${['energy','focus'].map(stat => `<div class="tolu-companion__stat"><span>${stat[0].toUpperCase()+stat.slice(1)}</span><div class="tolu-companion__track" role="progressbar" aria-label="${stat}" aria-valuemin="0" aria-valuemax="100"><span class="tolu-companion__fill tolu-companion__fill--${stat}"></span></div><span class="tolu-companion__value"></span></div>`).join('')}</div>`;
    const sprite = root.querySelector('button'); const moodLabel = root.querySelector('.tolu-companion__mood');
    root.querySelector('.tolu-companion__name').textContent = name;
    const rows = [...root.querySelectorAll('.tolu-companion__stat')];
    let state = {mood:'idle',energy:80,focus:92}; let displayed = null; let timer; let transient = null;
    const preload = Object.values(assets).map(url => { const image = new Image(); image.src = url; return image; });
    function render() {
      const mood = transient || state.mood;
      if (displayed !== mood) {
        sprite.style.backgroundImage = `url(${JSON.stringify(assets[mood])})`;
        sprite.style.setProperty('--duration', states[mood]+'s');
        sprite.style.animationName = 'none'; void sprite.offsetWidth; sprite.style.removeProperty('animation-name');
        moodLabel.textContent = mood; sprite.setAttribute('aria-label', name + ' is ' + mood + '. Click to celebrate.'); displayed=mood;
      }
      ['energy','focus'].forEach((key,i) => { const value=state[key]; rows[i].querySelector('.tolu-companion__fill').style.width=value+'%'; rows[i].querySelector('.tolu-companion__track').setAttribute('aria-valuenow',value); rows[i].querySelector('.tolu-companion__value').textContent=value; });
    }
    function validate(mood) { if (!Object.hasOwn(states,mood)) throw new RangeError('Unknown mood: '+mood); }
    function setState(patch = {}) {
      const next = {...state};
      if (patch.mood !== undefined) {validate(patch.mood); next.mood=patch.mood;}
      for (const key of ['energy','focus']) if (patch[key] !== undefined) next[key]=clamp(patch[key]);
      if (patch.mood !== undefined) {clearTimeout(timer); transient=null;}
      state=next; render(); return {...state};
    }
    function play(mood, duration=2200) {validate(mood); if (!Number.isFinite(duration) || duration<0) throw new RangeError('Invalid duration'); clearTimeout(timer); transient=mood; render(); timer=setTimeout(()=>{transient=null; render();},duration);}
    sprite.addEventListener('click',()=>play('celebrating'));
    setState(options.initialState); target.append(root);
    return {setState, getState:()=>({...state}), play, celebrate:(ms)=>play('celebrating',ms), sleep:()=>setState({mood:'sleeping'}), recharge:(ms)=>play('recharging',ms), destroy:()=>{clearTimeout(timer);root.remove();preload.length=0;}};
  }
  global.ToluCompanion = Object.freeze({mount, states:Object.freeze(Object.keys(states))});
})(window);
